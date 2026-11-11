"""Adapt the public FACTR handle/trigger and rotate a real XC330-T288-T for either hand.

Run using system Python with FreeCAD installed. All intrinsic sketches are millimeters,
in the published gripper handle coordinate system. Output BReps use the robot's
zero-angle arm frame. The public STEP inputs are copied unaltered in this study.
"""
from pathlib import Path
import math, json, sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App, Part, MeshPart
V = App.Vector
base=Path(__file__).resolve().parent
out=base/'parts'
out.mkdir(exist_ok=True)
vstep=base.parent/'arm/vendor/XC330.step'
def load(name):
    return Part.read(str(base/name))
def box(x,y,z,X,Y,Z):
    return Part.makeBox(X-x,Y-y,Z-z,V(x,y,z))
def cyl(center,axis,r,h):
    return Part.makeCylinder(r,h,V(*center),V(*axis))
def place(shape,origin,columns):
    mat=App.Matrix()
    for i in range(3):
        for j in range(3):
            setattr(mat,'A%d%d'%(i+1,j+1),columns[j][i])
        setattr(mat,'A%d4'%(i+1),origin[i])
    return shape.transformGeometry(mat) if mat.determinant()<0 else shape.transformed(mat)
def xy_face(cmd):
    first=last=V(*cmd[0],0)
    edges=[]
    for p in cmd[1:]:
        if len(p)==2:
            end=V(*p,0);edges.append(Part.makeLine(last,end))
        else:
            mid=V(*p[:2],0);end=V(*p[2:],0);edges.append(Part.Arc(last,mid,end).toShape())
        last=end
    if (last-first).Length>1e-8:
        edges.append(Part.makeLine(last,first))
    return Part.Face(Part.Wire(edges))
def slab(cmd,z,d):
    s=xy_face(cmd).extrude(V(0,0,d));s.translate(V(0,0,z));return s
def annulus(a,b,r,R,z,depth):
    def p(radius,angle):
        t=math.radians(angle)
        return (-7.5+radius*math.cos(t),10+radius*math.sin(t))
    return slab([p(r,a),p(R,a),p(R,(a+b)/2)+p(R,b),p(r,b),p(r,(a+b)/2)+p(r,a)],z,depth)
def mirrored(s):
    return s.mirror(V(),V(0,0,1))
def canon(s):
    return place(s,(17.75,0,528.445),((0,0,-1),(1,0,0),(0,-1,0)))
def native_servo(shape,side):
    # The motor is physically flipped about its vendor Y axis on the opposite hand.
    d=1 if side=='left' else -1
    return place(shape,(-7.5,10,d*8),((0,d,0),(-1,0,0),(0,0,d)))
handle=load('handle.step')
# Provide lateral print and vendor screw-envelope clearance around the servo.
handle=handle.cut(box(-17.26,-.26,-11.5,17.26,20.26,22))
# Direct J7 drive. A broad curved bridge keeps the grip in front of the wrist
# while allowing its palm stem to descend in the selected working posture.
bridge=slab([(-13,23.5),(13,23.5),(22,25,29,24),(47,19),(60,17),(70,17),
             (78,23,75,29),(67,33,57,32),(40,32),(19,35),(-8,35),
             (-15,33,-16,28),(-13,23.5)],-8,16)
# Lightening window in the span leaves the basal web and upper bridge intact.
window=slab([(23.5,28),(27,26.9,32,26.3),(47,23.3),(51,23.4,52.5,25.0),
             (51.2,26.6,48.4,27.4),(32,29.8),(25,30.5,23.5,28)],-9,18)
bridge=bridge.cut(window)
j7=cyl((70,15,0),(0,1,0),12,7)
lip=cyl((70,13.75,0),(0,1,0),10.5,1.28).cut(cyl((70,13.7,0),(0,1,0),8.25,1.31))
handle=handle.fuse(bridge).fuse(j7).fuse(lip)
# J7 screws seat at native y=18.7. Front stock horn registers against y=15.
for a,b in [(6,0),(-6,0),(0,6),(0,-6)]:
    handle=handle.cut(cyl((70+a,13,b),(0,1,0),1.15,30))
    handle=handle.cut(cyl((70+a,18.7,b),(0,1,0),2.2,22))
handle=handle.cut(cyl((70,13,0),(0,1,0),3.35,25))
# Clear the J8 case screw body and counterbore the four back holes slightly.
for x in [-15,15]:
    for y in [2,18]:
        handle=handle.cut(cyl((x,y,-15),(0,0,1),1.10,4.1))
