"""Clean-sheet N6 arm. Coordinates are the scaled Hexfellow arm root at q=0, mm.
Run inside this directory with cadquery 2.7. Vendor STEP paths are in vendor/.
"""
from pathlib import Path
import json, math, sys
import cadquery as cq
HERE = Path(__file__).resolve().parent
OUT = HERE/'out'
OUT.mkdir(exist_ok=True)
C = 9.75
Z2,Z3,Z4,Z5,Z6=94.445,192.,286.52,373.,458.445
V=cq.Vector
Z=(0,0,1)
X=(1,0,0)
Y=(0,1,0)
PARTS=[]

def loc(origin,xdir,normal):
    return cq.Plane(origin=origin,xDir=xdir,normal=normal).location

def cyl(p,axis,r,h):
    return cq.Solid.makeCylinder(r,h,p,axis)

def rect(w,h,t,r):
    return cq.Workplane('XY').rect(w,h).extrude(t).edges('|Z').fillet(r).val()

def loft(rows):
    wires=[cq.Wire.makeEllipse(rx,ry,(x,y,z),Z,X) for x,y,z,rx,ry in rows]
    return cq.Solid.makeLoft(wires)

def union(shapes):
    return shapes[0].fuse(*shapes[1:]).clean()

def cuts(s,tools):
    return s.cut(*tools).clean()

def keep(name,group,kind,s,info=None):
    if kind=='print':
        solids=s.Solids()
        assert len(solids)==1 and solids[0].isValid(),(name,'invalid or disconnected',len(solids))
        s=solids[0]
    path='out/'+name+'.brep'
    s.exportBrep(str(HERE/path))
    PARTS.append(dict(name=name,path=path,group=group,kind=kind,**(info or {})))
    print(name,round(s.Volume()/1000,2),flush=True)

def plate_xy(center,z,w,h,t,r=3):
    return rect(w,h,t,r).translate((center[0],center[1],z))

def through4(points,start,stop,r):
    return [cyl((x,y,start),Z,r,stop-start) for x,y in points]

def xm_sole(pitch):
    """Four case M2.5 bottom-side taps, with a relief on the plug side."""
    z=pitch-14.25
    w,h,t=35.,20.,4.3
    s=plate_xy((C-16,0),z-t,w,h,t)
    # Open crescent between the two mounting islands below the cable cover.
    relief=cyl((C-16,-16,z-t-1),Z,10,t+2)
    return s.cut(relief)

def xm_fixcuts(pitch):
    z=pitch-14.25
    points=[(C+y,d) for y in (-28,-4) for d in (-6,6)]
    screws=through4(points,z-32,z+1,1.45)
    # material under seat is opened to driver/head diameter.
    wrench=through4(points,z-34,z-4.3,2.75)
    return screws+wrench

def xc_back_native():
    return plate_xy((0,-7.5),-23.7,24.,37.5,4.2,3.0)

def xc_back_tools():
    points=[(x,y) for x in (-8.,8.) for y in (-22.5,7.5)]
    return through4(points,-65,-19,1.15)+through4(points,-65,-23.7,2.35)+[cyl((0,0,-45),Z,4.65,26)]

def xc_face_native(thickness=4.2):
    return cyl((0,0,6.5),Z,10.7,thickness)

def xc_face_tools():
    points=[(6*math.cos(i*math.pi/2),6*math.sin(i*math.pi/2)) for i in range(4)]
    return through4(points,6.2,58,1.13)+through4(points,10.7,50,2.25)+[cyl((0,0,6.2),Z,3.05,48)]

def xm_locator(pitch):
    # vendor x -> arm +z, vendor y -> arm +x, shaft z -> arm +y.
    return loc((C,0,pitch),Z,Y)

def xc_roll(face):
    return loc((C,0,face-6.5),X,Z)

def xc_pitch():
    # Shaft face y=-20. Tail toward the preceding link.
    return loc((C,-26.5,Z6),(-1,0,0),Y)

def xc_last():
    # Vendor x -> arm z, y -> -y, z -> +x.
    return loc((32.75-6.5,0,Z6),Z,X)

