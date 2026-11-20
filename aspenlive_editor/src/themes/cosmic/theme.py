"""
 @file
 @brief This file contains a theme's colors and UI dimensions
 @author Jonathan Thomas <jonathan@openshot.org>

 @section LICENSE

 Copyright (c) 2008-2024 OpenShot Studios, LLC
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

from qt_api import Qt
from qt_api import QIcon
from qt_api import QTabWidget, QWidget

from classes.info import PATH
from ..base import BaseTheme


class CosmicTheme(BaseTheme):
    def __init__(self, app):
        super().__init__(app)

        self.style_sheet = """
QToolTip, QLabel#razorHint {
    color: #f4f1ea;
    font-size: 12px;
    font-weight: normal;
    background-color: rgba(40, 50, 65, 230);
    border: 1px solid #6a655c;
    border-radius: 6px;
    margin: 0;
    min-width: 0;
    min-height: 0;
    padding: 2px 4px;
}

QMainWindow {
    background-color: #1c1f22;
    color: #e7e2d6;
}

QWidget#tutorial {
    background-color: #1c1f22;
    border: 1.2px solid #c4a15a;
    border-radius: 4px;
    padding: 20px;
}

QLabel#lblTutorialText {
    font-size: 14px;
}

QCheckBox#checkboxMetrics {
    font-size: 14px;
}

QWidget#tutorial QPushButton#NextTip {
    background-color: #2e3236;
    font-size: 12px;
}

QWidget#tutorial QPushButton#HideTutorial {
    font-size: 12px;
}


QDialog {
    background-color: #1c1f22;
    color: #e7e2d6;
}

QLabel#lblMissingFileHint,
QLabel#lblMissingFilePath {
    color: #c4beb0;
}

QFrame#recordingCard {
    background-color: rgba(20, 31, 48, 190);
    border: 1px solid rgba(70, 134, 230, 110);
    border-radius: 8px;
}
QFrame#recordingCard[checked="true"] {
    border: 2px solid #d4b36a;
    background-color: rgba(26, 58, 105, 170);
}
QFrame#recordingCard[available="false"] {
    border: 1px solid rgba(80, 91, 110, 90);
    background-color: rgba(20, 25, 34, 120);
}
QLabel#recordingCardIcon {
    color: #cfc6b4;
    font-size: 22px;
}
QLabel#recordingCardTitle {
    color: #f4f1ea;
    font-size: 14px;
    font-weight: 700;
}
QLabel#recordingCardSubtitle {
    color: #b7b1a4;
    font-size: 11px;
}
QFrame#recordingSection {
    background-color: rgba(13, 24, 38, 165);
    border: 1px solid rgba(83, 105, 134, 95);
    border-radius: 8px;
}
QFrame#recordingSection[active="true"] {
    border: 1px solid rgba(70, 141, 255, 125);
}
QFrame#recordingSection[active="false"] {
    color: #8e887c;
    background-color: rgba(15, 20, 28, 95);
}
QLabel#recordingSectionIcon {
    color: #d8d0c0;
    font-size: 16px;
}
QLabel#recordingSectionTitle {
    color: #f4f1ea;
    font-weight: 700;
}
QPushButton#recordingAdvancedLink {
    color: #e0c27a;
    border: none;
    padding: 0;
    text-align: right;
}
QPushButton#recordingAdvancedLink:enabled:hover {
    color: #ddd6c8;
    text-decoration: underline;
}
QPushButton#recordingAdvancedLink:disabled {
    color: #9a9488;
    text-decoration: none;
}
QPushButton#recordingSegment {
    border: 1px solid rgba(83, 105, 134, 120);
    border-radius: 6px;
    padding: 7px 10px;
    color: #e4dfd4;
    background-color: rgba(14, 25, 40, 170);
}
QPushButton#recordingSegment[position="left"] {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
}
QPushButton#recordingSegment[position="right"] {
    border-left: none;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
}
QPushButton#recordingSegment:checked {
    color: #d4cbb8;
    border: 1px solid #d4b36a;
    background-color: rgba(40, 94, 170, 135);
}

QWidget#Simple, QWidget#Advanced, QWidget#exportResult, QWidget#PreferencePanel {
    background-color: #16181a;
    border: none;
}

QScrollArea {
    border: none;
}

QTabWidget {
    border: none;
}

QMenuBar {
    background-color: #2e3236;
    color: #e7e2d6;
    padding: 0px;
    border: none;
}

