from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QSlider,
    QRadioButton,
    QButtonGroup,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QSpinBox,
    QSizePolicy,
    QTabWidget,
)
from PySide2.QtCore import Qt
import time

#================================================================

# Creating Widgets

#================================================================

from msc.modules import Utils_JointCreateAndOrientatorModule as jCO


def print_widget_name(widget_name):
    print(f"Widget '{widget_name}' was interacted with.")


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class QuickToolsWindow(MayaQWidgetDockableMixin, QWidget):
    def __init__(self, parent=None):
        super(QuickToolsWindow, self).__init__(parent=parent)
        self.setWindowTitle("RigMaster")
        self.setObjectName("RigMasterWindow")

        # Initialize the joint module
        self.joint_module = jCO.jointCreateAndOrientator()

        # Create the main layout and the tab widget
        main_layout = QVBoxLayout(self)

        # Create tab widget
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)

        # Create widgets for the first tab
        first_tab = QWidget()
        first_tab_layout = self.create_first_tab()
        first_tab.setLayout(first_tab_layout)

        # Create widgets for the second tab
        second_tab = QWidget()
        second_tab_layout = self.create_second_tab()
        second_tab.setLayout(second_tab_layout)

        # Add tabs to the tab widget
        self.tabs.addTab(first_tab, "Quick Tools")
        self.tabs.addTab(second_tab, "Second Tab")

        # Set main layout to the window
        self.setLayout(main_layout)

    def create_first_tab(self):
        """Create layout for the first tab (Quick Tools)."""
        layout = QVBoxLayout()

        # Add widgets for the first tab here (same as current QuickToolsWindow layout)
        joint_axis_wdgt = self.create_joint_axis_widget()
        layout.addLayout(joint_axis_wdgt)

        create_aim_wdgt = self.create_create_aim_widgets()
        layout.addLayout(create_aim_wdgt)

        aim_radio_buttons_wdgt = self.create_axis_radio_group("Aim")
        layout.addWidget(aim_radio_buttons_wdgt)

        up_radio_buttons_wdgt = self.create_axis_radio_group("Up")
        layout.addWidget(up_radio_buttons_wdgt)

        orient_joints_wdgt = self.create_orient_joints_widget()
        layout.addLayout(orient_joints_wdgt)

        layout4 = self.create_slider_widget()
        layout.addLayout(layout4)

        layout6 = self.create_combo_box_widget()
        layout.addLayout(layout6)

        layout7 = self.create_spin_box_widget()
        layout.addLayout(layout7)

        layout8 = self.create_label_widget()
        layout.addLayout(layout8)

        return layout

    def create_second_tab(self):
        """Create layout for the second tab."""
        layout = QVBoxLayout()

        sr_rename_wdgt, ps_rename_wdgt = self.create_rename_widgets()
        layout.addLayout(sr_rename_wdgt)
        layout.addLayout(ps_rename_wdgt)

        # Add some placeholder widgets or tools for the second tab
        label = QLabel("This is the second tab")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # You can add more tools or functionality for the second tab here
        button = QPushButton("Button in Second Tab")
        button.clicked.connect(lambda: print_widget_name("Second Tab Button"))
        layout.addWidget(button)

        return layout

    # ================================================================

    # Creating Widgets

    # ================================================================

    def create_joint_axis_widget(self):
        """Widget for controlling joint axis visibility."""
        joint_axis_wdgt = QHBoxLayout(self)
        show_axis_btn = QPushButton("Show Axis")
        hide_axis_btn = QPushButton("Hide Axis")
        show_axis_btn.clicked.connect(self.joint_module.turnOnJointAxisVis)
        hide_axis_btn.clicked.connect(self.joint_module.turnOffJointAxisVis)
        joint_axis_wdgt.addWidget(show_axis_btn)
        joint_axis_wdgt.addWidget(hide_axis_btn)
        return joint_axis_wdgt

    def create_create_aim_widgets(self):
        """Widget for creating and aiming joints."""
        create_aim_wdgt = QHBoxLayout(self)
        create_jnt_btn = QPushButton("Joint at component")
        aim_jnt_btn = QPushButton("Aim at component")
        create_jnt_btn.clicked.connect(self.joint_module.createBaseJoint)
        aim_jnt_btn.clicked.connect(self.joint_module.endBaseJoint)
        create_aim_wdgt.addWidget(create_jnt_btn)
        create_aim_wdgt.addWidget(aim_jnt_btn)
        return create_aim_wdgt

    def create_axis_radio_group(self, label):
        """Helper function to create a horizontal radio button group for axis selection."""
        group_box = QGroupBox(label)
        parentlayout = QVBoxLayout()  # Parent layout for the group box

        # Create a horizontal layout for the radio buttons
        layout = QHBoxLayout()
        radio_button_x = QRadioButton("X")
        radio_button_y = QRadioButton("Y")
        radio_button_z = QRadioButton("Z")

        # Add the radio buttons to the horizontal layout
        layout.addWidget(radio_button_x)
        layout.addWidget(radio_button_y)
        layout.addWidget(radio_button_z)

        # Create a QWidget to hold the layout and add it to the parent layout
        axis_widget = QWidget()
        axis_widget.setLayout(layout)
        # Add the QWidget to the parent layout
        parentlayout.addWidget(axis_widget)

        # Align the radio buttons to the top
        parentlayout.setAlignment(Qt.AlignTop)
        group_box.setLayout(parentlayout)  # Set the layout for the group box

        # Set size policy for the group box to avoid stretching
        group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return group_box  # Return the full group box widget

    def create_orient_joints_widget(self):
        """Widget for orienting joints."""
        orient_joints_wdgt = QHBoxLayout(self)
        orient_jnts_btn = QPushButton("Orient Joints")
        orient_joints_wdgt.addWidget(orient_jnts_btn)
        return orient_joints_wdgt

    def create_rename_widgets(self):
        """Widget for search/replace and prefix/suffix renaming."""
        sr_rename_wdgt = QHBoxLayout(self)
        search_lb = QLabel("Search")
        search_le = QLineEdit("")
        replace_lb = QLabel("Replace")
        replace_le = QLineEdit("")
        sr_rename_wdgt.addWidget(search_lb)
        sr_rename_wdgt.addWidget(search_le)
        sr_rename_wdgt.addWidget(replace_lb)
        sr_rename_wdgt.addWidget(replace_le)

        ps_rename_wdgt = QHBoxLayout(self)
        prefix_lb = QLabel("Prefix")
        prefix_le = QLineEdit("")
        suffix_lb = QLabel("Suffix")
        suffix_le = QLineEdit("")
        ps_rename_wdgt.addWidget(prefix_lb)
        ps_rename_wdgt.addWidget(prefix_le)
        ps_rename_wdgt.addWidget(suffix_lb)
        ps_rename_wdgt.addWidget(suffix_le)

        return sr_rename_wdgt, ps_rename_wdgt  # Return both layouts as a tuple

    def create_slider_widget(self):
        """Placeholder widget for slider."""
        layout = QVBoxLayout(self)
        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(lambda: print_widget_name("QSlider"))
        layout.addWidget(slider)
        return layout

    def create_combo_box_widget(self):
        """Placeholder widget for combo box."""
        layout = QVBoxLayout(self)
        combo_box = QComboBox()
        combo_box.addItems(["Choice 1", "Choice 2", "Choice 3"])
        combo_box.currentIndexChanged.connect(lambda: print_widget_name("QComboBox"))
        layout.addWidget(combo_box)
        return layout

    def create_spin_box_widget(self):
        """Placeholder widget for spin box."""
        layout = QVBoxLayout(self)
        spin_box = QSpinBox()
        spin_box.valueChanged.connect(lambda: print_widget_name("QSpinBox"))
        layout.addWidget(spin_box)
        return layout

    def create_label_widget(self):
        """Placeholder widget for a label."""
        layout = QVBoxLayout(self)
        label = QLabel("This is a label")
        label.setAlignment(Qt.AlignTop)
        layout.addWidget(label)
        return layout


def show_dockable_widget():
    global tm_tab_window

    # Try to delete the UI (the window) if it already exists
    try:
        if tm_tab_window is not None:
            tm_tab_window.close()  # Close the window first
            tm_tab_window.deleteLater()  # Delete the window after closing it
            tm_tab_window = None  # Set the global variable to None
    except Exception as e:
        print(f"Error deleting the UI: {e}")

    # Define a unique name for the workspace control
    workspace_control_name = "QuickToolsWindowWorkspaceControl"

    # Create the main window and set the parent
    tm_tab_window = QuickToolsWindow()

    # Create the workspace control if it doesn't exist
    if not cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, label="Quick Tools")

    # Make the widget dockable by attaching it to the workspace control
    cmds.workspaceControl(
        workspace_control_name, edit=True, uiScript=workspace_control_name
    )

    # Show the window
    tm_tab_window.show()


# Execute the show function when running the script
show_dockable_widget()
