"""Check the guide's fasteners against regenerated round-shoulder BReps."""
import math

from frame import CAD, P, V, X, cyl, polar, ring


def load(name):
    return P.read(str(CAD / (name + ".brep")))


def check_wall(profile, center, face, length, pilot_diameter, insert_diameter, wall):
    """The entire annular shell around the knurls must be printable material."""
    shell = ring(insert_diameter / 2 + wall, pilot_diameter / 2, face - length, length)
    shell.translate(V(*center, 0))
    missing = abs(shell.cut(profile).Volume)
    assert missing < 1e-5, (center, "missing insert boss material, mm³", missing)


def main():
    cassette = load("J03_Servo_cassette")
    cup = load("J04_Twin_bearing_socket")
    cap = load("J05_Outer_race_cap")
    spindle = load("J06_Shouldered_output_spindle")
    motor = load("J01_XM430_case")
    torso = load("F01_Arched_torso")
    for x in (-11.75, 11.75):
        for sign in (-1, 1):
            y = sign * 23.5 * math.sin(math.radians(60))
            check_wall(cassette, (x, y), 8.5, 5.7, 4.0, 4.6, 3.44)
            insert = cyl(2.3, 5.7, x, y, 2.8)
            assert insert.distToShape(motor)[0] > 3.80
            # J14 has a 35 mm shank. The tip passes through the open-bore brass.
            shank = cyl(1.5, 35, x, y, 2)
            for part in (cap, cup, cassette, motor):
                assert abs(shank.common(part).Volume) < 1e-5
    for hand in (1, -1):
        bell = torso.copy()
        bell.translate(V(0, -65 * hand, -560))
        bell.rotate(V(), X, 90 * hand)
        for x, y in polar(35, phase=45):
            check_wall(bell, (x, y), 0, 4, 5.6, 6.3, 2.1)
            # Sweep the purchased J12 button head down to the cassette face.
            passage = cyl(3.8, 33, x, y, 8.5)
            for part in (cap, cup, cassette, motor, spindle):
                assert abs(passage.common(part).Volume) < 1e-5
    for x, y in polar(8, phase=45):
        # Ø3.8 head travels from the spindle flange to the z=10.5 seat.
        passage = cyl(1.9, 34, x, y, 10.5)
        assert abs(passage.common(spindle).Volume) < 1e-5
    print("Passed all J14 paths, J12 and J14 insert walls, and J12/J15 head passages.")


if __name__ == "__main__":
    main()
