"""Export clock, keyframe agreement, and log-cap helpers."""

import os
import sys
import tempfile
import types
import unittest

from classes.export_robustness import (
    cumulative_samples,
    keyframe_value_mismatch,
    partial_export_path,
    preflight_export,
    samples_per_frame,
    software_video_fallback,
    timeline_keyframe_mismatch,
    total_samples,
)


class ExportRobustnessTests(unittest.TestCase):
    def test_fractional_fps_sample_budget_matches_integer_rounding(self):
        frames = 100000
        fps_num, fps_den, rate, channels = 24000, 1001, 48000, 2
        summed = total_samples(1, frames, rate, fps_num, fps_den, channels)
        expected = cumulative_samples(frames, rate, fps_num, fps_den)
        expected -= expected % channels
        self.assertEqual(summed, expected)
        self.assertEqual(samples_per_frame(1, 44100, 30, 1, 2), 1470)
        self.assertEqual(samples_per_frame(1, 48000, 30, 1, 2), 1600)

    def test_keyframe_mismatch_names_the_property(self):
        def curve(values):
            class Point:
                def __init__(self, x, y):
                    self.co = types.SimpleNamespace(X=x, Y=y)

            class Curve:
                def GetCount(self):
                    return len(values)

                def GetPoint(self, index):
                    x = sorted(values)[index]
                    return Point(x, values[x])

                def GetValue(self, frame):
                    frame = int(frame)
                    earlier = [x for x in values if x <= frame]
                    return values[max(earlier) if earlier else min(values)]

                def GetLong(self, frame):
                    return int(round(self.GetValue(frame)))

            return Curve()

        def clip(clip_id, volume):
            props = {
                "volume": curve(volume),
                "time": curve({1: 1}),
                "location_x": curve({1: 0.0}),
                "location_y": curve({1: 0.0}),
                "scale_x": curve({1: 1.0}),
                "scale_y": curve({1: 1.0}),
                "alpha": curve({1: 1.0}),
            }

            class Clip:
                def Id(self):
                    return clip_id

            item = Clip()
            for name, value in props.items():
                setattr(item, name, value)
            return item

        class Timeline:
            def __init__(self, clips):
                self._clips = clips

            def Clips(self):
                return self._clips

        same = clip("a", {1: 1.0, 30: 0.0})
        quieter = clip("a", {1: 1.0, 30: 0.5})
        self.assertIsNone(keyframe_value_mismatch(same, same))
        self.assertEqual(keyframe_value_mismatch(same, quieter), "volume")
        # Duplicate and unsorted points collapse on load. Matching samples pass.
        collapsed = clip("a", {1: 2.0, 30: 0.0})
        also_collapsed = clip("a", {1: 2.0, 30: 0.0})
        self.assertIsNone(keyframe_value_mismatch(collapsed, also_collapsed))
        self.assertIsNone(timeline_keyframe_mismatch(Timeline([same]), Timeline([same])))
        self.assertEqual(timeline_keyframe_mismatch(Timeline([same]), Timeline([])), "clips")

    def test_preflight_and_partial_path(self):
        self.assertEqual(
            os.path.basename(partial_export_path(os.path.join("DJG", "djg.mp4"))),
            "djg.aspenlive-partial.mp4",
        )
        self.assertIsNone(software_video_fallback("libx264"))
        self.assertEqual(software_video_fallback("h264_nvenc"), "libx264")
        with tempfile.TemporaryDirectory() as folder:
            issues = preflight_export(folder, 30, 1, 1, 10, 1000000)
            self.assertEqual(issues, [])
            self.assertIn("does not exist", preflight_export(os.path.join(folder, "missing"), 30, 1, 1, 10, 1000)[0])
            self.assertTrue(preflight_export(folder, 0, 1, 1, 10, 1000))

    def test_oversized_engine_log_is_replaced_in_place(self):
        sys.modules.setdefault("openshot", types.ModuleType("openshot"))
        from classes.logger_libopenshot import ENGINE_LOG_MAX_BYTES, prepare_log_file
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "libopenshot.log")
            with open(path, "wb") as handle:
                handle.write(b"x" * (ENGINE_LOG_MAX_BYTES + 10))
            prepare_log_file(path)
            self.assertLess(os.path.getsize(path), ENGINE_LOG_MAX_BYTES)


if __name__ == "__main__":
    unittest.main()