QMenuBar::item {
    padding: 6px 10px;
    background: transparent;
}

QMenuBar::item:selected {
    background-color: #3e4246;
    color: #ffffff;
}

QMenu {
    background-color: #16181a;
    color: #e7e2d6;
    padding: 6px;
    padding-left: 8px;
    padding-right: 8px;
    min-width: 40px;
    border: 1.2px solid #c4a15a;
    border-radius: 3px 3px;
}

QMenu::item {
    padding: 6px 18px 6px 22px;
}

QMenu::item:checked {
    padding: 6px 18px 6px 22px;
}

QMenu::indicator {
    width: 12px;
    height: 12px;
}

QMenu::item:selected:enabled {
    background-color: #1c1f22;
    color: #ffffff;
}

QMenu::item:disabled {
    color: #8a8478;
}

QMenu::separator {
    height: 8px;
    background-color: #16181a;
}

QToolBar#toolBar {
    background-color: #2e3236;
    spacing: 0px;
    padding: 0px;
    border: none;
}

QToolBar#toolBar QToolButton {
    background-color: #2e3236;
    color: #e7e2d6;
    padding-top: 9px;
    padding-bottom: 9px;
    padding-left: 7px;
    padding-right: 7px;
    border: 1px solid transparent;
}

QToolBar#toolBar QToolButton:hover {
    background-color: #3e4246;
}

QToolBar QToolButton:hover,
QDialog#sourcePreviewDialog QToolButton:hover {
    background-color: #1c1f22;
}

QToolBar QToolButton:pressed {
    background-color: #1c1f22;
}

QToolBar#filesToolbar,
QToolBar#transitionsToolbar,
QToolBar#effectsToolbar {
    background-color: transparent;
    spacing: 4px;
    padding: 2px;
    border: none;
}

QToolBar#filesToolbar QToolButton,
QToolBar#transitionsToolbar QToolButton,
QToolBar#effectsToolbar QToolButton {
    background-color: #16181a;
    color: #e7e2d6;
    border-radius: 3px;
    padding: 2px 5px;
    border: 1px solid transparent;
}

QToolBar#filesToolbar QToolButton:hover,
QToolBar#transitionsToolbar QToolButton:hover,
QToolBar#effectsToolbar QToolButton:hover {
    background-color: #1c1f22;
}

QToolBar#filesToolbar QToolButton:checked,
QToolBar#transitionsToolbar QToolButton:checked,
QToolBar#effectsToolbar QToolButton:checked {
    background-color: #282b2e;
}

QToolBar#filesToolbar QToolButton:focus,
QToolBar#transitionsToolbar QToolButton:focus,
QToolBar#effectsToolbar QToolButton:focus {
    border: 1px solid #d8bc82;
    background-color: #222528;
}


QToolBar#timelineToolbar {
    background-color: #1c1f22;
    spacing: 0px;
    padding: 0px;
    border: none;
}

QToolBar#timelineToolbar QToolButton {
    color: #e7e2d6;
    background-color: #16181a;
    padding: 7px;
    margin-bottom: 4px;
    margin-right: 5px;
    margin-left: 5px;
    border-radius: 4px;
    border: 1px solid transparent;
}

QToolBar#timelineToolbar QToolButton:hover {
    background-color: #2e3236;
}


QToolBar#timelineToolbar QToolButton:checked {
    background-color: #2e3236;
}

QToolBar#toolBar QToolButton:focus {
    border: 1px solid #d8bc82;
    background-color: #3a3e42;
}

QToolBar#timelineToolbar QToolButton:focus:!checked {
    border: 1px solid #d8bc82;
    background-color: #16181a;
}

QToolBar#timelineToolbar QToolButton:checked:focus {
    border: 1px solid #d8bc82;
    background-color: #2e3236;
}

QToolBar#timelineToolbar QToolButton:pressed {
    background-color: #52565a;
}

QToolBar#toolBar QToolButton:pressed {
    background-color: #4e5256;
}

QToolBar#filesToolbar QToolButton:pressed,
QToolBar#transitionsToolbar QToolButton:pressed,
QToolBar#effectsToolbar QToolButton:pressed {
    background-color: #34383c;
}

QToolBar#toolBar QToolButton:hover {
    background-color: #3e4246;
}

QToolBar#videoToolbar QToolButton,
QDialog#sourcePreviewDialog QToolButton {
    border: 1px solid transparent;
}

QToolBar#videoToolbar QToolButton:focus,
QDialog#sourcePreviewDialog QToolButton:focus {
    border: 1px solid #d8bc82;
    background-color: #222528;
}

QToolBar#videoToolbar QToolButton:pressed,
QDialog#sourcePreviewDialog QToolButton:pressed {
    background-color: #34383c;
}

QFrame#textStyleBar {
    background-color: rgba(25, 35, 50, 238);
    border: 1px solid rgba(83, 105, 134, 150);
    border-radius: 8px;
    qproperty-iconColor: #e7e2d6;
}
QFrame#textStyleBar QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 3px;
}
QFrame#textStyleBar QToolButton:hover {
    background-color: #2e3236;
}
QFrame#textStyleBar QToolButton:checked {
    background-color: rgba(40, 94, 170, 150);
    border: 1px solid #d4b36a;
}
QFrame#textStyleBar QComboBox,
QFrame#textStyleBar QSpinBox {
    background-color: #121212;
    border-radius: 4px;
    padding: 3px 6px;
    min-height: 18px;
}
QFrame#textStyleBar QSpinBox {
    padding-right: 20px;
}
QFrame#textStyleDivider {
    background-color: rgba(83, 105, 134, 150);
    border: none;
}

QDialog#textStyleDialog {
    background-color: #1c1f22;
}
QDialog#textStyleDialog QLabel {
    color: #e7e2d6;
    background-color: transparent;
}
QDialog#textStyleDialog QLabel#textStylePreview {
    background-color: #000000;
    border: 1px solid #2e3236;
    border-radius: 6px;
}
QFrame#textStyleSection {
    background-color: #16181a;
    border: 1px solid #2c2f32;
    border-radius: 8px;
}
QDialog#textStyleDialog QLabel#textStyleHeading {
    color: #f7f4ee;
    font-weight: 700;
}
QFrame#textStyleRule {
    background-color: #2e3236;
    border: none;
}
QPlainTextEdit#textStyleEditor {
    background-color: #121212;
    color: #f7f4ee;
    border: 1px solid #2e3236;
    border-radius: 6px;
    padding: 1px 4px;
}
QPlainTextEdit#textStyleEditor:focus {
    border-color: #c9a86a;
}
QPlainTextEdit#textStyleEditor:disabled {
    color: #e7e2d6;
}
QAbstractSpinBox#textStyleSpin {
    background-color: #121212;
    color: #f7f4ee;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 3px 22px 3px 8px;
}
QAbstractSpinBox#textStyleSpin:focus {
    border-color: #c9a86a;
}
QAbstractSpinBox#textStyleSpin::up-arrow,
QAbstractSpinBox#textStyleSpin::down-arrow {
    width: 15px;
    height: 15px;
}
QToolButton#textStyleSwatch {
    background-color: #121212;
    border: 1px solid #2e3236;
    border-radius: 4px;
    padding: 0px;
}
QToolButton#textStyleSwatch:hover {
    border-color: #c9a86a;
}
QPushButton#textStyleLink {
    background-color: transparent;
    color: #e7e2d6;
    border: none;
    padding: 8px 6px;
}
QPushButton#textStyleLink:hover,
QPushButton#textStyleLink:focus {
    color: #ffffff;
    background-color: transparent;
}
QDialog#textStyleDialog QPushButton#acceptButton {
    padding: 8px 20px;
}

QPushButton#acceptButton,
QDialog#sourcePreviewDialog QPushButton[dialogRole="primary"]:enabled,
QWidget#exportResult QPushButton[dialogRole="primary"]:enabled {
    padding: 8px 16px 8px 12px;
    border-radius: 4px;
    background-color: #c4a15a;
    color: #FFFFFF;
}

QPushButton#acceptButton:hover,
QDialog#sourcePreviewDialog QPushButton[dialogRole="primary"]:enabled:hover,
QWidget#exportResult QPushButton[dialogRole="primary"]:enabled:hover {
    background-color: #b08d45;
}

QPushButton#acceptButton:focus,
QPushButton#acceptButton:default,
QDialog#sourcePreviewDialog QPushButton[dialogRole="primary"]:enabled:focus,
QWidget#exportResult QPushButton[dialogRole="primary"]:enabled:focus {
    background-color: #d4b36a;
}

QPushButton {
    padding: 8px 16px 8px 12px;
    border-radius: 4px;
    background-color: #1c1f22;
    color: #e7e2d6;
}

QPushButton:hover {
    background-color: #2e3236;
}

QPushButton:focus {
    background-color: #2e3236;
}

