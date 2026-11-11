"""Check nominal shoulder interfaces and straight tool paths. Dimensions in mm."""
from itertools import combinations, product

from frame import CAD, FOLDER, V, X, Z, P, arm_map, polar, ring


def components(directory):
    return {path.stem: P.read(str(path)) for path in directory.glob('*.brep')}


def overlap(label, a, b):
    volume = abs(a.common(b).Volume) if a.BoundBox.intersect(b.BoundBox) else 0.
    if volume > 1.e-4:
        raise ValueError(f'{label}: {volume:.6f} cubic mm of interference')


def cylinder(radius, length, origin, axis=Z):
    return P.makeCylinder(radius, length, V(*origin), axis)


fixed = components(FOLDER/'fixed')
rotor = components(FOLDER/'rotating')
housing = fixed['J1_Fixed_external_drum']
case = fixed['J1_XM430_fixed_case']
plate = rotor['J1_Rotating_faceplate']
saddle = rotor['J1_J2_Swept_motor_saddle']
torso = P.read(str(CAD/'F01_Arched_torso.brep'))
arm = FOLDER.parent/'arm'/'out'
neighbors = {
    name: P.read(str(arm/(name+'.brep')))
    for name in ('M2_XM430_case','M2_XM430_drive_horn','M2_XM430_idler',
                 'F1_Exterior_fasteners','port_2_0','port_2_1')
}

# The nominal insert envelope, housing, motor and hardware should coexist.
for name, part in fixed.items():
    if name != 'J1_Fixed_external_drum':
        overlap('housing vs '+name, housing, part)
overlap('drum screws vs case', fixed['J1_Drum_mount_M4x14'], case)
overlap('motor screws vs inserts', fixed['J1_Case_mount_M25x7'], fixed['J1_Torso_M4_inserts'])
for y,z in product((-8,8), (28,40)):
    overlap('drum side driver', cylinder(1.5,60,(-99.55,y,z),X), housing)
for x,y in polar(35,4,45):
    overlap('drum base driver', cylinder(1.6,50,(x,y,10.7)), housing)
for dz in (0.1,6,12,25,39,55):
    shifted = case.copy()
    shifted.translate(V(0,0,dz))
    overlap(f'case insertion at {dz} mm', shifted, housing)

# Torso attachment and insert support at both real shoulder locations.
for sign in (-1,1):
    for name, part in fixed.items():
        overlap('torso vs '+name, torso, arm_map(part,sign))
    for x,y in polar(35,4,45):
        wall = ring(5.25,2.8,-4,4)
        wall.translate(V(x,y,0))
        missing = abs(arm_map(wall,sign).cut(torso).Volume)
        if missing > 1.e-4:
            raise ValueError(f'torso insert surround: {missing:.6f} cubic mm missing')
for part_path in CAD.glob('F0[345]*.brep'):
    overlap('torso vs '+part_path.stem, torso, P.read(str(part_path)))

# CAD in canonical q1=q2=0, including both J2 connector envelopes.
for name, part in rotor.items():
    for neighbor, shape in neighbors.items():
        overlap(f'{name} vs {neighbor}', part, shape)
for (name, part), (other, shape) in combinations(rotor.items(),2):
    overlap(f'{name} vs {other}', part, shape)
for x,y in product((-18.25,5.75),(-6.,6.)):
    overlap('detached saddle J2 screw entry', cylinder(2.55,50,(x,y,75.895),-Z), saddle)
for x,y in ((-29.2,0),(-2.4,21.3),(-2.4,-21.3)):
    key = cylinder(1.55,74,(x,y,64))
    for name, part in [('saddle',saddle), *neighbors.items()]:
        if name == 'saddle' or name.startswith('M2'):
            overlap('saddle driver vs '+name, key, part)
for x,y in polar(8,4,45):
    overlap('J1 horn head insertion', cylinder(1.86,35,(x,y,57.2)), plate)
print('Verified torso supports, motor insertion samples, nominal shoulder interfaces and driver paths.')
