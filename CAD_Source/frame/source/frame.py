"""Original mechanical geometry. Run with Debian FreeCAD's Python.
Canonical J1 units are mm. +z is outboard, measured from chest-side socket face.
World +X is operator-facing. Rigid-kinematic transforms live in the assembly.
"""
from pathlib import Path
import math
import json
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as A
import Part as P
V=A.Vector
FOLDER=Path(__file__).resolve().parents[1]
CAD=FOLDER/'cad'
WORLD={'parts':[]}
Z=V(0,0,1); Y=V(0,1,0); X=V(1,0,0)
zero=V()
def cyl(r,h,x=0,y=0,z=0,axis=Z):
    return P.makeCylinder(r,h,V(x,y,z),axis)
def unite(*ss):
    return ss[0].multiFuse(list(ss[1:])).removeSplitter() if len(ss)>1 else ss[0]
def cut(s,*ss):
    return s.cut(P.Compound(list(ss))).removeSplitter()
def ring(ro,ri,z,h):
    return cut(cyl(ro,h,z=z),cyl(ri,h+2,z=z-1))
def polar(r,n=4,phase=0):
    return [(r*math.cos(math.radians(phase+360*i/n)),r*math.sin(math.radians(phase+360*i/n))) for i in range(n)]
def rrect_wire(cx,cy,dx,dy,r,z=0):
    x0,x1=cx-dx/2,cx+dx/2;y0,y1=cy-dy/2,cy+dy/2;k=math.sqrt(.5)
    pt=lambda x,y:V(x,y,z)
    p=[pt(x0+r,y0),pt(x1-r,y0),pt(x1,y0+r),pt(x1,y1-r),pt(x1-r,y1),pt(x0+r,y1),pt(x0,y1-r),pt(x0,y0+r)]
    mid=[pt(x1-r+r*k,y0+r-r*k),pt(x1-r+r*k,y1-r+r*k),pt(x0+r-r*k,y1-r+r*k),pt(x0+r-r*k,y0+r-r*k)]
    ed=[]
    for i in range(4):
        j=2*i
        ed.extend((P.makeLine(p[j],p[j+1]),P.Arc(p[j+1],mid[i],p[(j+2)%8]).toShape()))
    return P.Wire(ed)
def rr(x,y,dx,dy,r,z,h):
    return P.Face(rrect_wire(x,y,dx,dy,r,z)).extrude(V(0,0,h))
def save(man,n,s,kind,g=0,qty=1,material=None):
    if s.isNull() or not s.isValid():
        raise ValueError(('shape invalid',n))
    if kind in ('print','stock') and len(s.Solids)!=1:
        raise ValueError(('disconnected',n,len(s.Solids)))
    s.exportBrep(str(CAD/(n+'.brep')))
    d={'name':n,'kind':kind,'group':g,'path':'cad/'+n+'.brep','quantity':qty}
    if material:
        d['material']=material
    man['parts'].append(d)
    print(n,round(s.Volume/1000,2),len(s.Solids),flush=True)
def arm_map(s,hand):
    a=s.copy();a.rotate(zero,X,-90 if hand>0 else 90);a.translate(V(0,65*hand,560))
    return a
def tube(z0,z1):
    return cut(rr(-96,0,40,40,2.5,z0,z1-z0),rr(-96,0,36,36,0.5,z0-1,z1-z0+2))
def rounded_yz(points,radii):
    from math import sin, tan
    walk=[]
    for j,(point,rad) in enumerate(zip(points,radii)):
        v=V(0,*point); u=V(0,*points[j-1])-v; w=V(0,*points[(j+1)%len(points)])-v
        ang=u.getAngle(w); u.normalize();w.normalize()
        t=rad/tan(ang/2); bis=u+w;bis.normalize()
        walk.append((v+u*t, v+bis*(rad/sin(ang/2)-rad),v+w*t))
    e=[]
    for k,(start,mid,end) in enumerate(walk):
        e.append(P.Arc(start,mid,end).toShape()); e.append(P.makeLine(end,walk[(k+1)%len(walk)][0]))
    return P.Wire(e)

def yz_solid(points,rads):
    w=rounded_yz(points,rads);s=P.Face(w).extrude(V(250,0,0));s.translate(V(-150,0,0));return s
def curve(points):
    c=P.BezierCurve();c.setPoles([V(x,-70,z) for x,z in points]);return c.toShape()
def side(zs):
    return [V(x,-70,z) for x,z in zs]


