import maya.cmds as mc
import maya.mel as mel

def createIK(limb, side, sj, ee):
    leg_ik_l = mc.ikHandle(
        sj='{0}_{1}'.format(sj, side), 
        ee='{0}_{1}'.format(ee, side), 
        n='{0}_ik_{1}'.format(limb, side), 
        p=2, 
        w=.5
    )
    createIKControl(limb, side, sj, ee)
    

def createIKControl(limb, side, sj, ee):
    pv_control = mc.curve(
        n="{0}_ik_{1}_con".format(limb, side), 
        d=1,
        p=[
            [-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
            [-0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, 1.0031016006564133],
        ],
    )
    
    mc.xform(s=[4, 4, 4])
    mc.select(pv_control)
    grp = mc.group(n='{0}_{1}_grp'.format(ee, side))
    
    mc.select(grp, '{0}_{1}'.format(ee, side))
    mel.eval('MatchTranslation;')
    const = mc.orientConstraint('{0}_{1}'.format(ee, side), pv_control, skip=['x', 'y'])
    mc.delete(const)
    mc.makeIdentity(pv_control, r=True, a=True, s=True)
    
    mc.parentConstraint(pv_control, '{0}_ik_{1}'.format(limb, side))
    mc.orientConstraint(pv_control, '{0}_{1}'.format(ee, side), mo=True)
    
def createSpine(pelvis, spine_01, spine_02, spine_03, spine_04):
    for i in range(5):
        
    pv_control = mc.curve(
        n="{0}_ik_{1}_con".format(limb, side), 
        d=1,
        p=[
            [-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
            [-0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [-0.989623460780981, 1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, 1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [-0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, -1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, -1.0031016006564133],
            [0.989623460780981, 1.0031016006564133, 1.0031016006564133],
        ],
    )
    
    mc.xform(s=[4, 4, 4])
    mc.select(pv_control)
    grp = mc.group(n='{0}_{1}_grp'.format(ee, side))
    
    mc.select(grp, '{0}_{1}'.format(ee, side))
    mel.eval('MatchTranslation;')
    

def run():
    createIK('leg', 'l', 'thigh', 'foot')
    createIK('leg', 'r', 'thigh', 'foot')
    createIK('arm', 'l', 'upperarm', 'hand')
    createIK('arm', 'r', 'upperarm', 'hand')
    
    createSpine('pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04')
    
run()