# Route the J8 side-exit plug beyond the mounting bridge. Vendor connector
# mouth runs along +vendor X on one grip and -vendor X on the other.
# One fully open side port is sufficient at the end of the bus.
handle=handle.cut(box(-4.5,19.95,-9.25,7.5,41,1.6))
# Two end stops anchored to the handle. Contact faces are radial, 30 degrees apart.
pad=slab([(-16.2,21.7),(0.5,21.7),(4,26,1.3,30.5),(-14.6,31.2),
          (-18,28,-16.2,21.7)],10.6,2.7)
handle=handle.fuse(pad)
for a,b in [(55,65),(106,118)]:
    handle=handle.fuse(annulus(a,b,14.0,17.4,11.2,7.6))
trigger=load('trigger.step')
# Positive sense closes the trigger, bringing the finger loop toward the palm.
trigger=place(trigger,(-7.5,10,14.5),((0,1,0),(0,0,1),(1,0,0)))
# Relieve the source trigger underside to provide 0.7 mm of nominal case clearance.
# The original 0.1 mm nominal gap can disappear with printed surfaces.
trigger=trigger.cut(box(-120,-120,6,120,120,12.2))
trigger=trigger.cut(cyl((-7.5,10,11),(0,0,1),8.25,3.5))
trigger=trigger.fuse(annulus(65,76,8.9,17.2,14.6,3.45))
handle=handle.removeSplitter();trigger=trigger.removeSplitter()
assert handle.isValid() and len(handle.Solids)==1, (len(handle.Solids),handle.isValid())
assert trigger.isValid() and len(trigger.Solids)==1
servo=Part.read(str(vstep)).Solids
vcase=Part.Compound([servo[i] for i in (0,1,2,4,5,6,7,8,13,14)])
vhorn=Part.Compound([servo[i] for i in (3,9)])
# Purchased screw envelopes show seating and shaft reach, without modeling thread teeth.
def screw_set(pos,dir,r,under_h,head_r,head_h):
    d=V(*dir);shapes=[]
    for p in pos:
        v=V(*p)
        shapes.append(Part.makeCylinder(r,under_h,v,d).fuse(Part.makeCylinder(head_r,head_h,v,-d)))
    return Part.Compound(shapes)
J7fix=screw_set([(70+a,18.7,b) for a,b in ((6,0),(-6,0),(0,6),(0,-6))], (0,-1,0),1,6,1.9,1.7)
# The 3 mm palm seat plus the rear case's 4.5 mm entry leaves 2.5 mm in the pilot.
casefix=screw_set([(x,y,-14.5) for x in (-15,15) for y in (2,18)],(0,0,1),1,10,1.85,1.8)
# The 4 mm trigger land leaves 2 mm in the stock horn (3 mm maximum).
trigfix=screw_set([(-7.5+a,10+b,18.5) for a,b in ((6,0),(-6,0),(0,6),(0,-6))],(0,0,-1),1,6,1.85,1.8)
hardware_notes = {
    'J7_grip_screws': '4 x 2 x 6 mm plastic tapping screws',
    'J8_case_screws': '4 x 2 x 10 mm plastic tapping screws',
    'J8_trigger_screws': '4 x 2 x 6 mm plastic tapping screws',
}
parts=[];info={}
for side in ('left','right'):
    d=1 if side=='left' else -1
    # A mirrored print changes hand; the purchased servo keeps its real handedness.
    handed=lambda p: p if d==1 else mirrored(p)
    for name,grp,kind,raw in [
        ('FACTR_palm',7,'print',handed(handle)),('FACTR_trigger',8,'print',handed(trigger)),
        ('J8_XC330_T288T_case',7,'purchase',native_servo(vcase,side)),
        ('J8_XC330_T288T_horn',8,'purchase',native_servo(vhorn,side)),
        ('J7_grip_screws',7,'purchase',handed(J7fix)),
        ('J8_case_screws',7,'purchase',handed(casefix)),('J8_trigger_screws',8,'purchase',handed(trigfix))]:
        shape=canon(raw)
        path=out/(side+'_'+name+'.brep');shape.exportBrep(str(path))
        parts.append(dict(name=side.capitalize()+'_'+name,side=side,group=grp,kind=kind,path=str(path.relative_to(base)),
                          hardware_notes=hardware_notes.get(name,'')))
    info[side.capitalize()]=dict(pivot=[27.75,-d*14.5,535.945],axis=[0,-1,0],home=0,limits=[0,30],palm_center=[-40.25,d*7.5,519.945])
(base/'manifest.json').write_text(json.dumps({'parts':parts},indent=2))
(base/'trigger.json').write_text(json.dumps(info,indent=2))
