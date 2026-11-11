"""Generate the horn-driven faceplate, removable J2 saddle and their fasteners."""
from pathlib import Path
import json, math
import cadquery as cq

base=Path(__file__).resolve().parents[1]/'rotating'
base.mkdir(exist_ok=True)
Z=(0,0,1)
Y=(0,1,0)
X=(1,0,0)

def cylinder(x,y,z,r,h):
    return cq.Solid.makeCylinder(r,h,(x,y,z),Z)

def union(*solids):
    return solids[0].fuse(*solids[1:]).clean()

def subtract(body,*tools):
    return body.cut(*tools).clean()

def ellipse(rows):
    wires=[cq.Wire.makeEllipse(rx,ry,(x,0,z),Z,X) for z,x,rx,ry in rows]
    return cq.Solid.makeLoft(wires)

def rrect(x,y,z,w,h,t,r):
    obj=cq.Workplane('XY').rect(w,h).extrude(t).edges('|Z').fillet(r).val()
    return obj.translate((x,y,z))

def box(x0,y0,z0,x1,y1,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,(x0,y0,z0))

def hex_prism(x,y,z,across,h):
    return (cq.Workplane('XY').polygon(6,across / math.cos(math.pi/6))
            .extrude(h).val().translate((x,y,z)))

def socket_screw(x,y,seat,length,r,headr,headh,key):
    blank=union(cylinder(x,y,seat-length,r,length),cylinder(x,y,seat,headr,headh))
    return subtract(blank,hex_prism(x,y,seat+0.42*headh,key,headh))

def cap_profile():
    # A flat rear rim guarantees clearance to the fixed shell. The center boss seats on the OEM horn.
    p=[(0,53),(10.15,53),(10.8,53.45),(36.8,53.45),(38.1,53.8),
       (39.0,54.65),(39.1,56.55),(38.45,57.55),(37.0,58.45),(0,58.45)]
    return cq.Workplane('XZ').polyline(p).close().revolve(360,(0,0),(0,1)).val()

def head_recess(x,y,r,seat):
    return cylinder(x,y,seat,r,18)

j1=[(8*math.cos(math.radians(a)),8*math.sin(math.radians(a))) for a in (45,135,225,315)]
saddle_fixes=[(-29.2,0),(-2.4,21.3),(-2.4,-21.3)]
j2=[(x,y) for x in (-18.25,5.75) for y in (-6.,6.)]
plate=cap_profile()
# Locate the removable saddle against a shallow, noncircular register.
plate=union(plate,rrect(-3.6,0,58.30,37,25.5,1.75,5.0))
plate=subtract(plate,cylinder(0,0,52.6,5.1,10.0),
               *[cylinder(x,y,52.2,1.12,8.9) for x,y in j1],
               *[head_recess(x,y,2.15,57.20) for x,y in j1],
               *[cylinder(x,y,52.1,1.65,10) for x,y in saddle_fixes],
               *[hex_prism(x,y,52.7,5.68,4.30) for x,y in saddle_fixes])

base_flange=ellipse([(58.45,-4,28.7,27.4),(59.0,-4,29.15,27.8),
                     (62.3,-4,28.5,27.0),(63.5,-4,27.8,26.5)])
# This gently tapered wrap forms a rising eyebrow along the motor tail, and a smaller lip across its nose.
body=ellipse([(62.7,-3.4,26.0,17.8),(67.4,-3.5,26.4,15.2),
              (74.0,-2.4,27.3,14.0),(80.0,-2.0,28.4,15.2),
              (86.0,-3.9,27.9,15.0),(93.0,-10.7,20.5,13.5),
              (98.2,-18.3,12.6,11.6),(101.4,-24.0,6.8,9.1),
              (102.5,-27.0,3.0,6.2)])
sole=rrect(-6.25,0,75.895,35,20,4.3,3.0)
saddle=union(base_flange,body,sole)
# Generic motor keepout and clearance below the vendor's JST openings.
saddle=subtract(saddle,box(-26.1,-22,80.195,21.65,22,115),
                box(-11.95,-31,68.09,2.25,-7.7,80.22))
# Four straight, backside assembly routes lead to the screws at the J2 case.
saddle=subtract(saddle,*[cylinder(x,y,54,2.77,75.895-54) for x,y in j2],
                *[cylinder(x,y,75.89,1.45,8) for x,y in j2])
# A window between the plate and the motor saddle is visible along the cradle center.
window=(cq.Workplane('XZ').center(-6.25,69.9).slot2D(16,6.1)
        .extrude(40,both=True).val())
saddle=subtract(saddle,window)
# Register plus relief around the already installed J1 horn and four factory-size socket heads.
saddle=subtract(saddle,rrect(-3.6,0,57.9,37.42,25.92,2.4,5.18),cylinder(0,0,57.7,10.4,2.7))
saddle=subtract(saddle,*[cylinder(x,y,57.5,1.65,9.8) for x,y in saddle_fixes],
                *[cylinder(x,y,63.0,3.05,64.) for x,y in saddle_fixes])
j1_screws=cq.Compound.makeCompound([socket_screw(x,y,57.2,6,1,1.86,2.0,1.5) for x,y in j1])
saddle_screws=cq.Compound.makeCompound([socket_screw(x,y,63.,10,1.5,2.75,3.0,2.5) for x,y in saddle_fixes])
nuts=cq.Compound.makeCompound([subtract(hex_prism(x,y,54.6,5.5,2.4),cylinder(x,y,54.4,1.5,3.0)) for x,y in saddle_fixes])
parts=[('J1_Rotating_faceplate','print',plate),
       ('J1_J2_Swept_motor_saddle','print',saddle),
       ('J1_Horn_drive_screws_M2x6','purchase',j1_screws),
       ('J1_Saddle_screws_M3x10','purchase',saddle_screws),
       ('J1_Saddle_captive_nuts_M3','purchase',nuts)]
rows=[]
for name,kind,s in parts:
    if not s.isValid() or (kind=='print' and len(s.Solids())!=1):
        raise RuntimeError((name,s.isValid(),len(s.Solids())))
    p=base/(name+'.brep')
    s.exportBrep(str(p))
    rows.append(dict(name=name,path=p.name,group=1,kind=kind,external_shoulder=True))
    print(name,round(s.Volume(),1),len(s.Solids()),flush=True)
(base/'manifest.json').write_text(json.dumps(rows,indent=2))
