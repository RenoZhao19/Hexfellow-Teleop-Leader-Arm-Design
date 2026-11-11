"""External shoulder stator. Canonical z points out of the torso, dimensions in mm."""
from pathlib import Path
from itertools import product
import json
import math
import sys

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App
import Part

FRAME = Path(__file__).resolve().parents[1]
ROOT = FRAME / 'fixed'
VENDOR = FRAME.parent / 'arm' / 'vendor' / 'X430.step'
V = App.Vector
X, Y, Z = V(1,0,0), V(0,1,0), V(0,0,1)

def cyl(radius, height, base, normal=Z):
    return Part.makeCylinder(radius, height, V(*base), normal)

def lathe(profile):
    vertices = [V(radius, 0, height) for radius,height in profile]
    return Part.Face(Part.makePolygon(vertices + [vertices[0]])).revolve(V(), Z, 360)

def rounded_prism(length, width, height, radius, base):
    block = Part.makeBox(length, width, height, V(*base))
    upright = [edge for edge in block.Edges if edge.BoundBox.ZLength > height-.0001]
    return block.makeFillet(radius, upright)

def hex_prism(across_flats, length):
    r = across_flats / math.sqrt(3)
    points = [V(r * math.cos(i*math.pi/3), r * math.sin(i*math.pi/3),0) for i in range(6)]
    return Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(0,0,length))

def fastener(thread_d, length, head_r, head_h, socket_af, base, head_axis=Z, button=False):
    # Under-head plane is local z=0, screw thread points -z.
    if button:
        head = lathe([(0,0),(head_r-.16,0),(head_r,.16),(head_r,.42),
                      (head_r-.26,.88),(head_r-.80,1.5),(head_r-1.65,head_h),(0,head_h)])
    else:
        head = lathe([(0,0),(head_r-.12,0),(head_r,.12),(head_r,head_h-.18),
                      (head_r-.18,head_h),(0,head_h)])
    socket = hex_prism(socket_af,head_h)
    socket.translate(V(0,0,head_h*.49))
    shank = cyl(thread_d/2, length,(0,0,-length))
    solid = head.cut(socket).fuse(shank).removeSplitter()
    solid.Placement = App.Placement(V(*base),App.Rotation(Z,head_axis))
    return solid

def circle_bolts(radius, phase=45):
    return [(radius*math.cos(math.radians(angle+phase)),
             radius*math.sin(math.radians(angle+phase))) for angle in range(0,360,90)]

def output(rows, name, shape, group, kind):
    assert not shape.isNull() and shape.isValid(), name
    if kind=='print': assert len(shape.Solids)==1, name
    path = ROOT / (name+'.brep')
    shape.exportBrep(str(path))
    rows.append(dict(name=name, path=path.name, group=group, kind=kind, external_shoulder=True))
    return shape

def build_fixed():
    ROOT.mkdir(exist_ok=True)
    rows = []
    # Split the metal drive horn from the ROBOTIS X430 assembly at its seating plane.
    # The horn rotates with J1; the case and rear idler remain fixed inside the drum.
    solids = Part.read(str(VENDOR)).Solids
    horn_volume = cyl(10.05, 10, (0,0,17.004))
    horn = solids[0].common(horn_volume)
    motor = Part.Compound([solids[0].cut(horn_volume), *solids[1:]])
    pose = App.Placement(V(0,0,34), App.Rotation(Z,-90))
    for component in (motor,horn):
        component.Placement = pose.multiply(component.Placement)

    # Annular rim and integral base plate. Base is bolted from its accessible open end.
    housing = lathe([(0,0),(42.2,0),(43.35,.75),(43.35,3.45),(43.05,4.15),
                     (42.0,4.70),(41.75,5.15),(41.75,6.0),(42.1,6.6),
                     (42.1,47.6),(41.94,48.5),(41.0,50.75),(40.3,51.5),
                     (39.3,51.5),(39.1,51.2),(39.1,9.20),(38.42,8.50),(0,8.50)])
    # Flat clamp register for the four case taps on the actual motor's posterior end.
    # Inner land x=-35.25. Outer drilling is accessible from the back of the station.
    pad = Part.makeBox(8.9,25.6,23,V(-44.15,-12.8,22.5))
    pad = pad.common(cyl(42.1,47.6,(0,0,0)))
    housing = housing.fuse(pad)
    housing = housing.cut(rounded_prism(30,24,13,5,(-25,-12,-2)))
    mount_screws=[]
    insert_bodies=[]
    for x,y in circle_bolts(35):
        housing = housing.cut(cyl(2.2,12,(x,y,-1)))
        housing = housing.cut(cyl(4.1,8,(x,y,8.5)))
        mount_screws.append(fastener(4,14,3.8,2.2,2.5,(x,y,8.5),button=True))
        # Pilot-sized brass installation envelope and screw clearance: thread geometry is omitted.
        insert_bodies.append(cyl(2.8,4,(x,y,-4)).cut(cyl(2.02,5,(x,y,-4.5))))
    case_screws=[]
    for y,z in product((-8,8),(28,40)):
        housing=housing.cut(cyl(1.43,14,(-47,y,z),X))
        housing=housing.cut(cyl(2.75,8,(-47.55,y,z),X))
        case_screws.append(fastener(2.5,7,2.25,2.5,2,(-39.55,y,z),-X))

    # Opposed rounded ports adjacent to the actual J1 connector at x~ -13, z~21.
    # They open through the side wall and allow a real connector to be reached.
    width, height = 23,14
    port = rounded_prism(width,height,104,4,(-13-width/2,-height/2,-52))
    port.rotate(V(),X,90)
    port.translate(V(0,0,21))
    housing=housing.cut(port).removeSplitter()
    output(rows, 'J1_Fixed_external_drum',housing,0,'print')
    output(rows, 'J1_XM430_fixed_case',motor,0,'purchase')
    output(rows, 'J1_XM430_drive_horn',horn,1,'purchase')
    output(rows, 'J1_Drum_mount_M4x14',Part.Compound(mount_screws),0,'purchase')
    output(rows, 'J1_Torso_M4_inserts',Part.Compound(insert_bodies),0,'purchase')
    output(rows, 'J1_Case_mount_M25x7',Part.Compound(case_screws),0,'purchase')
    (ROOT/'manifest.json').write_text(json.dumps(rows,indent=2))
