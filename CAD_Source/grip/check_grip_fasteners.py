"""Check both J8 mounting patterns after running build.py, using FreeCAD's Python."""
import csv
import sys
from pathlib import Path

sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent


def read_part(hand, name):
    return Part.read(str(HERE / 'parts' / f'{hand}_{name}.brep'))


def arm_point(hand, x, y, z):
    """Map from the source palm frame into the corresponding arm at joint zero."""
    y_sign = -1 if hand == 'left' else 1
    return App.Vector(17.75 + y, y_sign * z, 528.445 - x)


def intervals(shape, start, direction, length):
    """Return the axial intervals where a line crosses solid material."""
    section = shape.common(Part.makeLine(start, start + direction * length))
    hits = []
    for edge in section.Edges:
        depths = [(v.Point - start).dot(direction) for v in edge.Vertexes]
        hits.append((min(depths), max(depths)))
    return sorted(hits)


def check_holes(hand, joint, positions, z, sign, land, entry, length, printed,
                receiver, other_servo_part, screws):
    results = []
    screw_overlap = abs(screws.common(other_servo_part).Volume)
    assert screw_overlap < 0.001, (hand, joint, screw_overlap)

    for number, (x, y) in enumerate(positions, 1):
        seat = arm_point(hand, x, y, z)
        direction = arm_point(hand, x, y, z + sign) - seat

        # Probe the printed web just outside the clearance bore.
        probe = arm_point(hand, x + 1.45, y, z) - direction * 0.1
        web = intervals(printed, probe, direction, land + 0.2)
        measured_land = sum(end - start for start, end in web)
        assert abs(measured_land - land) < 0.015, (hand, joint, number, web)

        # A radial offset of 0.9 mm lies inside the entry but outside the
        # smaller 1.6 mm pilot bore. Measure where its thread-forming wall starts.
        pilot_probe = arm_point(hand, x + 0.9, y, z)
        pilot = intervals(receiver, pilot_probe, direction, length + 2)
        pilot_start, pilot_end = pilot[0]
        measured_entry = pilot_start - measured_land
        assert abs(measured_entry - entry) < 0.015, (hand, joint, number, pilot)
        assert pilot_end >= length - 0.015, (hand, joint, number, pilot)

        shaft = intervals(screws, seat + direction * 0.02, direction, 20)
        reach = max(end for _, end in shaft) + 0.02
        assert abs(reach - length) < 0.005, (hand, joint, number, shaft)

        # Begin just behind the 1.8 mm head and project outward from the seat.
        driver = Part.makeCylinder(1.6, 24, seat - direction * 1.81, -direction)
        driver_overlap = sum(abs(s.common(driver).Volume) for s in (printed, receiver, other_servo_part))
        assert driver_overlap < 0.001, (hand, joint, number, driver_overlap)

        shank = Part.makeCylinder(1, reach, seat, direction)
        pilot_overlap = abs(shank.common(receiver).Volume)
        results.append([hand, joint, number, round(measured_land, 3),
                        round(reach, 3), round(measured_entry, 3),
                        round(reach - pilot_start, 3), round(pilot_overlap, 6),
                        round(driver_overlap, 6), round(screw_overlap, 6)])
    return results


def main():
    rows = []
    case_bores = [(x, y) for x in (-15, 15) for y in (2, 18)]
    trigger_bores = [(-7.5 + x, 10 + y) for x, y in ((6, 0), (-6, 0), (0, 6), (0, -6))]

    for hand in ('left', 'right'):
        case = read_part(hand, 'J8_XC330_T288T_case')
        horn = read_part(hand, 'J8_XC330_T288T_horn')
        rows.extend(check_holes(hand, 'J8 case', case_bores, -14.5, 1, 3, 4.5, 10,
                                read_part(hand, 'FACTR_palm'), case, horn,
                                read_part(hand, 'J8_case_screws')))
        rows.extend(check_holes(hand, 'J8 trigger', trigger_bores, 18.5, -1, 4, 0, 6,
                                read_part(hand, 'FACTR_trigger'), horn, case,
                                read_part(hand, 'J8_trigger_screws')))

    with (HERE / 'Grip_fastener_fit.csv').open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['hand', 'interface', 'hole', 'measured_print_land_mm',
                         'measured_shank_length_mm', 'wide_entry_mm', 'nominal_pilot_reach_mm',
                         'plain_shank_in_thread_forming_material_mm3',
                         'straight_driver_D3.2_L24_overlap_mm3',
                         'screw_group_vs_other_motor_component_mm3'])
        writer.writerows(rows)
    print(f'Verified {len(rows)} screw seats, pilot entries and driver paths.')


if __name__ == '__main__':
    main()
