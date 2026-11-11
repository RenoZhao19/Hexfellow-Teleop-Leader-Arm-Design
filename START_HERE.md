# Open, inspect and build the leader

Download the repository with **Code → Download ZIP** on GitHub and extract it. The models use millimeters. The STEP assemblies open at fixed poses and the native FreeCAD assembly exposes each joint angle.

| To inspect | File |
| --- | --- |
| Complete station in its working pose | [Bimanual_leader.step](Assemblies/Bimanual_leader.step) |
| A single shoulder, arm and hand | [Left_leader.step](Assemblies/Left_leader.step) · [Right_leader.step](Assemblies/Right_leader.step) |
| Both arms with adjustable joint angles | [Poseable_leader.FCStd](Assemblies/Poseable_leader.FCStd) |
| Grip endpoints in the same coordinate system | [Grip_released.step](Assemblies/Grip_released.step) · [Grip_squeezed.step](Assemblies/Grip_squeezed.step) |
| Individual part dimensions, solid models and meshes | [Part quantities](Design/CAD_parts_and_quantities.csv) · [Printable STEP](Parts/Printable_STEP/) · [Printable STL](Parts/Printable_STL/) · [Metal STEP](Parts/Metal/) |

## Inspect and move the assembly

**Fusion.** Upload the complete STEP through the Data Panel, then open it and expand the component tree. Hide the fixed shoulder drum or section through it to see how the factory horn drives the faceplate.

**FreeCAD.** Open the FCStd, expand **Left arm and trigger** or **Right arm and trigger**, and select a joint. In the **Data** tab edit **JointAngle** in degrees. For example, move the left J4 elbow from 90° to 95°, or change the left squeeze trigger from 0° to 30°. The CAD lets you select angles that cause interference. Use the recorded two-stage path if you want to inspect the transition from hanging to working. [Workspace checks and pose data](Checks/Collision_and_workspace.md)

| Working pose | J1 | J2 | J3 | J4 | J5 | J6 | J7 | Trigger |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Left | 90° | 100° | 90° | 90° | 0° | 0° | 0° | 0° |
| Right | −90° | 100° | −90° | 90° | 0° | 0° | 0° | 0° |

The tabletop defines zero height. +X points toward the workspace, +Y toward the left arm and +Z upward. At zero joint angles the two J2 axes are 318.89 mm apart. Encoder direction, joint zero and the transform from the hand to the follower tool need calibration on the actual station. [Joint conventions and dimensions](Checks/Hexfellow_geometry.md)

## Build in this order

1. Check the quantities supplied in your motor kits, choose the bench bolts for your tabletop thickness and source the remaining items. The published elbow mount fits an XM430. [Buying guide and joint-by-joint fasteners](Design/Hardware_buying_guide.md)
2. Print the parts listed in the quantity table at 100% scale in millimeters. The largest torso print measures 166.5 × 130 × 189.5 mm in its export axes. Slice the actual quantities on your printer to estimate print time and filament use. Print and fit one shoulder set before committing to the second. Use the two metal STEP designs to prepare the drilled mast and four sleeves. [Fabrication inventory](Design/CAD_parts_and_quantities.csv) · [Frame dimensions](Design/Frame_and_shoulder.md)
3. Build and secure the stand, then fit the fixed shoulder drum, J1 horn, rotating faceplate and J2 saddle. Check wire and tool access before installing the upper arm. [Illustrated installation](Design/Shoulder_assembly.md)
4. Work outward from J2 to the wrist and grip. Keep the arm supported while checking drive screws, passive idlers and both trigger stops. [Arm installation](Design/Arm_interfaces.md) · [Palm and trigger](Design/FACTR_grip.md)
5. With one full arm supported, check faceplate play, saddle deflection, cable motion and the clearance to the drum throughout the intended motion. Powered bring-up then needs motor IDs and zero offsets, current limits, temperature monitoring and a deliberate release behavior before coupling the leader to the follower. [Gravity and actuator data](Checks/Gravity_and_actuators.md)

The current release is a mechanical prototype. Measurements on the physical station are still needed to establish stiffness, comfortable operation and sustainable reflected force. To modify the geometry, use the [CAD source and rebuild instructions](CAD_Source/README.txt).
