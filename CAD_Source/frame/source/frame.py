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
VENDOR=FOLDER.parent/'arm/vendor/X430.step'
WORLD={'parts':[]}; ROOT={'parts':[]}
Z=V(0,0,1); Y=V(0,1,0); X=V(1,0,0)
zero=V()
def cyl(r,h,x=0,y=0,z=0,axis=Z):
    return P.makeCylinder(r,h,V(x,y,z),axis)
def box(x,y,z,dx,dy,dz):
    return P.makeBox(dx,dy,dz,V(x,y,z))
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
def xzwire(cx,y,cz,dx,dz,r):
    w=rrect_wire(cx,cz,dx,dz,r)
    w.rotate(zero,X,90);w.translate(V(0,y,0))
    return w
def save(man,n,s,kind,g=0,qty=1,material=None):
    if s.isNull() or not s.isValid():
        raise ValueError(('shape invalid',n))
    if kind in ('print','stock') and len(s.Solids)!=1:
        raise ValueError(('disconnected',n,len(s.Solids)))
    s.exportBrep(str(CAD/(n+'.brep')))
    d={'name':n,'kind':kind,'group':g,'path':str((CAD/(n+'.brep')).resolve()),'quantity':qty}
    if material:
        d['material']=material
    man['parts'].append(d)
    print(n,round(s.Volume/1000,2),len(s.Solids),flush=True)
def arm_map(s,hand):
    a=s.copy();a.rotate(zero,X,-90 if hand>0 else 90);a.translate(V(0,65*hand,560))
    return a
def tap_holes(pairs,r,z,h):
    return [cyl(r,h,x,y,z) for x,y in pairs]
def tube(z0,z1):
    return cut(rr(-96,0,40,40,2.5,z0,z1-z0),rr(-96,0,36,36,0.5,z0-1,z1-z0+2))
def world_frame():
    # Arch top, lower U arms and posterior post socket form one continuous casting/print.
    # Top and bottom faces taper laterally and fore-aft toward the shoulder bell.
    sections=[(-60,-3,563,49,28,10),(-46,-16,571,45,25,9),(-26,-39,578,51,20,8),(0,-63,579,63,19,8),(26,-39,578,51,20,8),(46,-16,571,45,25,9),(60,-3,563,49,28,10)]
    rib=P.makeLoft([xzwire(x,y,z,dx,dz,r) for y,x,z,dx,dz,r in sections],True,False)
    collar=rr(-96,0,55,56,7,425,154)
    cheeks=[]
    for sign in (-1,1):
        st=[(433,-77,12,48,25,9),(443,-70,19,47,24,8),(470,-64,28,39,20,8),(504,-46,39,34,19,8),(538,-22,48,43,24,9),(559,-10,52,44,24,9)]
        cheeks.append(P.makeLoft([rrect_wire(x,sign*y,dx,dy,r,z) for z,x,y,dx,dy,r in st],True,False))
    # Both bells are united directly to the arch. Each body is trimmed to y=±65.
    bells=[arm_map(P.makeCone(32,42,23,V(0,0,-23),Z),s) for s in (-1,1)]
    chest=unite(rib,collar,*cheeks,*bells)
    # Cut the post clearance, side-removable cartridge pockets and service exits.
    # The opening through the posterior-bottom wall accepts unplugged JST leads.
    cuts=[rr(-96,0,40.6,40.6,2.0,423,150),cyl(3.3,80,-96,-40,451,Y),cyl(3.3,80,-96,-40,540,Y)]
    for z in (451,540):
        for sg in (-1,1):
            cuts.append(cyl(7,18,-96,sg*28,z,sg*Y))
    cuff_holes=polar(35,4,45)
    for hand in (-1,1):
        motor_pocket=rr(-9.75,0,56.5,35.5,4.0,-41,42)
        wire_exit=rr(-30,0,34,44,5,-42,29)
        cuts.extend([arm_map(motor_pocket,hand),arm_map(wire_exit,hand)])
        cuts.extend(arm_map(s,hand) for s in tap_holes(cuff_holes,2.8,-7.4,8.4))
    chest=cut(chest,*cuts)
    save(WORLD,'F01_Arched_torso',chest,'print',material='PETG')
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
    mast=tube(8,570)
    pins=[(-96,0,64,Y),(-96,0,26,X),(-96,0,451,Y),(-96,0,540,Y)]
    for x,y,z,ax in pins:
        mast=cut(mast,cyl(3.3,46,x-23*ax.x,y-23*ax.y,z,ax))
    save(WORLD,'F03_Square_mast_40x40x2_L562',mast,'stock',material='6061 aluminum')
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
    return chest
