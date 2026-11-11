# Hexfellow bimanual teleoperation leader

Open **Assemblies/Bimanual_leader.step** in Fusion to inspect the complete assembly at its working pose. **Left_leader.step** and **Right_leader.step** in the same directory show each shoulder cartridge, arm and grip individually. All linear dimensions are in mm. The Nero demonstration supplied the visual reference. The Hexfellow deployment model supplied the joint axes, relative positions and travel limits.

## Building the hardware

Work through the [hardware buying guide](Design/Hardware_buying_guide.md), [illustrated mast and shoulder assembly](Design/Shoulder_assembly.md) and [arm assembly sequence](Design/Arm_interfaces.md#assemble-one-arm). J03, J04 and J05 use a matched rectangular cap-screw pattern. Use all three files from the same revision.

## Moving the CAD

Open **Assemblies/Poseable_leader.FCStd** in FreeCAD. Expand **Left arm and trigger** or **Right arm and trigger**, then select the joint with the angle you want to change. In the Data tab, edit **JointAngle** in degrees. J1–J7 move the arm, and the **squeeze trigger** moves the finger lever. You can move both arms independently. The STEP overviews open as static assemblies in Fusion. The two grip-only STEP files show the endpoints in the same coordinate frame.

The displayed pose is J1–J7 [90, 100, 90, 90, 0, 0, 0]° on the left and [−90, 100, −90, 90, 0, 0, 0]° on the right. The trigger starts released at 0° and reaches its molded stop at 30°. The native model allows the user to select colliding angles. Use **Checks/Collision_and_workspace.md** for the tested motions, remaining interference and exact operating region. **Checks/Gravity_and_actuators.md** explains available torque at the grip. Component placement and desktop coordinates refer to the tabletop. +X is toward the operator workspace, +Y toward the left arm and +Z up.

## Mechanical decisions

- Both shoulder sockets sit directly in a single arched torso. The shoulder mounting planes are 130 mm apart, and the J2 pitch axes are 318.89 mm apart. Both measurements are 65% of their follower counterparts. Matching the torso spacing as well as the arm lengths preserves the relative wrist-center positions when both hands approach the same object. Palm centers and GP80 fingers have their own tool offsets.
- The mast is recessed behind the shoulders. An XM430 and a separately bearing-supported output spindle drive each shoulder. The upper arms and forearms use curved links with removable side cheeks at the transverse XM430 joints. The operating arm has seven revolute joints, including wrist roll; its modeled travel follows the Hexfellow joint convention.
- Each palm contains a separate DYNAMIXEL for the finger trigger. The encoder can measure partial squeezes. A future controller can map the calibrated endpoints to the Hexfellow gripper command. The mechanical design has no grip-force sensor or passive return spring. The loop allows manual reopening.
- Each side takes **3 × XM430-W210-T** (J1, J2, J4) and **5 × XC330-T288-T** (J3, J5, J6, J7, trigger). Total for the two arms is **6 XM430 + 10 XC330**. The choice of the third XM430 reflects the horizontal J1 gravity load. If the available compact servos are XC330-M181-T, those have a 3.7–6.0 V input range and require separate power engineering. Do not connect them to the common 12 V motor supply. See the manufacturer links in Design/Sources.md.

## Fabrication files

**Parts/Printable_STEP** and **Parts/Printable_STL** contain 17 unique printed designs with 28 printed occurrences in the full assembly. **Parts/Metal** contains five unique custom metal designs, including the drilled mast, crush sleeves and turned shoulder spindle. The bearing-supported spindle needs machining. **Design/CAD_parts_and_quantities.csv** lists part sizes and occurrences. Some rows represent groups of standard fasteners. Use the arm, frame and grip notes in **Design** for individual hardware quantities and fit dimensions. Part export axes follow their design geometry; select print orientation for the actual material and loads. **CAD_Source** contains the editable geometry definitions for future revisions.

## Prototype status

CAD checks covered the source joint geometry, mating parts, available tool and plug space, representative two-hand motions, and part export integrity. See **Checks** for pose vectors, geometric exceptions and static loads. The included physical geometry does not enforce collision avoidance throughout unrestricted movement. At extended poses, estimated gravity load can exceed the manufacturer's continuous estimate at J1, J2 or J3. Position control and reflected-force capability depend on the physical motors, harness and control system. Physical fit, hand clearance, cable loops, temperature under load and achievable haptics require a bench prototype.