def pitch_fork(pitch,roll):
    """Two flared cheeks converge into the rear-mounted roll case cradle.
    The forward relief leaves a central inspection/cable window between cheeks.
    """
    end=roll-30.2
    cheeks=[]
    tools=[]
    for sign in (-1,1):
        # The annular mating face lies at y=±19 on the purchased horn/idler.
        disk=cyl((C,sign*19,pitch),(0,sign,0),12.1,4.35)
        # Keep the split fork outside the body sweep through the first 40 mm.
        h=end-pitch
        rows=[(C,sign*21.22,pitch+4,10.,2.15),
              (C+0.8,sign*22.65,pitch+.24*h,7.8,3.2),
              (C+4.8,sign*23.5,pitch+.50*h,6.6,3.75),
              (C+5.1,sign*20.5,pitch+.71*h,7.0,4.3),
              (C+1.5,sign*9.5-2.3,pitch+.90*h,8.2,5.7),
              (C,sign*4.3-4,end+1.0,9.7,7.7)]
        cheeks+=[disk,loft(rows)]
        for a in (45,135,225,315):
            dx,dz=8*math.cos(math.radians(a)),8*math.sin(math.radians(a))
            tools.append(cyl((C+dx,sign*18.5,pitch+dz),(0,sign,0),1.13,12.5))
            tools.append(cyl((C+dx,sign*23.35,pitch+dz),(0,sign,0),2.25,14))
        tools.append(cyl((C,sign*18.8,pitch),(0,sign,0),4.6,16))
    mount=xc_roll(roll)
    cheeks.append(xc_back_native().moved(mount))
    # Serviceable side bolted at two clear lands above the motor case.
    join_x=C+4.8
    join_z=pitch+33
    padloc=loc((join_x,18,join_z),X,Y)
    cheeks.append(rect(14.,25.0,10.5,4.8).moved(padloc))
    for height in (27.,39.):
        tools.append(cyl((join_x,12,pitch+height),Y,1.65,21))
        tools.append(cyl((join_x,10,pitch+height),Y,3.6,10.0))
        tools.append(cyl((join_x,28.5,pitch+height),Y,3.6,8.0))
    full=cuts(union(cheeks),tools+[k.moved(mount) for k in xc_back_tools()])
    def positive_box(y_min,top):
        return cq.Solid.makeBox(95,69-y_min,top-(pitch-17),(-46,y_min,pitch-17))
    # Common clamping face at y=23.2; shoulder ends separated by 0.20 mm.
    take=union([positive_box(3.,pitch+21.9),positive_box(23.2,pitch+44.0)])
    pocket=union([positive_box(3.,pitch+22.1),positive_box(23.2,pitch+44.2)])
    main=full.cut(pocket).clean()
    removable=full.intersect(take).clean()
    return main,removable

def roll_upper():
    lm=xc_roll(Z3)
    mouth=xc_face_native().moved(lm)
    end=Z4-18.55
    spine=loft([(C,0,Z3+3.7,9.9,9.0),
                (C-2.8,-1,Z3+12.5,9.1,8.2),
                (C-9.5,-1,Z3+30,9.9,7.9),
                (C-15.5,-1,Z3+55,9.1,7.4),
                (C-16.5,0,end-8,9.6,8.4),
                (C-16,0,end+1,14.8,8.85)])
    s=union([mouth,spine,xm_sole(Z4)])
    # Rounded teardrop through-window in the neutral area of the wider bridge.
    window=loft([(C-11,-1,Z3+20,0.7,16),(C-12,-1,Z3+30,2.9,16),
                 (C-14,-1,Z3+45,3.1,16),(C-15.5,-1,Z3+58,0.7,16)])
    return cuts(s,[k.moved(lm) for k in xc_face_tools()]+xm_fixcuts(Z4)+[window])

def roll_forearm():
    lm=xc_roll(Z5); pm=xc_pitch()
    mount=xc_back_native().moved(pm)
    # Gradual dogleg clears the concentric J6/J7 crossing in the wrist.
    spine=loft([(C,0,Z5+3.75,9.8,9.0),
                (C-0.8,-2.5,Z5+13,9.1,8.7),
                (C-2,-13,Z5+32,9.6,8.3),
                (C-3,-30,Z5+47,8.4,8.0),
                (C-1,-43.4,Z5+60,9.0,6.3),
                (C,-47.9,Z5+72,10,2.65)])
    s=union([xc_face_native().moved(lm),spine,mount])
    # Trim the transition to the rear mating plane across the full case footprint.
    rear_keepout=cq.Solid.makeBox(21.0,36.0,26,(-10.5,-25.0,-19.5)).moved(pm)
    return cuts(s,[k.moved(lm) for k in xc_face_tools()]+[k.moved(pm) for k in xc_back_tools()]+[rear_keepout])

def wrist():
    p,w = xc_pitch(),xc_last()
    base=xc_face_native().moved(p)
    rear=xc_back_native().moved(w)
    # Short flared bridge lies between face of J6 and rear of J7.
    profile=loft([(0,0,0,6,7),(1,0,4,6.2,7.5),(3,0,9,5.8,8.0),
                  (4.0,0,14,4.7,9.0)])
    # local x maps to -X, local z to +Y, local y to +Z
    profile=profile.moved(loc((C-1,-16.6,Z6),(-1,0,0),Y))
    s=union([base,rear,profile])
    rear_keepout=cq.Solid.makeBox(21.0,36.0,26,(-10.5,-25.0,-19.5)).moved(w)
    return cuts(s,[k.moved(p) for k in xc_face_tools()]+[k.moved(w) for k in xc_back_tools()]+[rear_keepout])