QDialog#animatedTitle QPushButton:disabled,
QDialog#animatedTitle QPushButton#acceptButton:disabled,
QDialog#exportDialog QPushButton#acceptButton:disabled {
    background-color: #26292c;
    color: #7a756c;
}

QDialog#animatedTitle QPushButton#cancelButton {
    background-color: #2e3236;
}

QDialog#animatedTitle QPushButton#cancelButton:enabled:hover {
    background-color: #4a4e52;
}

QDialog#animatedTitle QPushButton#cancelButton:enabled:pressed {
    background-color: #5c6058;
}

QWidget#settingsContainer {
    background-color: #16181a;
}

QWidget#scrollAreaWidgetContents {
    background-color: #16181a;
}

QPushButton#dock-close-button {
    image: url({PATH}themes/cosmic/images/dock-close.svg);
    padding: 0px;
    padding-top: 2px;
    padding-bottom: 2px;
    margin: 0px;
    margin-right: 16px;
    width: 16px;
    height: 16px;
}
QPushButton#dock-float-button {
    image: url({PATH}themes/cosmic/images/dock-float.svg);
    padding: 0px;
    padding-top: 2px;
    padding-bottom: 2px;
    margin: 0px;
    width: 16px;
    height: 16px;
}

QPushButton#dock-close-button,
QPushButton#dock-float-button {
    border: 1px solid transparent;
    background: transparent;
}

QPushButton#dock-close-button:hover,
QPushButton#dock-float-button:hover,
QPushButton#dock-close-button:pressed,
QPushButton#dock-float-button:pressed,
QPushButton#dock-close-button:focus,
QPushButton#dock-float-button:focus {
    background: transparent;
}

QPushButton#dock-close-button:focus,
QPushButton#dock-float-button:focus {
    border: 1px solid #d8bc82;
    outline: none;
}

QLabel#dock-title-label {
    color: #e7e2d6;
    font-weight: 500;
    min-height: 20px;
    padding: 9px 0px 0px 0px;
    margin: 0px 16px 8px 16px;
    border-bottom: 1px solid transparent;
}

QLabel#dock-title-handle {
    padding-left: 16px;
    qproperty-pixmap: url({PATH}themes/cosmic/images/dock-move.svg);
}

QDockWidget {
    background-color: #16181a;
    titlebar-close-icon: url({PATH}themes/cosmic/images/dock-close.svg);
    titlebar-normal-icon: url({PATH}themes/cosmic/images/dock-float.svg);
    color: #e7e2d6;
    font-weight: 500;
    padding: 16px;
}

QDockWidget QWidget {
    border: none;
}

QLabel#dock-title-label[focusWithin="true"] {
    border-bottom: 1px solid #d8bc82;
}

QTabBar[dockFocusTabs="true"]::tab {
    border-bottom: 1px solid transparent;
}

QTabBar[dockFocusTabs="true"]::tab:focus,
QTabBar[dockFocusTabs="true"][focusWithin="true"]::tab:selected {
    border-bottom: 1px solid #d8bc82;
}

QDockWidget QWidget#dockFilesContents, QWidget#dockTransitionsContents, QWidget#dockEmojisContents, QWidget#dockEffectsContents, QWidget#dockCaptionContents, QWidget#dockVideoContents, QWidget#dockPropertiesContents {
    background-color: #16181a;
    border-radius: 8px;
    margin-left: 16px;
    margin-right: 16px;
}

QListView, QTreeView, QTableView {
    background-color: #14171a;
    border: 1px solid #2a2f34;
    border-radius: 8px;
    outline: none;
    padding: 2px;
}

QListView::item:selected, QTreeView::item:selected, QTableView::item:selected {
    background: rgba(196, 161, 90, 0.20);
    color: #f7f2e8;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #3a3f45;
    border-radius: 5px;
    min-height: 28px;
}
QScrollBar::handle:vertical:hover {
    background: #c4a15a;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QDockWidget QWidget#dockGpuInspectorContents {
    background-color: #16181a;
    border-radius: 4px;
}

QDockWidget QWidget#dockTimelineContents {
    border-radius: 0px;
    margin-left: 0px;
    margin-right: 0px;
    padding: 0px;
}

QTabBar {
    border: none;
    qproperty-drawBase: 0;
    qproperty-expanding: 0;
    qproperty-usesScrollButtons: 1;
    margin: 0px;
    padding: 0px;
}

