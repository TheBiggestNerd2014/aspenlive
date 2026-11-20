"""
 @file
 @brief Fixed-library project picker for AspenLive (.alp + assets folders).
"""

import os
from datetime import datetime

from qt_api import (
    Qt, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QFrame, QSizePolicy, QMessageBox, QWidget,
)

from classes import info
from classes.app import get_app


class ProjectLibraryDialog(QDialog):
    """Sleek project chooser bound to Documents/AspenLive."""

    MODE_OPEN = "open"
    MODE_SAVE = "save"
    MODE_START = "start"

    def __init__(self, parent=None, mode=MODE_START, suggested_name=""):
        super().__init__(parent)
        self.mode = mode
        self.selected_path = None
        self._ = get_app()._tr
        info.ensure_project_library()

        self.setObjectName("projectLibraryDialog")
        self.setWindowTitle(self._("Projects"))
        self.setModal(True)
        self.setMinimumSize(520, 460)
        self.resize(560, 520)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 24)
        root.setSpacing(16)

        brand = QLabel("AspenLive")
        brand.setObjectName("projectLibraryBrand")
        brand.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        root.addWidget(brand)

        if mode == self.MODE_SAVE:
            subtitle = self._("Save this project in your AspenLive library.")
        elif mode == self.MODE_OPEN:
            subtitle = self._("Open a project from your AspenLive library.")
        else:
            subtitle = self._("Choose a project to continue, or start something new.")
        hint = QLabel(subtitle)
        hint.setObjectName("projectLibrarySubtitle")
        hint.setWordWrap(True)
        root.addWidget(hint)

        path_row = QHBoxLayout()
        path_label = QLabel(self._("Library"))
        path_label.setObjectName("projectLibraryMeta")
        path_row.addWidget(path_label)
        path_value = QLabel(info.PROJECTS_ROOT)
        path_value.setObjectName("projectLibraryPath")
        path_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        path_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        path_row.addWidget(path_value, 1)
        root.addLayout(path_row)

        if mode == self.MODE_SAVE:
            name_row = QHBoxLayout()
            name_label = QLabel(self._("Name"))
            name_label.setObjectName("projectLibraryMeta")
            name_row.addWidget(name_label)
            self.name_edit = QLineEdit(info.project_stem(suggested_name) or self._("Untitled Project"))
            self.name_edit.setObjectName("projectLibraryName")
            self.name_edit.selectAll()
            name_row.addWidget(self.name_edit, 1)
            root.addLayout(name_row)
        else:
            self.name_edit = None

        self.list = QListWidget()
        self.list.setObjectName("projectLibraryList")
        self.list.setUniformItemSizes(True)
        self.list.itemDoubleClicked.connect(self._accept_selection)
        self.list.itemSelectionChanged.connect(self._sync_buttons)
        root.addWidget(self.list, 1)

        empty = QLabel(self._("No projects yet. Create one to get started."))
        empty.setObjectName("projectLibraryEmpty")
        empty.setAlignment(Qt.AlignCenter)
        empty.setWordWrap(True)
        self.empty_label = empty
        root.addWidget(empty)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("projectLibraryDivider")
        root.addWidget(divider)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        self.btn_new = QPushButton(self._("New Project"))
        self.btn_new.setObjectName("projectLibrarySecondary")
        self.btn_new.clicked.connect(self._new_project)
        buttons.addWidget(self.btn_new)

        buttons.addStretch(1)

        self.btn_cancel = QPushButton(self._("Cancel"))
        self.btn_cancel.setObjectName("projectLibrarySecondary")
        self.btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(self.btn_cancel)

        primary_label = self._("Save") if mode == self.MODE_SAVE else self._("Open")
        if mode == self.MODE_START:
            primary_label = self._("Open Project")
        self.btn_primary = QPushButton(primary_label)
        self.btn_primary.setObjectName("projectLibraryPrimary")
        self.btn_primary.setDefault(True)
        self.btn_primary.clicked.connect(self._accept_primary)
        buttons.addWidget(self.btn_primary)
        root.addLayout(buttons)

        self._reload()
        self._sync_buttons()
        self.setStyleSheet(self._stylesheet())

    def _stylesheet(self):
        return """
        QDialog#projectLibraryDialog {
            background-color: #1a1d21;
            color: #efeae0;
        }
        QLabel#projectLibraryBrand {
            font-family: "Segoe UI Semibold", "Segoe UI", sans-serif;
            font-size: 28px;
            font-weight: 600;
            color: #f3eee4;
            letter-spacing: 0.4px;
        }
        QLabel#projectLibrarySubtitle {
            color: #b7b1a4;
            font-size: 13px;
        }
        QLabel#projectLibraryMeta {
            color: #8f8a7f;
            font-size: 11px;
            min-width: 56px;
        }
        QLabel#projectLibraryPath {
            color: #c4a15a;
            font-size: 12px;
        }
        QLabel#projectLibraryEmpty {
            color: #8f8a7f;
            font-size: 13px;
            padding: 24px;
        }
        QLineEdit#projectLibraryName {
            background: #24282d;
            border: 1px solid #3a3f45;
            border-radius: 8px;
            padding: 8px 12px;
            color: #f3eee4;
            selection-background-color: #c4a15a;
        }
        QListWidget#projectLibraryList {
            background: #14171a;
            border: 1px solid #2e3338;
            border-radius: 10px;
            padding: 6px;
            outline: none;
        }
        QListWidget#projectLibraryList::item {
            padding: 12px 14px;
            margin: 2px 0;
            border-radius: 8px;
            color: #e7e2d6;
        }
        QListWidget#projectLibraryList::item:selected {
            background: rgba(196, 161, 90, 0.22);
            color: #f7f2e8;
        }
        QListWidget#projectLibraryList::item:hover:!selected {
            background: rgba(255, 255, 255, 0.04);
        }
        QFrame#projectLibraryDivider {
            color: #2e3338;
            max-height: 1px;
        }
        QPushButton#projectLibraryPrimary {
            background: #c4a15a;
            color: #1a1d21;
            border: none;
            border-radius: 8px;
            padding: 9px 18px;
            font-weight: 600;
            min-width: 110px;
        }
        QPushButton#projectLibraryPrimary:hover {
            background: #d4b36a;
        }
        QPushButton#projectLibraryPrimary:disabled {
            background: #4a463c;
            color: #9a9488;
        }
        QPushButton#projectLibrarySecondary {
            background: #2a2f34;
            color: #e7e2d6;
            border: 1px solid #3a3f45;
            border-radius: 8px;
            padding: 9px 16px;
            min-width: 96px;
        }
        QPushButton#projectLibrarySecondary:hover {
            background: #343a40;
            border-color: #c4a15a;
        }
        """

    def _reload(self):
        self.list.clear()
        projects = info.list_library_projects()
        for name, path, mtime in projects:
            when = datetime.fromtimestamp(mtime).strftime("%b %d, %Y  %I:%M %p")
            item = QListWidgetItem("%s\n%s" % (name, when))
            item.setData(Qt.UserRole, path)
            item.setToolTip(path)
            self.list.addItem(item)
        has_items = self.list.count() > 0
        self.list.setVisible(has_items)
        self.empty_label.setVisible(not has_items)
        if has_items:
            self.list.setCurrentRow(0)

    def _sync_buttons(self):
        has_selection = bool(self.list.currentItem())
        if self.mode == self.MODE_SAVE:
            name = (self.name_edit.text().strip() if self.name_edit else "")
            self.btn_primary.setEnabled(bool(name))
            self.btn_new.setVisible(False)
        else:
            self.btn_primary.setEnabled(has_selection)
            self.btn_new.setVisible(self.mode in (self.MODE_START, self.MODE_OPEN))

    def _accept_selection(self, *_args):
        item = self.list.currentItem()
        if not item:
            return
        self.selected_path = item.data(Qt.UserRole)
        self.accept()

    def _accept_primary(self):
        if self.mode == self.MODE_SAVE:
            name = self.name_edit.text().strip() if self.name_edit else ""
            if not name:
                return
            path = info.project_library_path(name)
            if os.path.exists(path):
                ret = QMessageBox.question(
                    self,
                    self._("Replace Project?"),
                    self._("A project named \"%s\" already exists. Replace it?") % info.project_stem(path),
                    QMessageBox.Cancel | QMessageBox.Yes,
                )
                if ret != QMessageBox.Yes:
                    return
            self.selected_path = path
            self.accept()
            return
        self._accept_selection()

    def _new_project(self):
        self.selected_path = ""
        self.done(2)  # custom code: new blank project


def prompt_project_library(parent, mode=ProjectLibraryDialog.MODE_START, suggested_name=""):
    """Show the library dialog and return a path, '' for new, or None if cancelled."""
    dialog = ProjectLibraryDialog(parent, mode=mode, suggested_name=suggested_name)
    if dialog.name_edit is not None:
        dialog.name_edit.textChanged.connect(lambda *_: dialog._sync_buttons())
    result = dialog.exec() if hasattr(dialog, "exec") else dialog.exec_()
    if result == 2:
        return ""
    if result:
        return dialog.selected_path
    return None
