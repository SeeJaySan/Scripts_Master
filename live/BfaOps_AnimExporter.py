import sys
import os
import subprocess
import importlib
import maya.cmds as mc
import maya.mel as mel

class BfaOps_AnimExporter(object):
        
    #constructor
    def __init__(self):
            
        self.window = "BfaOps_AnimExport"
        self.title = "Anim Exporter"
        self.size = (400, 120)

                # close old window is open
        if mc.window(self.window, exists = True):
            mc.deleteUI(self.window, window=True)
            
        #create new window
        self.window = mc.window(self.window, title=self.title)

        mc.columnLayout(adjustableColumn = True)

        mc.text(self.title)
        mc.separator(height = 20)

        self.prep_bn = mc.button( label='Prep', command=self.BfaOps_AnimExportPrep)
        mc.separator(height = 20)
        mc.text('set time range')
        mc.separator(height = 10)
        self.minTime_bn = mc.button( label='Set Min Time', command=self.setMinTime)
        self.maxTime_bn = mc.button( label='Set Max Time', command=self.setMaxTime)
        mc.separator(height = 20)
        mc.text('Exporting')
        mc.separator(height = 10)
        self.exportSelected_bn = mc.button( label='First Time Export', command=self.exportSelection, enable = False)
        self.export_bn = mc.button( label='Export', command=self.exportAnimations, enable = False)
        mc.separator(height = 20)
        mc.text('restarting file')
        mc.separator(height = 10)
        self.reopen_bn = mc.button( label='Reopen', command=self.restartFile)
        
        mc.separator(height = 20)

        #display new window
        mc.showWindow()

    def BfaOps_AnimExportPrep(self, *args):        
        
        #prepping
        
        mel.eval('file -save;')
        
        mel.eval('namespace -mergeNamespaceWithRoot -removeNamespace "SKL_robin";')

        all_ref_paths = mc.file(q=True, reference=True) or []  # Get a list of all top-level references in the scene.

        for ref_path in all_ref_paths:
            if mc.referenceQuery(ref_path, isLoaded=True):  # Only import it if it's loaded, otherwise it would throw an error.
                mc.file(ref_path, importReference=True)  # Import the reference.

                new_ref_paths = mc.file(q=True, reference=True)  # If the reference had any nested references they will now become top-level references, so recollect them.
                if new_ref_paths:
                    for new_ref_path in new_ref_paths:
                        if new_ref_path not in all_ref_paths:  # Only add on ones that we don't already have.
                            all_ref_paths.append(new_ref_path)
        mc.select('SKL')
        this = mc.pickWalk(direction = 'DOWN')
        mc.parent(this, w = 1)

        that = mc.select('GEO')
        this1 = mc.listRelatives(c = True)
        mc.parent(this1, w = 1)

        mc.select('Root', hi = 1)
        
        mc.button(self.exportSelected_bn, e = True, enable = True)
        mc.button(self.export_bn, e = True, enable = True)
        
        mc.button(self.prep_bn, e = True, enable = False)
        mc.button(self.minTime_bn, e = True, enable = False)
        mc.button(self.maxTime_bn, e = True, enable = False)

    def exportAnimations(self, *args):
        
        # exporting
        
        mc.select('Root', hi = 1)

        filepath = mc.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        path = filepath.replace(filename, '')

        new_filename = filename.replace('ma','fbx')

        new_path = '"' + path + 'exportTesting/' + new_filename + '"'
        print(new_path)


        #exporting
        #mel.eval('file -force -options "v=0;" -typ "FBX export" -pr -es {0};'.format(new_path))
        
        min = mc.playbackOptions(q = True, min = True)
        max = mc.playbackOptions(q = True, max = True)
        
        mel.eval('FBXResetExport')
        #mel.eval('FBXProperties')
        mel.eval('FBXExportBakeComplexAnimation -v 1')
        mel.eval('FBXExportBakeComplexStart -v 1'.format (min))
        mel.eval('FBXExportBakeComplexEnd -v {0}'.format (max))
        mel.eval('FBXExportBakeComplexEnd -v {0}'.format (max))
        mel.eval('FBXExportAnimationOnly -v 1')
        mel.eval('FBXExportAnimationOnly -v 1')
        
        mc.select('Root', hi = 1)
        mel.eval('FBXExport -f {0} -s'.format(new_path))
    
    def restartFile(self, *args):
        filepath = mc.file(q=True, sn=True)
        mc.file(filepath, open=True, force = True)
        mc.button(self.exportSelected_bn, e = True, enable = False)
        mc.button(self.export_bn, e = True, enable = False)
        mc.button(self.prep_bn, e = True, enable = True)
        mc.button(self.minTime_bn, e = True, enable = True)
        mc.button(self.maxTime_bn, e = True, enable = True)
        
    def setMinTime(self, *args):

        this = mc.currentTime(q = True)

        mc.playbackOptions(min = this, ast = this)
        
    def setMaxTime(self, *args):

        this = mc.currentTime(q = True)

        mc.playbackOptions(max = this, aet = this)
        
    def exportSelection(self, *args):
        
        mel.eval('ExportSelection;')
        
