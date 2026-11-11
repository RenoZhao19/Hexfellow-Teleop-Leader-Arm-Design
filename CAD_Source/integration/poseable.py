"""Build a self-contained, expression-driven mechanical assembly in FreeCAD."""
import json, sys
from release_paths import WORK, RELEASE
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as A,Part
V=A.Vector
scene=json.loads((WORK/'scene.json').read_text())
dest=RELEASE/'Assemblies'/'Poseable_leader.FCStd'
doc=A.newDocument('Hexfellow_External_Drum_Leader')
fixed=doc.addObject('App::Part','Torso')
fixed.Label='Torso and table mount'
parents={}; joints={};expect={}
for side,spec in scene['arms'].items():
    unit=doc.addObject('App::Part',side)
    unit.Label=f'{side} arm and trigger'
    sign=1 if side=='Left' else -1
    unit.Placement=A.Placement(V(0,sign*65,560),A.Rotation(V(1,0,0),-sign*90))
    parents[side,0]=unit
    prev=V(0,0,0)
    for j,(point,axis,q,limits) in enumerate(zip(spec['points'],spec['axes'],spec['angles'],spec['limits']),start=1):
        node=doc.addObject('App::Part',f'{side}J{j}');parents[side,j-1].addObject(node)
        node.Label=f'{side} J{j}' if j<=7 else f'{side} squeeze trigger'
        p=V(*point)
        node.addProperty('App::PropertyVector','PivotOffset','Kinematics').PivotOffset=p-prev
        node.addProperty('App::PropertyVector','ShaftAxis','Kinematics').ShaftAxis=V(*axis)
        node.addProperty('App::PropertyAngle','JointAngle','Kinematics','Change this angle to move the joint and all downstream parts (degrees).').JointAngle=q
        node.addProperty('App::PropertyString','NominalRange','Kinematics').NominalRange=f'{limits[0]} to {limits[1]} deg'
        for prop in ['PivotOffset','ShaftAxis','NominalRange']:node.setEditorMode(prop,1)
        node.setExpression('Placement','create(<<placement>>; PivotOffset; create(<<rotation>>; ShaftAxis; JointAngle))')
        parents[side,j]=node;joints[side,j]=node;prev=p

def apply(m,xyz):
    return V(*[sum(m[i][k]*xyz[k] for k in range(3))+m[i][3] for i in range(3)])
def center(s):
    # Bounding-box center is not invariant under rotation. Evaluate an actual persistent point instead.
    if not s.Vertexes: raise ValueError('No shape vertices')
    return s.Vertexes[0].Point
def world_pt(obj):
    return obj.getGlobalPlacement().multiply(obj.Placement.inverse()).multVec(center(obj.Shape))
for idx,p in enumerate(scene['parts']):
    s=Part.read(p['path'])
    homept=center(s);side=p['side'];g=p['group']
    if side=='Frame':
        par=fixed
    else:
        par=parents[side,g]
        if g:s.translate(-V(*scene['arms'][side]['points'][g-1]))
    obj=doc.addObject('Part::Feature',f'Body{idx:03d}');obj.Label=p['local_name']
    par.addObject(obj);obj.Shape=s
    expect[obj.Name]=apply(p['matrix'],list(homept))
doc.recompute()
for n,reference in expect.items():
    diff=(world_pt(doc.getObject(n))-reference).Length
    if diff>1e-4: raise ValueError((n,diff,str(world_pt(doc.getObject(n))),str(reference)))
doc.saveAs(str(dest));A.closeDocument(doc.Name)
back=A.openDocument(str(dest));back.recompute()
for n,reference in expect.items():
    assert (world_pt(back.getObject(n))-reference).Length<1e-4
for side in scene['arms']:
    for number in (1,2,4,8):
        node=back.getObject(f'{side}J{number}')
        descendants=[o for o in node.Group if o.TypeId=='Part::Feature']
        assert len(descendants)>0
        angle=node.JointAngle.Value
        before=[world_pt(x) for x in descendants]
        node.JointAngle=angle+6;back.recompute()
        motion=max((world_pt(o)-v).Length for o,v in zip(descendants,before))
        assert motion>.01, (side,number,motion)
        node.JointAngle=angle;back.recompute()
print('Restored',len(expect),'nominal component placements after reopen; both J1, J2, J4 and trigger joints moved independently in CAD.')
A.closeDocument(back.Name)
