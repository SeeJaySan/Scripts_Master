import sys
import os
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
        self.export_bn = mc.button( label='Export', command=self.exportAnimations)
        self.reopen_bn = mc.button( label='Reopen', command=self.restartFile)
        
        mc.separator(height = 20)

        #display new window
        mc.showWindow()

    def BfaOps_AnimExportPrep(self, *args):
        
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

    def exportAnimations(self, *args):
        
        mc.select('Root', hi = 1)

        filepath = mc.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        path = filepath.replace(filename, '')

        new_filename = filename.replace('ma','fbx')

        new_path = '"' + path + 'exportTesting/' + new_filename + '"'
        print(new_path)


        #exporting
        mel.eval('file -force -options "v=0;" -typ "FBX export" -pr -es {0};'.format(new_path))
    
    def restartFile(self, *args):
        filepath = mc.file(q=True, sn=True)
        mc.file(filepath, open=True, force = True)
