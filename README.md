# Hexfellow Teleop Leader Arm Design

| Front | Rear |
| --- | --- |
| ![Front view of the bimanual leader and both orange triggers](Images/Leader_front.png) | ![Rear view of both arms and their shared mast](Images/Leader_rear.png) |

| Three-quarter view | Side view |
| --- | --- |
| ![Angled view showing both forearms and trigger grips reaching forward](Images/Leader_three_quarter.png) | ![Side profile showing the shoulder, bent elbow, and trigger grip](Images/Leader_side.png) |

![FACTR-style finger trigger in its released and squeezed positions, from 0 to 30 degrees](Grip_travel.png)

A tabletop, two-handed leader for teleoperating the Hexfellow MAVER X4 and its GP80 grippers. Each hand moves a seven-joint arm and squeezes a separate proportional trigger. Both arms and the spacing between their shoulders follow the Hexfellow joint geometry at 65% scale. The round shoulder sockets and curved links take their layout from the Nero demonstration. The hand design adapts FACTR’s published palm and trigger. [FACTR 2 Nero demonstration](https://jasonjzliu.com/factr2/) · [FACTR Hardware](https://github.com/JasonJZLiu/FACTR_Hardware) · [Hexfellow deployment URDF](https://github.com/ZiWang1105/hexfellow-deploy-106/blob/9ba8ea5f0aa7115a9d2f9b905c8a456904f92dd9/robot_resources/urdf/maver_x4_gp80.urdf)

## Build the round-shoulder leader

1. **Buy the hardware.** The buying guide lists each connection, its screw size and head, and the installed quantity for two arms. Check the motor kits before ordering duplicates. [Hardware buying guide](Design/Hardware_buying_guide.md)
2. **Build the mast and one shoulder.** Follow the illustrated order for the motor cassette, two bearings, spacers, spindle, circlip and cap. Print J03, J04 and J05 from the same revision. The current cap holes form a **23.50 × 40.70 mm rectangle**. The earlier three prints used a square pattern. [Illustrated shoulder and mast assembly](Design/Shoulder_assembly.md)
3. **Build the arm and hand.** Follow the joint order from the shoulder neck to the trigger. The rear of the trigger motor takes **four 2 × 10 mm** plastic tapping screws per hand. The trigger lever takes **four 2 × 6 mm**. [Arm assembly, J2–J8](Design/Arm_interfaces.md#assemble-one-arm) · [Hand and trigger](Design/FACTR_grip.md)

## What’s in the repository

| Location | Contents |
| --- | --- |
| [Images](Images/) | Four CAD views of the assembled leader and illustrated build details. |
| [Assemblies](Assemblies/) | Whole station, individual left and right arms, released and squeezed grip close-ups, and the poseable FreeCAD model. |
| [Parts/Printable_STL](Parts/Printable_STL/) | 17 unique printable designs. The bimanual assembly uses 28 printed pieces. |
| [Parts/Printable_STEP](Parts/Printable_STEP/) | Individual solid models of those 17 designs for measuring and modifying mounting features. |
| [Parts/Metal](Parts/Metal/) | Five custom metal designs, including the mast, crush sleeves and machined shoulder spindle. |
| [Design](Design/) | Part quantities, shoulder hardware and spindle dimensions, arm interfaces, gripper construction, sources and the upstream FACTR license. Start with the [parts and quantities table](Design/CAD_parts_and_quantities.csv). |
| [Checks](Checks/) | Measured shaft axes, tested two-hand motions, known collision poses, trigger stops, assembly clearances, and gravity estimates. |
| [CAD_Source](CAD_Source/) | Python geometry generators, their upstream grip inputs and instructions for rebuilding the models. |
| [START_HERE.md](START_HERE.md) | Coordinate conventions, reference pose, actuator selection and prototype status. |

## Prototype status

The first project milestone is to reproduce the NEXT free-motion and contact demonstration on Hexfellow. The CAD, manufacturing models and geometry checks are available here. Powered teleoperation and force feedback still need hardware commissioning, encoder calibration and Hexfellow control integration.

- **Geometry.** The shoulder mounting planes are 130 mm apart. The leader’s shoulder-to-elbow and elbow-to-wrist spans are 192.075 mm and 171.925 mm. All seven measured motor shaft lines agree with the scaled follower model. [Geometry check](Checks/Hexfellow_geometry.md)
- **Two-handed workspace.** A tested reach moved the palm centers from 220 mm to 100 mm apart while the triggers moved independently. All 5,192 screened component pairs cleared that path. Other poses let the grips touch each other or a link contact the frame. Human fingers and flexible cables still need a physical fit test. [Collision report and test scope](Checks/Collision_and_workspace.md)
- **Actuators.** Each side uses **three XM430-W210-Ts** at J1, J2 and J4 and **five XC330-T288-Ts** for the other four axes and the trigger. In some extended poses the calculated gravity load at J1, J2 or J3 exceeds the manufacturer’s estimated continuous torque. Test one arm under load before assessing sustained force feedback. [Gravity and actuator estimates](Checks/Gravity_and_actuators.md) · [Motor references](Design/Sources.md)

## How to open and use the files

Start with **Code → Download ZIP** on GitHub and extract the folder on your computer. Keep the folder structure so the links and part names in the design notes stay easy to follow.

| File type | Application | What to do with it |
| --- | --- | --- |
| `.png` | A web browser, macOS Preview, or Photos | View the whole assembly and the two trigger positions. |
| `.step` | Autodesk Fusion or FreeCAD | Open an assembly to inspect component placement. Open a single part from `Parts/Printable_STEP/` or `Parts/Metal/` to measure or edit its solid geometry. The assembly STEP files show fixed poses. |
| `.FCStd` | FreeCAD | Open the native assembly and change joint angles to pose either arm and its trigger. |
| `.stl` | PrusaSlicer, or the slicer used by your lab | Prepare an individual printable mesh for a particular printer. Model dimensions are in millimeters. |
| `.md`, `.txt` | GitHub or a text editor | Read the design notes, source credits and validation reports. |
| `.csv` | GitHub, Excel, Google Sheets, or LibreOffice Calc | Look up part quantities, joint limits, tested poses and clearance measurements. |
| `.json` | A text editor or VS Code | Inspect the geometry hashes that identify the components used for the collision checks. |
| `.py` | A Python environment with CadQuery or FreeCAD modules | Regenerate or change the design using the optional CAD source. The exported models open independently. |

**Inspect the whole station in Fusion.** Open the Data Panel, select your project, choose **Upload → Select Files**, and upload `Assemblies/Bimanual_leader.step`. When the upload completes, double-click the design. The assembled arms, torso, mast, and grips open together. Use the component tree to hide one arm and inspect the shoulder mounting. [Autodesk STEP import guide](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-import-or-open-a-step-file-in-Autodesk-Fusion-360.html)

**Move the elbow or squeeze a trigger.** In FreeCAD, open `Assemblies/Poseable_leader.FCStd`. Expand **Left arm and trigger** and its nested joints in the model tree. Select **Left J4**, open its **Data** tab, and change **JointAngle** from 90° to 95°. Press Enter to see the forearm and grip move together. For the hand, select **Left squeeze trigger** and change **JointAngle** from 0° (released) to 30° (squeezed). The model permits interfering poses. Check the documented motions before drawing conclusions about clearance. [FreeCAD download](https://www.freecad.org/downloads) · [FreeCAD property editor](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Property_editor.md) · [Tested workspace](Checks/Collision_and_workspace.md)

**Prepare a part for printing.** Find the part in the quantity table, then open the matching mesh from `Parts/Printable_STL/` in the slicer. For example, the complete two-arm build uses two `J03_Servo_cassette.stl` prints. At 100% scale each measures 82 × 82 × 8.5 mm. Select the actual printer and material, set the orientation and supports for that part, slice it, and review the layer preview before exporting the printer file. The five designs under `Parts/Metal/` are machining models. [Part quantities and dimensions](Design/CAD_parts_and_quantities.csv) · [PrusaSlicer first-print guide](https://help.prusa3d.com/article/first-print-with-prusaslicer-3-0-0_1079761)

**Regenerate the CAD after a design change.** The generators use CadQuery 2.7, NumPy, SciPy and a Python interpreter with FreeCAD's Part, Mesh and MeshPart modules. Obtain the two matching ROBOTIS STEP inputs and place them under `CAD_Source/arm/vendor/`. Regenerate the arm, frame and grip first, compose the assembly, then export the models with the appropriate interpreter. Geometry changes require new fit, motion and load checks. [Source workflow](CAD_Source/README.txt) · [Required ROBOTIS inputs](CAD_Source/arm/vendor/Required_input_files.txt)
