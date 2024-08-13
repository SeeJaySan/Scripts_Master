import maya.cmds as mc
import maya.mel as mel


class AnimOpsExportPrep(object):
    def __init__(self):
        self.skl_sel = []
        self.geo_sel = []
        self.final_sel = []

    def run(self):
        self._manage_namespaces()
        self._select_and_compile()

    def _manage_namespaces(self):
        """Handle namespaces: remove unwanted ones and merge with parent."""
        default_namespaces = ['UI', 'shared']
        namespaces = mc.namespaceInfo(lon=True)

        for ns in namespaces:
            if ns not in default_namespaces:
                mc.namespace(removeNamespace=ns, mergeNamespaceWithParent=True)

    def _select_and_compile(self):
        """Select SKL_lyr and GEO_lyr layers and compile them into a final selection list."""
        # Select SKL_lyr and gather connections
        mc.select('SKL_lyr')
        self.skl_sel = mc.listConnections('SKL_lyr') or []
        if self.skl_sel:
            self.skl_sel.pop(0)
        print('SKL:', self.skl_sel)

        # Select GEO_lyr and gather connections
        mc.select('GEO_lyr')
        self.geo_sel = mc.listConnections('GEO_lyr') or []
        if self.geo_sel:
            self.geo_sel.pop(0)
        print('GEO:', self.geo_sel)

        # Compile final selection
        self.final_sel.extend(self.geo_sel)
        self.final_sel.extend(self.skl_sel)

        # Print and select the final selection
        print('Complete selection:', self.final_sel)
        mc.select(self.final_sel)


def main():
    exporter = AnimOpsExportPrep()
    exporter.run()
