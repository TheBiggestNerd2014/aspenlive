"""Checks and path helpers for export, shared by the dialog and unit tests.

The timeline clock stays on the project frame rate and sample rate. The writer
may resample at the edge. These helpers keep that contract testable without
opening the export dialog.
"""

import os
import shutil

PARTIAL_SUFFIX = ".aspenlive-partial"
MAX_EXPORT_FPS = 480
STALL_SECONDS = 20
MAX_REPEATED_BAD_FRAMES = 5

_KEYFRAME_PROPERTIES = (
    "volume", "time", "location_x", "location_y", "scale_x", "scale_y", "alpha",
)
_HARDWARE_MARKERS = ("nvenc", "qsv", "amf", "vaapi", "videotoolbox", "vulkan", "_mf")


def partial_export_path(path):
    """A sibling path that is renamed onto `path` only after the file is valid.

    The real extension stays at the end. FFmpeg chooses the container from it,
    and a suffix after `.mp4` is reported as an unknown format.
    """
    folder, name = os.path.split(path)
    stem, ext = os.path.splitext(name)
    if not ext:
        return path + PARTIAL_SUFFIX
    return os.path.join(folder, stem + PARTIAL_SUFFIX + ext)


def cumulative_samples(frame, sample_rate, fps_num, fps_den):
    """Samples through the end of `frame` (1-based), rounded to the nearest sample.

    Integer arithmetic matches Frame::GetSamplesPerFrame so 23.976 fps does not
    drift the way a repeated double multiply does.
    """
    if frame <= 0 or sample_rate <= 0 or fps_num <= 0 or fps_den <= 0:
        return 0
    numerator = frame * sample_rate * fps_den
    return (numerator + fps_num // 2) // fps_num


def samples_per_frame(frame, sample_rate, fps_num, fps_den, channels):
    """Channel-aligned sample count for one timeline frame."""
    if channels <= 0:
        return 0

    def align(samples):
        if channels <= 1 or samples <= 0:
            return max(0, samples)
        return samples - (samples % channels)

    previous = align(cumulative_samples(frame - 1, sample_rate, fps_num, fps_den))
    total = align(cumulative_samples(frame, sample_rate, fps_num, fps_den))
    return max(0, total - previous)


def total_samples(start_frame, end_frame, sample_rate, fps_num, fps_den, channels):
    """Exact sample budget for a contiguous export range."""
    if end_frame < start_frame:
        return 0
    return sum(
        samples_per_frame(frame, sample_rate, fps_num, fps_den, channels)
        for frame in range(int(start_frame), int(end_frame) + 1)
    )


_VALUE_EPSILON = 0.001


def _fps_factor(fps_factor):
    try:
        factor = float(fps_factor or 1.0)
    except (TypeError, ValueError):
        factor = 1.0
    if factor <= 0:
        return 1.0
    return factor


def _knot_frames(curve):
    """Frame numbers stored on a Keyframe, via GetCount/GetPoint."""
    frames = []
    try:
        count = int(curve.GetCount())
    except Exception:
        return frames
    for index in range(max(0, count)):
        try:
            frame = int(round(float(curve.GetPoint(index).co.X)))
        except Exception:
            continue
        if frame > 0:
            frames.append(frame)
    return frames


def _sample_pairs(left, right, factor):
    """Preview/export frame pairs at each knot and halfway between knots."""
    pairs = {(1, max(1, int(round(factor))))}
    for frame in _knot_frames(left):
        pairs.add((frame, max(1, int(round(frame * factor)))))
    for frame in _knot_frames(right):
        pairs.add((max(1, int(round(frame / factor))), frame))
    preview_frames = sorted({preview for preview, _export in pairs})
    for start, end in zip(preview_frames, preview_frames[1:]):
        if end - start > 1:
            middle = (start + end) // 2
            pairs.add((middle, max(1, int(round(middle * factor)))))
    return sorted(pairs)


def keyframe_value_mismatch(preview_clip, export_clip, fps_factor=1.0):
    """Property name when sampled GetValue/GetLong differs, else None.

    Point lists are not compared. Loading a curve sorts points and keeps the
    last point at a duplicate frame, so the saved JSON and Timeline.Json()
    can disagree while every interpolated value still matches.
    """
    factor = _fps_factor(fps_factor)
    for prop in _KEYFRAME_PROPERTIES:
        left = getattr(preview_clip, prop, None)
        right = getattr(export_clip, prop, None)
        if left is None or right is None:
            return prop
        compared = False
        for preview_frame, export_frame in _sample_pairs(left, right, factor):
            try:
                left_value = float(left.GetValue(int(preview_frame)))
                right_value = float(right.GetValue(int(export_frame)))
            except Exception:
                continue
            compared = True
            if abs(left_value - right_value) > _VALUE_EPSILON:
                return prop
            if prop == "time":
                try:
                    if int(left.GetLong(int(preview_frame))) != int(right.GetLong(int(export_frame))):
                        return prop
                except Exception:
                    continue
        # A curve that cannot be sampled must not block the export.
        if not compared:
            continue
    return None


def timeline_keyframe_mismatch(preview_timeline, export_timeline, fps_factor=1.0):
    """Property or "clips" when the export timeline disagrees with preview."""
    try:
        preview_clips = {clip.Id(): clip for clip in preview_timeline.Clips()}
        export_clips = {clip.Id(): clip for clip in export_timeline.Clips()}
    except Exception:
        return None
    if preview_clips and not export_clips:
        return "clips"
    for clip_id, preview_clip in preview_clips.items():
        export_clip = export_clips.get(clip_id)
        if export_clip is None:
            return "clips"
        mismatch = keyframe_value_mismatch(preview_clip, export_clip, fps_factor)
        if mismatch:
            return mismatch
    return None


def preflight_export(folder, fps_num, fps_den, start_frame, end_frame, bits_per_second):
    """One-sentence problems that should stop an export before encoding starts."""
    issues = []
    if fps_den <= 0 or fps_num <= 0:
        issues.append("Frame rate is not valid.")
    else:
        fps = fps_num / float(fps_den)
        if fps < 1 or fps > MAX_EXPORT_FPS:
            issues.append("Frame rate must be between 1 and 480.")
    if end_frame <= start_frame:
        issues.append("Select a valid range of frames to export.")
    if not folder or not os.path.isdir(folder):
        issues.append("Export folder does not exist.")
        return issues
    probe = os.path.join(folder, ".aspenlive-write-probe")
    try:
        with open(probe, "w"):
            pass
        os.remove(probe)
    except OSError:
        issues.append("Export folder is not writable.")
        return issues
    if end_frame > start_frame and fps_num > 0 and fps_den > 0:
        try:
            free = shutil.disk_usage(folder).free
        except OSError:
            free = None
        if free is not None:
            seconds = (end_frame - start_frame + 1) * fps_den / float(fps_num)
            estimate = int(max(int(bits_per_second or 0), 1000000) * seconds / 8) + 1000000
            if free < estimate:
                issues.append("Not enough free disk space for this export.")
    return issues


def software_video_fallback(vcodec):
    """Software codec used once when a hardware encoder fails to open."""
    name = (vcodec or "").lower()
    if not any(marker in name for marker in _HARDWARE_MARKERS):
        return None
    if "hevc" in name or "h265" in name or "265" in name:
        return "libx265"
    if "av1" in name:
        return "libsvtav1"
    return "libx264"


def remove_partial(path):
    """Delete a partial export. A missing file is not an error."""
    if not path:
        return
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass
