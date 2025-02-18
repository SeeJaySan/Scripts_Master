from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds

from PySide2.QtWidgets import (
    QApplication, QWidget, QPushButton, QCheckBox, QLineEdit, QSlider, QRadioButton, 
    QButtonGroup, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QComboBox, QSpinBox, 
    QSizePolicy, QTabWidget
)
from PySide2.QtCore import Qt

import time
from msc.modules import Utils_JointCreateAndOrientatorModule as jCO


def print_widget_name(widget_name):
    """Helper function to print the name of interacted widgets."""
    print(f"Widget '{widget_name}' was interacted with.")


def get_maya_main_window():
    """Returns the main Maya window as a QWidget instance."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class QuickToolsWindow(MayaQWidgetDockableMixin, QWidget):
    """Main UI class for RigMaster, containing tool tabs and layouts."""

    def __init__(self, parent=None):
        super(QuickToolsWindow, self).__init__(parent=parent)
        self.setWindowTitle("RigMaster")
        self.setObjectName("RigMasterWindow")

        # Initialize the joint module
        self.joint_module = jCO.jointCreateAndOrientator()

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create and add tab widget
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)

        # Create first tab (Quick Tools)
        first_tab = QWidget()
        first_tab.setLayout(self.create_first_tab())
        self.tabs.addTab(first_tab, "Quick Tools")

        # Create second tab
        second_tab = QWidget()
        second_tab.setLayout(self.create_second_tab())
        self.tabs.addTab(second_tab, "Second Tab")

        # Set main layout
        self.setLayout(main_layout)

    def create_first_tab(self):
        """Creates layout for the Quick Tools tab."""
        layout = QVBoxLayout()

        # Add joint axis visibility buttons
        layout.addLayout(self.create_joint_axis_widget())

        # Add create and aim joint buttons
        layout.addLayout(self.create_create_aim_widgets())

        # Add axis radio button groups
        layout.addWidget(self.create_axis_radio_group("Aim"))
        layout.addWidget(self.create_axis_radio_group("Up"))

        # Add orient joints button
        layout.addLayout(self.create_orient_joints_widget())

        # Additional UI elements (Slider, ComboBox, SpinBox, Label)
        layout.addLayout(self.create_slider_widget())
        layout.addLayout(self.create_combo_box_widget())
        layout.addLayout(self.create_spin_box_widget())
        layout.addLayout(self.create_label_widget())

        return layout

    def create_second_tab(self):
        """Creates layout for the second tab."""
        layout = QVBoxLayout()

        # Add rename widgets
        sr_rename_wdgt, ps_rename_wdgt = self.create_rename_widgets()
        layout.addLayout(sr_rename_wdgt)
        layout.addLayout(ps_rename_wdgt)

        # Add placeholder label and button
        label = QLabel("This is the second tab")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button = QPushButton("Button in Second Tab")
        button.clicked.connect(lambda: print_widget_name("Second Tab Button"))
        layout.addWidget(button)

        return layout

    def create_joint_axis_widget(self):
        """Creates widget for controlling joint axis visibility."""
        layout = QHBoxLayout()
        show_axis_btn = QPushButton("Show Axis")
        hide_axis_btn = QPushButton("Hide Axis")
        show_axis_btn.clicked.connect(self.joint_module.turnOnJointAxisVis)
        hide_axis_btn.clicked.connect(self.joint_module.turnOffJointAxisVis)
        layout.addWidget(show_axis_btn)
        layout.addWidget(hide_axis_btn)
        return layout

    def create_create_aim_widgets(self):
        """Creates widget for creating and aiming joints."""
        layout = QHBoxLayout()
        create_jnt_btn = QPushButton("Joint at component")
        aim_jnt_btn = QPushButton("Aim at component")
        create_jnt_btn.clicked.connect(self.joint_module.createBaseJoint)
        aim_jnt_btn.clicked.connect(self.joint_module.endBaseJoint)
        layout.addWidget(create_jnt_btn)
        layout.addWidget(aim_jnt_btn)
        return layout

    def create_axis_radio_group(self, label):
        """Creates a group box with radio buttons for axis selection."""
        group_box = QGroupBox(label)
        layout = QHBoxLayout()
        for axis in ["X", "Y", "Z"]:
            layout.addWidget(QRadioButton(axis))
        group_box.setLayout(layout)
        return group_box

    def create_orient_joints_widget(self):
        """Creates a button to orient joints."""
        layout = QHBoxLayout()
        layout.addWidget(QPushButton("Orient Joints"))
        return layout

    def create_rename_widgets(self):
        """Creates widgets for renaming tools (search/replace & prefix/suffix)."""
        sr_layout = QHBoxLayout()
        sr_layout.addWidget(QLabel("Search"))
        sr_layout.addWidget(QLineEdit())
        sr_layout.addWidget(QLabel("Replace"))
        sr_layout.addWidget(QLineEdit())

        ps_layout = QHBoxLayout()
        ps_layout.addWidget(QLabel("Prefix"))
        ps_layout.addWidget(QLineEdit())
        ps_layout.addWidget(QLabel("Suffix"))
        ps_layout.addWidget(QLineEdit())

        return sr_layout, ps_layout

    def create_slider_widget(self):
        """Creates a slider widget."""
        layout = QVBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(lambda: print_widget_name('QSlider'))
        layout.addWidget(slider)
        return layout

    def create_combo_box_widget(self):
        """Creates a combo box widget."""
        layout = QVBoxLayout()
        combo_box = QComboBox()
        combo_box.addItems(["Choice 1", "Choice 2", "Choice 3"])
        combo_box.currentIndexChanged.connect(lambda: print_widget_name('QComboBox'))
        layout.addWidget(combo_box)
        return layout

    def create_spin_box_widget(self):
        """Creates a spin box widget."""
        layout = QVBoxLayout()
        spin_box = QSpinBox()
        spin_box.valueChanged.connect(lambda: print_widget_name('QSpinBox'))
        layout.addWidget(spin_box)
        return layout

    def create_label_widget(self):
        """Creates a label widget."""
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is a label"))
        return layout


def show_dockable_widget():
    """Shows the dockable QuickToolsWindow in Maya."""
    global tm_tab_window
    try:
        if tm_tab_window:
            tm_tab_window.close()
            tm_tab_window.deleteLater()
            tm_tab_window = None
    except Exception as e:
        print(f"Error deleting UI: {e}")

    tm_tab_window = QuickToolsWindow()
    tm_tab_window.show()


# Execute the show function
show_dockable_widget()
