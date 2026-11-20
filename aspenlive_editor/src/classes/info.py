"""
 @file
 @brief This file contains the current version number of OpenShot, along with other global settings.
 @author Jonathan Thomas <jonathan@openshot.org>

 @section LICENSE

 Copyright (c) 2008-2026 OpenShot Studios, LLC
 (http://www.openshotstudios.com). This file is part of
 OpenShot Video Editor (http://www.openshot.org), an open-source project
 dedicated to delivering high quality video editing and animation solutions
 to the world.

 OpenShot Video Editor is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 OpenShot Video Editor is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with OpenShot Library.  If not, see <http://www.gnu.org/licenses/>.
 """

import os
import re
import sys
import tempfile

VERSION = "0.0.1"
MINIMUM_LIBOPENSHOT_VERSION = "1.2.0"
DATE = "20261117000000"
NAME = "aspenlive"
PRODUCT_NAME = "AspenLive"
# Upstream commits this tree was forked from.
UPSTREAM_OPENSHOT_QT = "890e7c895ffe7cf680aab6069a06042362d9d718"
UPSTREAM_LIBOPENSHOT = "83675780c69582bb633b6ec0c7f8475a1df0961a"
UPSTREAM_LIBOPENSHOT_AUDIO = "289816cea961831ba856501bc2fd7b890a391516"
GPL_VERSION = "3"
DESCRIPTION = "Create and edit videos, films, and animations."
COMPANY_NAME = "The Biggest Studios"
COPYRIGHT = "Copyright 2026 The Biggest Studios"
CWD = os.getcwd()

# Application paths
# Windows/Linux assets sit by the executable. Mac assets follow classes under lib,
# then under Resources after the DMG builder moves and symlinks that directory.
PATH = (os.path.dirname(os.path.abspath(sys.executable))
        if getattr(sys, "frozen", False) and sys.platform != "darwin"
        else os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
RESOURCES_PATH = os.path.join(PATH, "resources")
PROFILES_PATH = os.path.join(PATH, "profiles")
IMAGES_PATH = os.path.join(PATH, "images")
EXPORT_PRESETS_PATH = os.path.join(PATH, "presets")
COLORS_PATH = os.path.join(PATH, "colors")

# User paths
HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, ".aspenlive")
# Fixed project library (not user-configurable): Documents/AspenLive/.alp + /assets
PROJECTS_ROOT = os.path.join(HOME_PATH, "Documents", "AspenLive")
PROJECTS_ALP_PATH = os.path.join(PROJECTS_ROOT, ".alp")
PROJECTS_ASSETS_PATH = os.path.join(PROJECTS_ROOT, "assets")
ASSETS_PATH = USER_PATH
BACKUP_PATH = os.path.join(USER_PATH)
RECOVERY_PATH = os.path.join(USER_PATH, "recovery")
THUMBNAIL_PATH = os.path.join(USER_PATH, "thumbnail")
CACHE_PATH = os.path.join(USER_PATH, "cache")
BLENDER_PATH = os.path.join(USER_PATH, "blender")
TITLE_PATH = os.path.join(USER_PATH, "title")
TRANSITIONS_PATH = os.path.join(USER_PATH, "transitions")
EMOJIS_PATH = os.path.join(USER_PATH, "emojis")
PREVIEW_CACHE_PATH = os.path.join(USER_PATH, "preview-cache")
USER_PROFILES_PATH = os.path.join(USER_PATH, "profiles")
USER_PRESETS_PATH = os.path.join(USER_PATH, "presets")
USER_TITLES_PATH = os.path.join(USER_PATH, "title_templates")
COMFYUI_PATH = os.path.join(USER_PATH, "comfyui")
COMFYUI_OUTPUT_PATH = os.path.join(USER_PATH, "comfyui-output")
USER_COLORS_PATH = os.path.join(USER_PATH, "colors")
PROTOBUF_DATA_PATH = os.path.join(USER_PATH, "protobuf_data")
YOLO_PATH = os.path.join(USER_PATH, "yolo")
CLIPBOARD_PATH = os.path.join(USER_PATH, "clipboard")
PROXY_PATH = os.path.join(USER_PATH, "optimized")
# User files
BACKUP_FILE = os.path.join(BACKUP_PATH, "backup.alp")
LEGACY_BACKUP_FILE = os.path.join(BACKUP_PATH, "backup.osp")
USER_DEFAULT_PROJECT = os.path.join(USER_PATH, "default.alp")
OSP_DEFAULT_PROJECT = os.path.join(USER_PATH, "default.osp")
LEGACY_DEFAULT_PROJECT = os.path.join(USER_PATH, "default.project")
# .alp is the save name. .osp is the same project document and still opens.
PROJECT_EXTENSION = ".alp"
_PROJECT_FILE = re.compile(r"\.(?:alp|osp)(?P<bak>\.bak(?:\.\d+)?)?\Z", re.IGNORECASE)

