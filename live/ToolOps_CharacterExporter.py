from maya import cmds as mc

path = r'C:\Users\CJ Nowacek\Dropbox\My PC (DESKTOP-7N81176)\Documents\~CJ\[BFA_Runaway]\Artwork\export'

fileName = 'SKL_Robin'

def ToolOps_CharacterExporter():
    exportList = []

    mc.select('GEO')

    mc.select('GEO')
    this = mc.listRelatives(c = True)
    mc.select(this)
    geo = mc.ls(sl = 1)

    for each in geo:
        exportList.append(each)

    exportList.append('Root')

    for each in exportList:
        mc.parent(each, w = 1)
    
    #exporting
    mc.file('{}{}{}{}'.format(path, '\\', fileName, '.fbx'), f = True, options = 'v=0;', typ = "FBX export", pr = True, es = True)

    # reparenting stuff back to where it belongs
    a = list(map(lambda i : mc.parent(i, 'GEO') if i.startswith('SKL')\
    else (mc.parent(i, 'SKL') if i.startswith('Root') else None), exportList))