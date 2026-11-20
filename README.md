# AspenLive

AspenLive is a Windows video editor based on the [OpenShot](https://www.openshot.org/) platform. It keeps the familiar docked workspace (preview, timeline, project files, titles, properties) with AspenLive’s gray-and-gold UI and `.alp` project format.

**Repository:** [github.com/TheBiggestNerd2014/aspenlive](https://github.com/TheBiggestNerd2014/aspenlive)  
**Status:** preparing **0.1** for production use (current installer builds are labeled **0.0.1**).

---

## Features

- Import video, audio, and images
- Multi-track timeline editing (trim, razor, snapping, keyframes)
- Direct Text overlays in the preview
- SVG Titles, including a Credits template with add/remove rows
- Real-time preview and export

The app ships as a single Windows installer (`aspenlive.exe`) that includes the editor, video engine, and audio stack.

---

## Install (Windows)

1. Close AspenLive if it is already running.
2. Run the latest installer from [Releases](https://github.com/TheBiggestNerd2014/aspenlive/releases) when available, or a local build:

   `aspenlive_editor/installer/Output/AspenLive-0.0.1-x64.exe`
3. Finish the setup wizard (default install location is Program Files).
4. Launch **AspenLive** from the Start menu or desktop shortcut.

No separate runtime install is required.

### First launch

A project library dialog appears so you can open an existing project or start a new one.

Projects always live here (this path is fixed):

```text
Documents\AspenLive\
  .alp\       # project files, e.g. japan-video.alp
  assets\     # per-project folders, e.g. japan-video-assets\
```

App settings, caches, and recovery files stay under `%USERPROFILE%\.aspenlive\`.

---

## Project layout

| Item | Location |
|------|----------|
| Project file | `Documents\AspenLive\.alp\<name>.alp` |
| Project assets | `Documents\AspenLive\assets\<name>-assets\` |
| App data / cache | `%USERPROFILE%\.aspenlive\` |

`.alp` is the native format. Older `.osp` projects still open; saves go to `.alp` in the library above.

---

## Workspace

Classic OpenShot-style layout:

- **Preview** — frame-accurate viewer with transform handles
- **Timeline** — tracks, clips, transitions, keyframes, snapping
- **Project Files** — imported media
- **Transitions / Effects / Titles** — libraries for the timeline
- **Properties** — clip and effect parameters

AspenLive adds the Cosmic theme, Direct Text, Credits titles, and the fixed project library.

---

## Repository structure

| Folder | Role |
|--------|------|
| [`aspenlive_editor`](https://github.com/TheBiggestNerd2014/aspenlive/tree/main/aspenlive_editor) | Qt/Python editor UI and Windows installer |
| [`aspenlive_engine`](https://github.com/TheBiggestNerd2014/aspenlive/tree/main/aspenlive_engine) | Video engine (libopenshot fork) |
| [`aspenlive_ae`](https://github.com/TheBiggestNerd2014/aspenlive/tree/main/aspenlive_ae) | Audio engine (libopenshot-audio fork) |

Day-to-day packaging uses the freeze tree and Inno Setup under `aspenlive_editor/installer/`. Rebuild the native engines only when C++ code changes.

---

## Support

- Report issues: [github.com/TheBiggestNerd2014/aspenlive/issues](https://github.com/TheBiggestNerd2014/aspenlive/issues)
- Logs and recovery: `%USERPROFILE%\.aspenlive\`
- Close the app before reinstalling when updating from a new installer.

---

## License & lineage

AspenLive builds on the OpenShot open-source stack ([openshot-qt](https://github.com/OpenShot/openshot-qt), [libopenshot](https://github.com/OpenShot/libopenshot), [libopenshot-audio](https://github.com/OpenShot/libopenshot-audio)), rebranded and extended for AspenLive. See `LICENSE` and the license files in each component tree for details.

---

## 0.1 focus

0.1 aims for a solid Windows installer, a clear project library, polished Cosmic UI, and dependable editing/title workflows. Feedback on install, project paths, and Credits/titles is especially welcome.