# Back up "default" values for user paths
_path_defaults = {
    k: v for k, v in locals().items()
    if k.endswith("_PATH")
    and v.startswith(USER_PATH)
}

# Only project assets follow the unsaved assets preference. Settings, caches,
# recovery files, templates, and downloaded tools remain in USER_PATH.
_asset_folders = {
    "THUMBNAIL_PATH": "thumbnail",
    "TITLE_PATH": "title",
    "BLENDER_PATH": "blender",
    "PROTOBUF_DATA_PATH": "protobuf_data",
    "CLIPBOARD_PATH": "clipboard",
    "COMFYUI_OUTPUT_PATH": "comfyui-output",
    "PROXY_PATH": "optimized",
}


def _check_assets_folder(path):
    """Create and check a writable directory without touching existing files."""
    os.makedirs(path, exist_ok=True)
    with tempfile.TemporaryFile(dir=path):
        pass


def default_assets_path():
    """Choose the Linux Snap-accessible default, retaining the legacy fallback."""
    videos = os.path.join(HOME_PATH, "Videos")
    if sys.platform.startswith("linux") and os.path.isdir(videos):
        candidate = os.path.join(videos, ".aspenlive-tmp")
        try:
            _check_assets_folder(candidate)
            return candidate
        except OSError:
            pass
    return USER_PATH


def set_assets_path(path):
    """Retarget active project assets without changing the unsaved defaults."""
    global ASSETS_PATH
    ASSETS_PATH = path
    for name, folder in _asset_folders.items():
        globals()[name] = os.path.join(path, folder)


def configure_asset_defaults(path):
    """Apply the startup preference, falling back if it cannot be used."""
    path = os.path.abspath(os.path.expanduser(path or USER_PATH))
    try:
        _check_assets_folder(path)
        for folder in _asset_folders.values():
            _check_assets_folder(os.path.join(path, folder))
    except OSError:
        path = USER_PATH
        for folder in _asset_folders.values():
            os.makedirs(os.path.join(path, folder), exist_ok=True)
    set_assets_path(path)
    for name in ("ASSETS_PATH", *_asset_folders):
        _path_defaults[name] = globals()[name]
    return path


try:
    from qt_api import QSize

    # UI Thumbnail settings
    LIST_ICON_SIZE = QSize(100, 65)
    LIST_GRID_SIZE = LIST_ICON_SIZE + QSize(5, 25)
    TREE_ICON_SIZE = QSize(75, 49)
    EMOJI_ICON_SIZE = QSize(75, 75)
    EMOJI_GRID_SIZE = EMOJI_ICON_SIZE + QSize(5, 25)
    # Runtime emoji selections
    EMOJI_FILES = {}
    EMOJI_PATH = ""
    EMOJI_ICON = ""
except ImportError:
    # Fail gracefully if we're running without Qt (e.g. CI tasks)
    print("Failed to import `qt_api.QSize` (ignoring exception)")

# Maintainer details, for packaging
JT = {"name": "Jonathan Thomas",
      "email": "jonathan@openshot.org",
      "website": "http://openshot.org/developers/jonathan"}

# Desktop launcher ID, for Linux
DESKTOP_ID = "org.aspenlive.AspenLive.desktop"

# Blender minimum version required (a string value)
BLENDER_MIN_VERSION = "5.0"