def port_envelopes(joint):
    # Native case STEP connector mouths, expanded for insertion of an approximately
    # 10 mm plug nose in either direction. This bounds neither lead bending nor slack.
    if joint in (2,4):
        t=xm_locator(Z2 if joint==2 else Z4)
        return [cq.Solid.makeBox(12,14,9.5,(x,-21.6,-17.3)).moved(t)
                for x in (14.25,-26.25)]
    t={3:xc_roll(Z3),5:xc_roll(Z5),6:xc_pitch(),7:xc_last()}[joint]
    return [cq.Solid.makeBox(12,11.3,10.,(x,-14.65,-16.85)).moved(t)
            for x in (10.,-22.)]

def export_motors():
    xm=cq.importers.importStep(str(HERE/'vendor/X430.step')).val()
    # Only the two concentric output disks belong to the rotating fork. Their
    # side faces define the 9.75 mm radii and -16/+17 mm vendor separation planes.
    original=xm.Solids()
    front_tool=cyl((0,0,17.0),Z,9.75002,14)
    rear_tool=cyl((0,0,-16.0),(0,0,-1),9.75002,12)
    drive_disk=original[0].intersect(front_tool).clean()
    idle_disk=original[0].intersect(rear_tool).clean()
    assert len(drive_disk.Solids())==1 and len(idle_disk.Solids())==1
    body0=original[0].cut(front_tool,rear_tool).clean()
    xm_core=cq.Compound.makeCompound([body0]+original[1:])
    assert abs(xm_core.Volume()+drive_disk.Volume()+idle_disk.Volume()-xm.Volume())<.005
    xc=cq.importers.importStep(str(HERE/'vendor/XC330.step')).val().Solids()
    # Optional XC rear idler is omitted because all XC case mounts are rear plates.
    fixed=cq.Compound.makeCompound([s for i,s in enumerate(xc) if i not in (3,9,10,11,12)])
    horn=cq.Compound.makeCompound([xc[3],xc[9]])
    for j,q in [(2,xm_locator(Z2)),(3,xc_roll(Z3)),(4,xm_locator(Z4)),(5,xc_roll(Z5)),(6,xc_pitch()),(7,xc_last())]:
        if j in (2,4):
            keep(f'M{j}_XM430_case',j-1,'purchase',xm_core.moved(q),{'mass_g':80,'vendor':'ROBOTIS XM430-W210-T'})
            keep(f'M{j}_XM430_drive_horn',j,'purchase',drive_disk.moved(q),{'mass_g':2,'vendor':'ROBOTIS HN12-N101 supplied horn; allocated share of motor mass'})
            keep(f'M{j}_XM430_idler',j,'purchase',idle_disk.moved(q),{'mass_g':round(idle_disk.Volume()*0.0027,2),'vendor':'ROBOTIS rear idler envelope; mass estimated from nominal aluminum volume'})
        else:
            keep(f'M{j}_XC330_case',j-1,'purchase',fixed.moved(q),{'mass_g':22,'vendor':'ROBOTIS XC330-T288-T'})
            keep(f'M{j}_XC330_horn',j,'purchase',horn.moved(q),{'mass_g':1,'vendor':'ROBOTIS stock plastic XC330 horn and factory axial screw'})

if __name__=='__main__':
    for group,pitch,roll,stem in [(2,Z2,Z3,'Upper'),(4,Z4,Z5,'Elbow')]:
        main,removable=pitch_fork(pitch,roll)
        keep(f'L{group}_{stem}_fork',group,'print',cuts(main,port_envelopes(group+1)))
        keep(f'L{group}_{stem}_service_cheek',group,'print',cuts(removable,port_envelopes(group+1)))
    keep('L3_Upper_bone',3,'print',cuts(roll_upper(),port_envelopes(4)))
    keep('L5_Forearm_bone',5,'print',cuts(roll_forearm(),port_envelopes(6)))
    keep('L6_Wrist_saddle',6,'print',cuts(wrist(),port_envelopes(7)))
    for j in range(2,8):
        for i,port in enumerate(port_envelopes(j)):
            port.exportBrep(str(OUT/f'port_{j}_{i}.brep'))
    export_motors()
    from hardware import hardware_groups
    for g,geometry in hardware_groups(sys.modules[__name__]).items():
        keep(f'F{g}_Exterior_fasteners',g,'purchase',cq.Compound.makeCompound(geometry),
             {'vendor':'Standard purchased hardware, exposed heads and fork lap bolts', 'mass_g': [1.6,7.0,2.6,7.0,2.1,2.1][g-1]})
    (HERE/'manifest.json').write_text(json.dumps({'parts':PARTS},indent=2))