def make_root():
    # Motor front has two tapped M2.5 case screws on the front face, plus a fitted rectangular key around case body.
    # Factory output and two-piece XM case are represented with geometry separated only at the visible horn.
    source=P.read(str(VENDOR))
    motor=source.Solids
    core=motor[0]
    halo=cyl(10.05,10,z=17.004)
    powered=core.common(halo)
    stationary=core.cut(halo)
    motor_rot=A.Rotation(Z,-90)
    motor_offset=A.Placement(V(0,0,-11.5),motor_rot)
    def mot_pose(shape):
        a=shape.copy();a.Placement=motor_offset.multiply(a.Placement);return a
    save(ROOT,'J01_XM430_case',mot_pose(P.Compound([stationary]+motor[1:])),'purchase')
    save(ROOT,'J02_XM430_horn',mot_pose(powered),'purchase',1)
    # The case enters the cartridge from its rear. Its two M2.5 screw heads are installed before the bearing cup.
    rear=unite(cyl(41,5.5),P.makeCone(41,39.2,3,V(0,0,5.5),Z))
    card=polar(35,phase=45)
    # The rectangular cap pattern gives all four M3 inserts solid backing beside the motor pocket.
    cup_patt=[(x, y) for x in (-11.75, 11.75)
              for y in (-23.5 * math.sin(math.radians(60)), 23.5 * math.sin(math.radians(60)))]
    cuts=[rr(-12,0,47.2,29.2,1.1,-.1,5.6),cyl(11.60,5,z=5),cyl(1.38,6,-8,11,4),cyl(1.38,6,-8,-11,4)]
    cuts+=tap_holes(card,2.2,-1,10.5)
    # Ø4.0 × 6.9 deep for CNC Kitchen M3 × 5.7. Through relief clears the M3 × 35 screw tip.
    cuts+=tap_holes(cup_patt,2.0,1.6,7.0)
    cuts+=tap_holes(cup_patt,1.65,-0.1,1.8)
    rear=cut(rear,*cuts)
    save(ROOT,'J03_Servo_cassette',rear,'print',material='PETG')
    cup=unite(P.makeCone(29,27,5,V(0,0,8.5),Z),cyl(27,20.5,z=13.5))
    cup=cut(cup,cyl(17.43,7,z=8.2),cyl(18.00,6.6,z=8.25),cyl(18.58,21,z=15),cyl(2.65,2.0,-8,11,8.4),cyl(2.65,2.0,-8,-11,8.4),*tap_holes(cup_patt,1.65,7,30))
    save(ROOT,'J04_Twin_bearing_socket',cup,'print',material='PETG')
    cap=cut(ring(27,17.4,34,3),*tap_holes(cup_patt,1.65,33,6))
    save(ROOT,'J05_Outer_race_cap',cap,'print',material='PETG')
    # A turned journal and two commercial bearings support overturning loads. Four motor screws on diagonals avoid
    # the output flange bolts on cardinal axes. The receiving shaft is threaded directly at the outboard end.
    shaft=unite(cyl(11.0,5.0,z=7.5),cyl(12.49,1.0,z=12.5),cyl(11.94,1.3,z=13.5),
                cyl(12.49,19.2,z=14.8),cyl(13.5,3.5,z=34),cyl(16.5,5.5,z=37.5))
    # Through M2x5 cap screws have 3 mm of hub grip and only 2 mm of thread in the vendor horn.
    drive=polar(8,phase=45); outbound=polar(12)
    shaft=cut(shaft,cyl(4.6,38,z=6.5),*tap_holes(drive,1.1,7,4),*tap_holes(drive,2.03,10.5,34),
              *tap_holes(outbound,1.25,37.3,6.8))
    save(ROOT,'J06_Shouldered_output_spindle',shaft,'stock',1,material='6061-T6 aluminum')
    for i,z in enumerate((15,27)):
        save(ROOT,'J07_6805ZZ_'+('inboard' if i==0 else 'outboard'),ring(18.5,12.5,z,7),'purchase')
    save(ROOT,'J08_Outer_spacer',ring(18.4,17.35,22,5),'stock',material='aluminum')
    save(ROOT,'J09_Inner_spacer',ring(13.5,12.55,22,5),'stock',1,material='aluminum')
    save(ROOT,'J10_Inner_thrust_shim',ring(13.5,12.55,14.8,.2),'purchase',1)
    # The sector is deliberately a full circular ring minus a front opening; the catalog check uses its clearance cylinder.
    cir=ring(17.40,11.95,13.6,1.2)
    cir=cut(cir,box(-1.4,10,13,2.8,10,2))
    save(ROOT,'J11_25mm_circlip_envelope',cir,'purchase',1)
    # Combined fastener references use simple cylinders with nominal shank diameter; real threads engage pilot holes.
    def fasts(pattern,head_r,shank_r,headz,eng,hh):
        return P.Compound([unite(cyl(shank_r,eng,x,y,headz-eng),cyl(head_r,hh,x,y,headz)) for x,y in pattern])
    save(ROOT,'J12_Cassette_M4x14',fasts(card,3.8,2,8.5,14,2.2),'purchase')
    save(ROOT,'J13_Motor_case_M25x6',fasts([(-8,11),(-8,-11)],2.3,1.25,8.5,6,1.7),'purchase')
    save(ROOT,'J14_Bearing_cap_M3x35',fasts(cup_patt,2.8,1.5,37,35,3),'purchase')
    save(ROOT,'J15_Horn_M2x5',fasts(drive,1.9,1,10.5,5,2),'purchase',1)
    save(ROOT,'J16_Outboard_flange_M3x10',fasts(outbound,2.75,1.5,48,10,3),'purchase',1)
    return rear,cup,cap,shaft
if __name__=='__main__':
    CAD.mkdir(exist_ok=True)
    if len(sys.argv)==1 or 'root' in sys.argv:
        make_root()
        (FOLDER/'root_manifest.json').write_text(json.dumps(ROOT,indent=2))
    if len(sys.argv)==1 or 'frame' in sys.argv:
        world_frame()
        (FOLDER/'manifest.json').write_text(json.dumps(WORLD,indent=2))