# Data-model debugging enabler
MODEL_TEST = False
FEEDBACK_PREVIEW = False  # Launch-only preview; never stored in user settings.
RATING_PREVIEW = False  # Launch-only Store UI preview on any installation.
UPDATE_PREVIEW = False

# Default/initial logging levels
LOG_LEVEL_FILE = 'INFO'
LOG_LEVEL_CONSOLE = 'INFO'

# Sentry.io error & transaction reporting rate (0.0 TO 1.0)
# 0.0 = no error reporting to Sentry
# 0.5 = 1/2 of errors reported to Sentry
# 1.0 = all errors reporting to Sentry
#    ERROR: Exceptions sent to Sentry
#    TRANS: Transactions sent to Sentry
#    STABLE: If both version and build commit match the current published release
#    UNSTABLE: Older versions, different builds, or unconfirmed releases
#    STABLE_VERSION: This is the current stable release reported by openshot.org
ERROR_REPORT_RATE_STABLE = 0.0
ERROR_REPORT_RATE_UNSTABLE = 0.0
TRANS_REPORT_RATE_STABLE = 0.0
TRANS_REPORT_RATE_UNSTABLE = 0.0
ERROR_REPORT_STABLE_VERSION = None
ERROR_REPORT_IS_RELEASE = False

# Languages
CMDLINE_LANGUAGE = None
CURRENT_LANGUAGE = 'en_US'
SUPPORTED_LANGUAGES = ['en_US']

try:
    from language import openshot_lang
    language_path = ":/locale/"
except ImportError:
    language_path = os.path.join(PATH, 'language')
    print("Compiled translation resources missing!")
    print(f"Loading translations from: {language_path}")

# Compile language list from :/locale resource
try:
    from qt_api import QDir
    langdir = QDir(language_path)
    trpaths = langdir.entryList(
        ['OpenShot_*.qm'],
        QDir.NoDotAndDotDot | QDir.Files,
        sort=QDir.Name)
    for trpath in trpaths:
        # Extract everything between "Openshot_" and ".qm"
        lang=trpath[trpath.find('_')+1:-3]
        SUPPORTED_LANGUAGES.append(lang)
except ImportError:
    # Fail gracefully if we're running without Qt (e.g. CI tasks)
    print("Failed to import `qt_api.QDir` (ignoring exception)")

SETUP = {
    "name": NAME,
    "version": VERSION,
    "author": JT["name"] + " and others",
    "author_email": JT["email"],
    "maintainer": JT["name"],
    "maintainer_email": JT["email"],
    "url": "",
    "license": "GNU GPL v." + GPL_VERSION,
    "description": DESCRIPTION,
    "long_description": "Create and edit videos and movies\n"
                        " AspenLive is a video editor from The Biggest Studios. Original code from\n"
                        " OpenShot Video Editor. It can create and edit videos and movies using many popular video, audio, \n"
                        " image formats.  Create videos for YouTube, Flickr, Vimeo, Metacafe, iPod,\n"
                        " Xbox, and many more common formats!\n"
                        ".\n"
                        " Features include:\n"
                        "  * Multiple tracks (layers)\n"
                        "  * Compositing, image overlays, and watermarks\n"
                        "  * Support for image sequences (rotoscoping)\n"
                        "  * Key-frame animation\n  * Video and audio effects (chroma-key)\n"
                        "  * Transitions (lumas and masks)\n"
                        "  * 3D animation (titles and simulations)\n"
                        "  * Upload videos (YouTube and Vimeo supported)",

    # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "classifiers": [
                       "Development Status :: 5 - Production/Stable",
                       "Environment :: X11 Applications",
                       "Environment :: X11 Applications :: GTK",
                       "Intended Audience :: End Users/Desktop",
                       "License :: OSI Approved :: GNU General Public License (GPL)",
                       "Operating System :: OS Independent",
                       "Operating System :: POSIX :: Linux",
                       "Programming Language :: Python",
                       "Topic :: Artistic Software",
                       "Topic :: Multimedia :: Video :: Non-Linear Editor", ] +
                   ["Natural Language :: " + language for language in SUPPORTED_LANGUAGES],

    # Automatic launch script creation
    "entry_points": {
        "console_scripts": ["openshot-cli = openshot_qt.cli:main"],
        "gui_scripts": [
            "openshot-qt = openshot_qt.launch:main"
        ]
    }
}

