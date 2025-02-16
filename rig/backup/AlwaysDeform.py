import maya.cmds as mc
import os

jointList = []
unique_names = []

this = mc.ls(sl = 1)
that = mc.listRelatives(this)

# Get all bones associate with selected meshes

def getBoneNames(jointList, unique_names):
    print('\n|-------------------------------------------------------------------------------------------|\n')
    print('-----------------------------------Always Deform Readout|-----------------------------------|')
    print('\n|-------------------------------------------------------------------------------------------|\n')
    
    for i in that:
        #print(mc.objectType(i))
    
        print('\n|-------------------------------------------------------------------------------------------|\n')
        if mc.objectType(i) == 'mesh':
            print('mesh FOUND! -> ' + i)
            print('\n|-------------------------------------------------------------------------------------------|\n')
            meshConnections = mc.listConnections(that)
            print(meshConnections)
            
            for j in meshConnections:
                if mc.objectType(j) == 'skinCluster':
                    print('\nskinCluster FOUND! -> ' + j)
                    scConnections = mc.listConnections(j, type = 'joint')
                    print(scConnections)
                    
                    for k in scConnections:
                        if mc.objectType(k) == 'joint':
                            jointList.append(k)
                else:
                    print('\nNo skinCluster found!')
                    
        else:
            print('NO MESH FOUND!')
        
        print('\n|-------------------------------------------------------------------------------------------|')
    
        for i in jointList:
            if i not in unique_names:
                unique_names.append(i)
                    
        return unique_names
def run():
               
    this = getBoneNames(jointList, unique_names)
    
    print('joint list:')
    print(this)

run()