QTabBar::tab {
    height: 16px;
    border: none;
    margin-left: 16px;
    margin-top: 16px;
    margin-bottom: 0px;
    padding-bottom: 0px;
    color: rgba(183, 177, 164, 0.72);
}

QTabWidget#exportTabs QTabBar::tab,
QTabWidget#tabCategories QTabBar::tab,
QTabWidget#tabCredits QTabBar::tab,
QTabWidget#generateTabs QTabBar::tab {
    margin-bottom: 10px;
}

/* Keep the export dialog's name/folder rows and tabs compact. */
QTabWidget#exportTabs QTabBar::tab {
    margin-top: 4px;
}

QDialog#exportDialog QPushButton#btnBrowse {
    padding-top: 2px;
    padding-bottom: 2px;
}

QTabWidget#generateTabs QTabBar::tab:selected {
    border-bottom: 1.2px solid #c9a86a;
}

QTabBar::tab:selected {
    color: #d4b36a;
}

QTabBar:focus {
    outline: none;
}

QTabBar::tab:focus {
    border-bottom: 1.2px solid #c9a86a;
}

QToolBox::tab:focus {
    border-left: 1.2px solid #c9a86a;
}

QCheckBox:focus {
    background-color: #2e3236;
}

QLineEdit#filesFilter, QLineEdit#effectsFilter, QLineEdit#transitionsFilter, QLineEdit#emojisFilter, QLineEdit#txtPropertyFilter {
    background-color: #1c1f22;
    border-radius: 4px;
    padding: 6px;
    padding-left: 8px;
    padding-right: 8px;
}

QLineEdit,
QSpinBox,
QDoubleSpinBox {
    background-color: #121212;
    border: 1.2px solid transparent;
    border-radius: 4px;
    padding-top: 1px;
    padding-bottom: 1px;
    padding-left: 6px;
    min-height: 18px;
}

QSpinBox,
QDoubleSpinBox {
    padding-right: 22px;
}

QDoubleSpinBox#colorGradeSpinBox {
    padding-right: 14px;
}

QSpinBox::up-button,
QDoubleSpinBox::up-button,
QSpinBox::down-button,
QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    width: 16px;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 3px;
    margin-right: 2px;
}

QSpinBox::up-button,
QDoubleSpinBox::up-button {
    subcontrol-position: top right;
    margin-top: 1px;
    margin-bottom: 0px;
    min-height: 7px;
}

QSpinBox::down-button,
QDoubleSpinBox::down-button {
    subcontrol-position: bottom right;
    margin-top: 0px;
    margin-bottom: 1px;
    min-height: 7px;
}

QSpinBox::up-button:hover,
QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover,
QDoubleSpinBox::down-button:hover {
    background-color: rgba(196, 161, 90, 0.12);
    border-color: rgba(196, 161, 90, 0.4);
}

QSpinBox::up-button:pressed,
QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed,
QDoubleSpinBox::down-button:pressed {
    background-color: rgba(196, 161, 90, 0.22);
    border-color: rgba(196, 161, 90, 0.6);
}

QSpinBox::up-arrow,
QDoubleSpinBox::up-arrow {
    image: url({PATH}themes/cosmic/images/spin-up-arrow.svg);
    width: 12px;
    height: 12px;
}

QSpinBox::down-arrow,
QDoubleSpinBox::down-arrow {
    image: url({PATH}themes/cosmic/images/spin-down-arrow.svg);
    width: 12px;
    height: 12px;
}

QLineEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus {
    border-width: 1.2px;
    border-style: solid;
    border-color: #c9a86a;
}

QLineEdit#filesFilter:focus, QLineEdit#effectsFilter:focus, QLineEdit#transitionsFilter:focus, QLineEdit#emojisFilter:focus, QLineEdit#txtPropertyFilter:focus {
    border-width: 1.2px;
    border-style: solid;
    border-color: #c9a86a;
}

QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: rgba(138, 132, 120, 170);
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
    border: none;
    background: transparent;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: rgba(138, 132, 120, 170);
    border-radius: 4px;
    min-width: 20px;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
    border: none;
    background: transparent;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
}

QComboBox, QDockWidget QComboBox {
    background-color: #121212;
    color: #FFFFFF;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 6px;
    padding-left: 8px;
    padding-right: 8px;
    combobox-popup: 0;
}

QComboBox:focus, QDockWidget QComboBox:focus {
    border: 1px solid #d8bc82;
    outline: none;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 40px;
    border: none;
}

QComboBox::down-arrow {
    image: url({PATH}themes/cosmic/images/dropdown-arrow.svg);
}