def is_project_file(path):
    """True for an AspenLive project, including an older .osp file."""
    if not path or str(path).startswith("content:"):
        return bool(path)
    return _PROJECT_FILE.search(os.path.basename(str(path))) is not None


def ensure_project_library():
    """Create the fixed Documents/AspenLive/.alp and assets folders."""
    for path in (PROJECTS_ROOT, PROJECTS_ALP_PATH, PROJECTS_ASSETS_PATH):
        os.makedirs(path, exist_ok=True)
    return PROJECTS_ROOT


def project_library_path(name):
    """Absolute .alp path inside the fixed project library."""
    ensure_project_library()
    stem = project_stem(name) or "Untitled Project"
    # Keep filenames filesystem-friendly without changing display names much.
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", stem).strip(" .") or "Untitled Project"
    return os.path.join(PROJECTS_ALP_PATH, safe + PROJECT_EXTENSION)


def list_library_projects():
    """Return [(display_name, alp_path, mtime), ...] newest first."""
    ensure_project_library()
    items = []
    try:
        names = os.listdir(PROJECTS_ALP_PATH)
    except OSError:
        return items
    for filename in names:
        path = os.path.join(PROJECTS_ALP_PATH, filename)
        if not is_project_file(path) or not os.path.isfile(path):
            continue
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = 0.0
        items.append((project_stem(path), path, mtime))
    items.sort(key=lambda row: row[2], reverse=True)
    return items


def project_save_path(path):
    """Return the .alp path for this project inside the fixed library folder."""
    if not path or str(path).startswith("content:"):
        return path
    # Always persist into Documents/AspenLive/.alp — path is not user-configurable.
    return project_library_path(path)


def project_stem(path):
    """Project name without an .alp or .osp extension."""
    name = os.path.basename(str(path or ""))
    match = _PROJECT_FILE.search(name)
    if match:
        return name[:match.start()]
    root, _ext = os.path.splitext(name)
    return root


def is_backup_file(path):
    """True for the current autosave and an autosave left from an older build."""
    if not path:
        return False
    try:
        target = os.path.abspath(str(path))
    except OSError:
        return False
    return target in {os.path.abspath(BACKUP_FILE), os.path.abspath(LEGACY_BACKUP_FILE)}


def pending_backup():
    """Newest unsaved-project backup, preferring neither name over the other."""
    found = [path for path in (BACKUP_FILE, LEGACY_BACKUP_FILE) if os.path.exists(path)]
    if not found:
        return None
    return max(found, key=os.path.getmtime)


def setup_userdirs():
    """Create user paths if they do not exist (this is where
    temp files are stored... such as cached thumbnails)"""
    for folder in _path_defaults.values():
        if not os.path.exists(os.fsencode(folder)):
            os.makedirs(folder, exist_ok=True)
    ensure_project_library()

    # Migrate USER_DEFAULT_PROJECT from former name
    if all([
        os.path.exists(LEGACY_DEFAULT_PROJECT),
        not os.path.exists(USER_DEFAULT_PROJECT),
    ]):
        print("Migrating default project file to new name")
        os.rename(LEGACY_DEFAULT_PROJECT, USER_DEFAULT_PROJECT)


def reset_userdirs():
    """Reset all info.FOO_PATH attributes back to their initial values,
    as they may have been modified by the runtime code (retargeting
    info.THUMBNAIL_PATH to a project assets directory, for example)"""
    for k, v in _path_defaults.items():
        globals()[k] = v


def get_default_path(varname):
    """Return the default value of the named info.FOO_PATH attribute,
    even if it's been modified"""
    return _path_defaults.get(varname, None)


def website_language():
    """Get the current website language code for URLs"""
    return {
        "zh_CN": "zh-hans/",
        "zh_TW": "zh-hant/",
        "en_US": ""}.get(CURRENT_LANGUAGE,
                         "%s/" % CURRENT_LANGUAGE.split("_")[0].lower())
