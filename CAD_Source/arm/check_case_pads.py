"""Measure the four XL330 rear mounting pads in the printable STEP exports."""
import argparse
from itertools import combinations
from math import dist, isclose
from pathlib import Path
import sys

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App
import Part

# Axis normal to each motor's rear case in its printable STEP coordinates.
PAD_AXES = {'L2_Upper_fork': 2, 'L4_Elbow_fork': 2,
            'L5_Forearm_bone': 1, 'L6_Wrist_saddle': 0}


def check_pad(path, normal):
    shape = Part.read(str(path))
    bores = []
    plane = [i for i in range(3) if i != normal]
    for face in shape.Faces:
        surface = face.Surface
        if not isinstance(surface, Part.Cylinder) or abs(surface.Axis[normal]) < 0.99999:
            continue
        if isclose(surface.Radius, 1.15, abs_tol=1e-5):
            bounds = face.BoundBox
            depth = (bounds.XLength, bounds.YLength, bounds.ZLength)[normal]
            bores.append((surface.Center, depth, bounds.Center[normal]))
    if len(bores) != 4 or any(abs(depth - 3.0) > 1e-5 for _, depth, _ in bores):
        raise ValueError(f'{path.name}: expected four Ø2.30 bores through 3.00 mm of print')

    centers = [[point[i] for i in plane] for point, _, _ in bores]
    spacing = sorted(round(dist(a, b), 4) for a, b in combinations(centers, 2))
    if spacing != [16., 16., 30., 30., 34., 34.]:
        raise ValueError(f'{path.name}: the XL330 rear screw pattern is not 16 × 30 mm')

    # Sample the flat strip between each screw pocket and the side of the pad.
    # The 24 mm wide pad extends 4 mm beyond the 16 mm screw spacing.
    widths = [max(row[j] for row in centers) - min(row[j] for row in centers) for j in range(2)]
    short_index = widths.index(min(widths))
    short_axis = plane[short_index]
    center = sum(row[short_index] for row in centers) / len(centers)
    for point, _, mid in bores:
        probe = list(point)
        probe[short_axis] += 3.0 if point[short_axis] > center else -3.0
        start = probe.copy()
        end = probe.copy()
        start[normal], end[normal] = mid - 3.0, mid + 3.0
        line = Part.makeLine(App.Vector(*start), App.Vector(*end))
        material = shape.common(line).Length
        if not isclose(material, 3.0, abs_tol=1e-4):
            raise ValueError(f'{path.name}: flat plate outside head pockets measures {material:.4f} mm')
    print(f'{path.name}: 3.00 mm at four holes and four flat-pad locations, 16 × 30 mm pattern')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step_directory', type=Path, help='Directory of individual printable STEP files')
    step_directory = parser.parse_args().step_directory
    for name, axis in PAD_AXES.items():
        check_pad(step_directory / (name + '.step'), axis)