QComboBox QAbstractItemView {
    color: #FFFFFF;
    border: 1.2px solid #c4a15a;
    border-radius: 3px 3px 0px 0px;
    padding: 6px;
    padding-left: 8px;
    padding-right: 8px;
    background-color: #16181a;
    text-align: left;
}

QComboBox::item {
    height: 24px;
}

QComboBox::item:selected {
    border: none;
    text-align: left;
    background-color: #1c1f22;
}

QComboBox::item:checked {
    font-weight: bold;
    background-color: #1c1f22;
}

QComboBox::indicator::checked {
    image: url({PATH}themes/cosmic/images/dropdown-tick.svg);
}

QHeaderView::section {
    background-color: #16181a;
    color: #e7e2d6;
    padding: 4px;
    border: none;
}

QTableView {
    background-color: #16181a;
    gridline-color: #16181a;
}

QTableView#propertyTableView::item:selected {
    background-color: #1c1f22;
    border: 1.2px solid #c4a15a;
}

QTreeView {
    background-color: #16181a;
}

QListView {
    background-color: #16181a;
}

QWidget#Details, QWidget#Output {
    background-color: #16181a;
}

QWidget#Output QTextEdit {
    color: #e7e2d6;
}

QToolBox::tab {
    color: #e7e2d6;
    border-top: 1px solid rgba(106, 101, 92, 0.55);
}

QTabWidget QWidget#pageAdvancedOptions, QWidget#pageProfile, QWidget#pageImageSequenceSettings, QWidget#pageVideoSettings, QWidget#pageAudioSettings {
    background-color: #16181a;
}

QTabWidget QWidget#pageVideoDetails, QWidget#pageVideoFormat, QWidget#pageAudioFormat, QWidget#pageFrameSettings {
    background-color: #16181a;
}

QDialog#generateDialog QTabWidget#generateTabs::pane {
    border: none;
    background-color: #16181a;
}

QDialog#generateDialog QTabWidget#generateTabs QWidget#pagePrompt,
QDialog#generateDialog QTabWidget#generateTabs QWidget#pagePoints,
QDialog#generateDialog QTabWidget#generateTabs QWidget#pageHighlight {
    background-color: #16181a;
    border: none;
}

QDialog#generateDialog QLineEdit,
QDialog#generateDialog QTextEdit,
QDialog#generateDialog QComboBox {
    background-color: #16181a;
    color: #e7e2d6;
    border: 1.2px solid transparent;
    border-radius: 4px;
    padding: 6px 8px;
}

QDialog#generateDialog QLineEdit:focus,
QDialog#generateDialog QTextEdit:focus,
QDialog#generateDialog QComboBox:focus {
    border: 1.2px solid #c9a86a;
}

QLineEdit:disabled,
QTextEdit:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled {
    color: #808080;
}

QComboBox:disabled::drop-down {
    opacity: 0.75;
}

QWidget#cutting QPushButton#btnStart,QPushButton#btnEnd  {
    border: 1px solid #b08d45;
}

QWidget#cutting QPushButton#btnStart:disabled,QPushButton#btnEnd:disabled {
    color: #666666;
    border: 1px solid #666666;
}

QWidget#cutting QPushButton#btnAddClip {
    background-color: #b08d45;
    color: #FFFFFF;
}

QWidget#cutting QPushButton#btnAddClip:disabled,
QDialog#sourcePreviewDialog QPushButton[dialogRole="primary"]:disabled {
    background-color: #2e3236;
    color: #666666;
}

.property_value {
    foreground-color: #c4a15a;
    background-color: #2e3236;
}

.zoom_slider_playhead {
    background-color: #FABE0A;
}

QWidget#videoPreview {
    background-color: #16181a;
}
        """
        path_unix_slashes = PATH.replace("\\", "/")
        self.style_sheet = f"""
