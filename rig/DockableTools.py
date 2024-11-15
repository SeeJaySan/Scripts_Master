from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QLineEdit, QSlider, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QComboBox, QSpinBox
from PySide2.QtCore import Qt
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
from msc import jointCreateAndOrientatorModule as jCO
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

def print_widget_name(widget_name):
    print(f"Widget '{widget_name}' was interacted with.")

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class QuickToolsWindow(MayaQWidgetDockableMixin, QWidget):
    def __init__(self, parent=None):
        super(QuickToolsWindow, self).__init__(parent=parent)
        self.setWindowTitle("Quick Tools")
        self.setObjectName("QuickToolsWindow")
        
        self.joint_module = jCO.jointCreateAndOrientator()
        
        main_layout = QVBoxLayout(self)
        
        jointAxisVis_wdgt = QHBoxLayout(self)
        showAxis_Btn = QPushButton("Show Axis")
        hideAxis_Btn = QPushButton("Hide Axis")
        showAxis_Btn.clicked.connect(self.joint_module.turnOnJointAxisVis)
        hideAxis_Btn.clicked.connect(self.joint_module.turnOffJointAxisVis)
        jointAxisVis_wdgt.addWidget(showAxis_Btn)
        jointAxisVis_wdgt.addWidget(hideAxis_Btn)
        
        CreateAim_wdgt = QHBoxLayout(self)
        createJnt_Btn = QPushButton("Joint at component")
        aimJnt_Btn = QPushButton("Aim at component")
        createJnt_Btn.clicked.connect(self.joint_module.createBaseJoint)
        aimJnt_Btn.clicked.connect(self.joint_module.endBaseJoint)
        CreateAim_wdgt.addWidget(createJnt_Btn)
        CreateAim_wdgt.addWidget(aimJnt_Btn)
        
        aimRadioButtons_wdgt = QHBoxLayout(self)
        radioButtons1_lb = QLabel("Aim")
        radioButtonX = QRadioButton("X")
        radioButtonY = QRadioButton("Y")
        radioButtonZ = QRadioButton("Z")
        aimReverse_Cbx = QCheckBox("Reverse")
        aimReverse_Cbx.stateChanged.connect(lambda: print_widget_name('CheckBox'))
        radioButtonGroup = QButtonGroup(self)
        radioButtonGroup.addButton(radioButtonX)
        radioButtonGroup.addButton(radioButtonY)
        radioButtonGroup.addButton(radioButtonZ)
        radioButtonGroup.buttonClicked.connect(lambda: print_widget_name('QRadioButton'))
        radioButtonGroup.buttonClicked.connect(lambda: print_widget_name('QRadioButton'))
        radioButtonGroup.buttonClicked.connect(lambda: print_widget_name('QRadioButton'))
        aimRadioButtons_wdgt.addWidget(radioButtons1_lb)
        aimRadioButtons_wdgt.addWidget(radioButtonX)
        aimRadioButtons_wdgt.addWidget(radioButtonY)
        aimRadioButtons_wdgt.addWidget(radioButtonZ)
        aimRadioButtons_wdgt.addWidget(aimReverse_Cbx)

        upRadioButtons_wdgt = QHBoxLayout(self)
        radioButtons2_lb = QLabel("Up")
        radioButtonX = QRadioButton("X")
        radioButtonY = QRadioButton("Y")
        radioButtonZ = QRadioButton("Z")
        upReverse_Cbx = QCheckBox("Reverse")
        upReverse_Cbx.stateChanged.connect(lambda: print_widget_name('CheckBox'))
        radioButtonGroup = QButtonGroup(self)
        radioButtonGroup.addButton(radioButtonX)
        radioButtonGroup.addButton(radioButtonY)
        radioButtonGroup.addButton(radioButtonZ)
        radioButtonGroup.buttonClicked.connect(lambda: print_widget_name('QRadioButton'))
        radioButtonGroup.buttonClicked.connect(lambda: print_widget_name('QRadioButton'))
        radioButtonGroup.buttonClicked.connect(lambda: print_widget_name('QRadioButton'))
        upRadioButtons_wdgt.addWidget(radioButtons2_lb)
        upRadioButtons_wdgt.addWidget(radioButtonX)
        upRadioButtons_wdgt.addWidget(radioButtonY)
        upRadioButtons_wdgt.addWidget(radioButtonZ)
        upRadioButtons_wdgt.addWidget(upReverse_Cbx)
        
        upRadioButtons_wdgta = QHBoxLayout(self)
        orintJoints_Btn = QPushButton("Orient Joints")
        upRadioButtons_wdgta.addWidget(orintJoints_Btn)
        
        srRename_wdgt = QHBoxLayout(self)
        search_lb = QLabel("Search")
        search_le = QLineEdit("")
        repalce_lb = QLabel("Replace")
        repalce_le = QLineEdit("")
        srRename_wdgt.addWidget(search_lb)
        srRename_wdgt.addWidget(search_le)
        srRename_wdgt.addWidget(repalce_lb)
        srRename_wdgt.addWidget(repalce_le)
        
        psRename_wdgt = QHBoxLayout(self)
        prefix_lb = QLabel("Prefix")
        prefix_le = QLineEdit("")
        suffix_lb = QLabel("Suffix")
        suffix_le = QLineEdit("")
        psRename_wdgt.addWidget(prefix_lb)
        psRename_wdgt.addWidget(prefix_le)
        psRename_wdgt.addWidget(suffix_lb)
        psRename_wdgt.addWidget(suffix_le)
        
        layout4 = QVBoxLayout(self)
        slider = QSlider(Qt.Horizontal)
        slider.valueChanged.connect(lambda: print_widget_name('QSlider'))
        layout4.addWidget(slider)
        
        layout6 = QVBoxLayout(self)
        comboBox = QComboBox()
        comboBox.addItems(["Choice 1", "Choice 2", "Choice 3"])
        comboBox.currentIndexChanged.connect(lambda: print_widget_name('QComboBox'))
        layout6.addWidget(comboBox)
        
        layout7 = QVBoxLayout(self)
        spinBox = QSpinBox()
        spinBox.valueChanged.connect(lambda: print_widget_name('QSpinBox'))
        layout7.addWidget(spinBox)
        
        layout8 = QVBoxLayout(self)
        label = QLabel("This is a label")
        label.setAlignment(Qt.AlignTop)
        layout8.addWidget(label)
        
        main_layout.addLayout(jointAxisVis_wdgt)
        main_layout.addLayout(CreateAim_wdgt)
        main_layout.addLayout(aimRadioButtons_wdgt)
        main_layout.addLayout(upRadioButtons_wdgt)
        main_layout.addLayout(upRadioButtons_wdgta)
        main_layout.addLayout(srRename_wdgt)
        main_layout.addLayout(psRename_wdgt)
        main_layout.addLayout(layout4)
        main_layout.addLayout(layout6)
        main_layout.addLayout(layout7)
        main_layout.addLayout(layout8)

        self.setLayout(main_layout)
        
    def create_axis_radio_group(self, label):
        """ Helper function to create a horizontal radio button group for axis selection. """
        group_box = QGroupBox(label)
        layout = QHBoxLayout()  # Change layout to horizontal
        layout.addWidget(QRadioButton("X"))
        layout.addWidget(QRadioButton("Y"))
        layout.addWidget(QRadioButton("Z"))
        group_box.setLayout(layout)
        return group_box
        
        
def show_dockable_widget():
    global tm_tab_window
    
    # Define a unique name for the workspace control
    workspace_control_name = "QuickToolsWindowWorkspaceControl"
    
    # Check if the workspace control already exists and delete it
    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name, control=True)
    
    # Create a new instance of QuickToolsWindow
    tm_tab_window = QuickToolsWindow()
    
    # Show the widget as dockable
    tm_tab_window.show(dockable=True, area='right', floating=False, uiScript="")
    
    # Rename the workspace control to our unique name
    cmds.workspaceControl(tm_tab_window.objectName(), edit=True, label="PySide Dockable", retain=False, tabToControl=[workspace_control_name, -1])
    cmds.rename(tm_tab_window.objectName(), workspace_control_name)

# Call the function to show the dockable widget
show_dockable_widget()