def world_frame():
    outside=yz_solid([(-64,600),(64,600),(64,533),(55,526),(30,451),(22,444),(-22,444),(-30,451),(-55,526),(-64,533)],[13,13,8,8,7,6,6,7,8,8])
    opening=yz_solid([(-41,584),(41,584),(21,482),(15,475),(-15,475),(-21,482)],[7,7,6,5,5,6])
    front=[(-55,437),(-58,493),(35,539),(17,605)]
    back=[(-32,605),(-25,548),(-115,498),(-110,437)]
    sag=P.Wire([curve(front),P.makeLine(side(front)[-1],side(back)[0]),curve(back),P.makeLine(side(back)[-1],side(front)[0])])
    torso=outside.common(P.Face(sag).extrude(V(0,140,0))).cut(opening)
    print('window blank',torso.isValid(),len(torso.Edges),flush=True)
    torso=torso.makeFillet(2.4,[e for e in torso.Edges if e.Length>3])
    # Flush end bells match drum screw circle. Original interface geometry is retained.
    bosses=[arm_map(P.makeCone(35.5,42.5,16,V(0,0,-16),Z),h) for h in (-1,1)]
    # Mast pocket finishes three millimetres above the tube end.
    collar=rr(-96,0,56,56,7.5,413,52)
    # Hem the exposed edge of the collar top and toe.
    collar=collar.makeFillet(2.3,[e for e in collar.Edges if e.BoundBox.ZLength<.001])
    torso=torso.multiFuse([collar,*bosses]).removeSplitter()
    print('union',torso.isValid(),len(torso.Solids),flush=True)
    # Round central cable tunnel through each flange and beam. Inner end opens into the front-visible window.
    cutters=[rr(-96,0,40.6,40.6,2,411,51)]
    for h in (-1,1):
        cutters.append(arm_map(rr(-10,0,30,24,4,-62,64),h))
        for x,y in polar(35,4,45):cutters.append(arm_map(cyl(2.8,8.2,x,y,-7.4),h))
    for z in (427,450):
        cutters.append(cyl(3.3,74,-96,-37,z,Y))
        for sg in (-1,1):cutters.append(cyl(7.0,15,-96,sg*28,z,Y*sg))
    for c in cutters:torso=torso.cut(c)
    torso=torso.removeSplitter()
    print('final',torso.isValid(),len(torso.Solids),flush=True)
    save(WORLD,'F01_Arched_torso',torso,'print',material='PETG')
    # Foot tapers upward into the collar around mast. A printed closed floor carries the tube end.
    foot=P.makeLoft([rrect_wire(-96,0,136,138,13,0),rrect_wire(-96,0,136,138,13,7),rrect_wire(-96,0,88,88,12,12),rrect_wire(-96,0,64,64,11,33),rrect_wire(-96,0,56,56,8,85)],True,True)
    holes=[rr(-96,0,40.6,40.6,2,8,80),cyl(3.3,90,-96,-45,64,Y),cyl(3.3,95,-144,0,26,X)]
    for x in (-50,50):
        for y in (-51,51):
            holes.extend((cyl(3.3,35,-96+x,y,-1),cyl(7.5,28,-96+x,y,8.0)))
    for ax,span,ht in [(X,32,26),(Y,27,64)]:
        c=V(-96,0,ht)
        for sg in (-1,1):
            sgax=ax*sg;pt=c+sgax*span
            holes.append(cyl(7.6,30,*pt,axis=sgax))
    foot=cut(foot,*holes)
    save(WORLD,'F02_Flared_table_foot',foot,'print',material='PETG')
    # Through-sleeves insert from the open tube ends before fitting its crossbolts.
    mast=tube(8,461)
    pins=[(-96,0,64,Y),(-96,0,26,X),(-96,0,427,Y),(-96,0,450,Y)]
    for x,y,z,ax in pins:
        mast=mast.cut(cyl(3.3,46,x-23*ax.x,y-23*ax.y,z,ax))
    save(WORLD,'F03_Square_mast_40x40x2_L453',mast,'stock',material='6061 aluminum')
    for i,(x,y,z,ax) in enumerate(pins):
        base=V(x,y,z)-ax*18;sl=cyl(5,36,*base,axis=ax).cut(cyl(3.3,38,*(base-ax),axis=ax))
        save(WORLD,f'F04_Mast_sleeve_{i+1}',sl,'stock',material='aluminum')
    for i,((x,y,z,ax),span,length) in enumerate(zip(pins,[27,32,28,28],[65,75,65,65])):
        c=V(x,y,z);start=c-ax*(span+1.6);fin=c+ax*(span+1.6)
        def circle(rad,h,p): return cyl(rad,h,*p,axis=ax)
        washers=[circle(6,1.6,start),circle(6,1.6,c+ax*span)]
        washers=[w.cut(circle(3.2,3,c0-ax*.5)) for w,c0 in zip(washers,[start,c+ax*span])]
        # Standard M6, 10 mm across-flats outer nut envelope, hex head/washer stack.
        nutpts=[V(xx,yy,0) for xx,yy in polar(10/math.sqrt(3),6)]
        def hexat(point,h):
            prism=P.Face(P.makePolygon(nutpts+[nutpts[0]])).extrude(V(0,0,h));prism.Placement=A.Placement(point,A.Rotation(Z,ax));return prism
        nut=hexat(fin,5.0).cut(circle(3,7,fin-ax));bolt=unite(hexat(start-ax*4,4),circle(3,length,start))
        save(WORLD,f"F05_M6x{length}_post_pin_{i+1}",P.Compound([bolt,nut,*washers]),"purchase")

if __name__ == '__main__':
    from fixed_shoulder import build_fixed
    CAD.mkdir(exist_ok=True)
    world_frame()
    (FOLDER/'manifest.json').write_text(json.dumps(WORLD, indent=2))
    build_fixed()