QMessageBox {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #24272a,
        stop: 0.55 #1a1d20,
        stop: 1 #141618
    );
    border: 1px solid #5a564c;
}}
QMessageBox QLabel#qt_msgbox_label {{
    color: #f4f1ea;
    font-size: 12px;
}}
QMessageBox QPushButton[dialogRole="primary"] {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #c4a15a,
        stop: 1 #a6853e
    );
    color: #1c1f22;
    border: 1px solid #e0c27a;
}}
QMessageBox QPushButton[dialogRole="primary"]:hover {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #d4b36a,
        stop: 1 #b8944c
    );
}}
QMessageBox QPushButton[dialogRole="secondary"] {{
    color: #ddd6c8;
    background-color: #2e3236;
    border: 1px solid #565a52;
}}
QMessageBox QPushButton[dialogRole="secondary"]:hover {{
    background-color: #45494d;
    border-color: #6a655c;
}}
QMessageBox QPushButton[dialogRole="cancel"] {{
    color: #cfc6b4;
}}
QMessageBox QPushButton[dialogRole="cancel"]:hover {{
    color: #ddd6c8;
    background-color: #2e3236;
}}
QMessageBox QPushButton[dialogRole="destructive"] {{
    color: #ffffff;
    background-color: #c43d4b;
    border: 1px solid #df5361;
}}
        """ + self.style_sheet.replace("{PATH}", f"{path_unix_slashes}/")

    def apply_theme(self):
        super().apply_theme()

        from classes.app import get_app
        from classes import ui_util
        from classes.logger import log
        from qt_api import QStyleFactory
        from qt_api import QFont

        _ = get_app()._tr

        log.info("Setting Fusion dark palette")
        self.app.setStyle(QStyleFactory.create("Fusion"))
        from qt_api import QColor, QPalette
        dark_palette = ui_util.make_dark_palette(self.app.palette())
        dark_palette.setColor(QPalette.Window, QColor("#1c1f22"))
        dark_palette.setColor(QPalette.WindowText, QColor("#f4f1ea"))
        dark_palette.setColor(QPalette.Base, QColor("#16181a"))
        dark_palette.setColor(QPalette.AlternateBase, QColor("#24272a"))
        dark_palette.setColor(QPalette.Text, QColor("#f4f1ea"))
        dark_palette.setColor(QPalette.Button, QColor("#2e3236"))
        dark_palette.setColor(QPalette.ButtonText, QColor("#f4f1ea"))
        dark_palette.setColor(QPalette.Highlight, QColor(196, 161, 90, 210))
        dark_palette.setColor(QPalette.HighlightedText, QColor("#1c1f22"))
        dark_palette.setColor(QPalette.Link, QColor("#d4b36a"))
        dark_palette.setColor(QPalette.LinkVisited, QColor("#b08d45"))
        dark_palette.setColor(QPalette.ToolTipBase, QColor("#2e3236"))
        dark_palette.setColor(QPalette.ToolTipText, QColor("#f4f1ea"))
        self.app.setPalette(dark_palette)

        icon_path = os.path.join(PATH, "images", "aspenlive.png")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.app.setWindowIcon(icon)
            if self.app.window:
                self.app.window.setWindowIcon(icon)

        # Segoe UI is the Windows face; Ubuntu is not installed here.
        font = QFont("Segoe UI")
        font.setPointSizeF(9)
        self.app.setFont(font)

        # Move tabs to top (all dock areas, since restoreState() does not persist tab positions)
        for area in (Qt.TopDockWidgetArea, Qt.BottomDockWidgetArea,
                     Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea):
            self.app.window.setTabPosition(area, QTabWidget.North)

        # Set dock widget content margins to 0
        self.set_dock_margins([16, 0, 16, 0])
        self.set_dock_margins([0, 0, 0, 0], [0, 10, 0, 0], "dockTimelineContents")

        # Apply new stylesheet
        self.app.setStyleSheet(self.compose_stylesheet())

        # Create a transparent spacer widget
        spacer = QWidget(self.app.window)
        spacer.setFixedSize(15, 1)
        spacer.setStyleSheet("background: transparent;")

        # Main toolbar buttons
        toolbar_buttons = [
            {"action": self.app.window.actionNew, "icon": "themes/cosmic/images/tool-new-project.svg", "style": Qt.ToolButtonTextBesideIcon},
            {"action": self.app.window.actionOpen, "icon": "themes/cosmic/images/tool-open-project.svg", "style": Qt.ToolButtonTextBesideIcon},
            {"action": self.app.window.actionImportFiles, "icon": "themes/cosmic/images/tool-import-files.svg", "style": Qt.ToolButtonTextBesideIcon},
            {"action": self.app.window.actionProfile, "icon": "themes/cosmic/images/tool-profile.svg", "style": Qt.ToolButtonTextBesideIcon},
            {"expand": True},
            {"action": self.app.window.actionSave, "icon": "themes/cosmic/images/tool-save-project.svg", "style": Qt.ToolButtonTextBesideIcon},
            {"action": self.app.window.actionExportVideo, "icon": "themes/cosmic/images/tool-export.svg",
             "style": Qt.ToolButtonTextBesideIcon, "stylesheet": "QToolButton { background-color: #c4a15a; color: #1c1f22; border: 1px solid transparent; } QToolButton:hover { background-color: #d4b36a; } QToolButton:focus { background-color: #d4b36a; border: 1px solid #d8bc82; } QToolButton:pressed { background-color: #e8d09a; }"},
        ]
        self.set_toolbar_buttons(self.app.window.toolBar, icon_size=20, settings=toolbar_buttons)

        self.app.window.actionColor_Grade_View.setIcon(
            QIcon(os.path.join(PATH, "themes/cosmic/images/view-color.svg"))
        )

        # Timeline toolbar buttons
        timeline_buttons = [
            {"action": self.app.window.actionAddTrack, "icon": "themes/cosmic/images/tool-add-track.svg", "style": Qt.ToolButtonTextBesideIcon, "stylesheet": "QToolButton { margin-left: 15px; }"},
            {"action": self.app.window.actionUndo, "icon": "themes/cosmic/images/tool-undo.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-right: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionRedo, "icon": "themes/cosmic/images/tool-redo.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; }"},
            {"action": self.app.window.actionSnappingTool, "icon": "themes/cosmic/images/tool-snapping.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-right: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionAutoKeyframes, "icon": "themes/cosmic/images/tool-auto-keyframes.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; margin-right: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionTimingTool, "icon": "themes/cosmic/images/tool-timing.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; margin-right: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionRazorTool, "icon": "themes/cosmic/images/tool-razor.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; margin-right: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionDirectText, "icon": "images/tool-text.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; }"},
            {"action": self.app.window.actionAddMarker, "icon": "themes/cosmic/images/tool-add-marker.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-right: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionPreviousMarker, "icon": "themes/cosmic/images/tool-prev-marker.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; margin-right: 0px; border-bottom-right-radius: 0px; border-top-right-radius: 0px; }"},
            {"action": self.app.window.actionNextMarker, "icon": "themes/cosmic/images/tool-next-marker.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QToolButton { margin-left: 0px; border-bottom-left-radius: 0px; border-top-left-radius: 0px; }"},
            {"action": self.app.window.actionCenterOnPlayhead, "icon": "themes/cosmic/images/tool-center-playhead.svg", "style": Qt.ToolButtonIconOnly, "stylesheet": "QWidget { margin-right: 10px; }"},
            {"widget": self.app.window.sliderZoomWidget},
            {"widget": spacer}
        ]
        self.set_toolbar_buttons(self.app.window.timelineToolbar, icon_size=12, settings=timeline_buttons)

        # Video toolbar
        toolbar_buttons = [
            {"expand": True},
            {"action": self.app.window.actionJumpStart, "icon": "themes/cosmic/images/tool-media-skip-back.svg", "style": Qt.ToolButtonIconOnly},
            {"action": self.app.window.actionRewind, "icon": "themes/cosmic/images/tool-media-rewind.svg", "style": Qt.ToolButtonIconOnly},
            {"action": self.app.window.actionPlay, "icon": "themes/cosmic/images/tool-media-play.svg", "style": Qt.ToolButtonIconOnly},
            {"action": self.app.window.actionFastForward, "icon": "themes/cosmic/images/tool-media-forward.svg", "style": Qt.ToolButtonIconOnly},
            {"action": self.app.window.actionJumpEnd, "icon": "themes/cosmic/images/tool-media-skip-forward.svg", "style": Qt.ToolButtonIconOnly},
            {"expand": True}
        ]
        self.set_toolbar_buttons(self.app.window.videoToolbar, icon_size=32, settings=toolbar_buttons)

        from .styles import CosmicDuskTimelineTheme
        self.app.window.timeline.apply_theme(CosmicDuskTimelineTheme())

        # Emit signal
        self.app.window.ThemeChangedSignal.emit(self)

    def togglePlayIcon(self, isPlay):
        """ Toggle the play icon from play to pause and back """
        self._update_play_action_text(isPlay)
        button = self.app.window.videoToolbar.widgetForAction(self.app.window.actionPlay)
        if button:
            icon_name = "tool-media-pause.svg" if isPlay else "tool-media-play.svg"
            icon_path = os.path.join(PATH, "themes/cosmic/images", icon_name)
            icon = self.create_svg_icon(icon_path, self.app.window.videoToolbar.iconSize())
            button.setIcon(icon)
