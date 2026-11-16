# Design references

The FACTR 2 Nero demonstration is the visual reference for the bimanual layout. The fixed external drum, factory-horn faceplate and removable J2 saddle in this release are this project's own shoulder design. The team’s Hexfellow URDF supplies the kinematic reference and the ROBOTIS drawings supply the actuator interfaces.

- [FACTR 2 Nero demonstration](https://jasonjzliu.com/factr2/)
- [NEXT repository at inspected revision](https://github.com/philiphan0109/factr2_next/tree/0df02c5b26e33911078152b6c587d6e8a160d279)
- [Hexfellow MAVER X4 and GP80 URDF](https://github.com/ZiWang1105/hexfellow-deploy-106/blob/9ba8ea5f0aa7115a9d2f9b905c8a456904f92dd9/robot_resources/urdf/maver_x4_gp80.urdf)

## Original FACTR gripper

The separate FACTR Hardware repository is the public Franka leader. Each hand has a fixed grip carrying a small XC330-T288-T and a pivoting finger trigger screwed to the servo horn. The servo senses angular position. The gripper at the follower end can receive a proportional opening command after calibration. The original assembly sequence fastens a purchased FPX330-S102 to the wrist horn, mounts the printed grip, installs servo 8, and fixes the trigger to that servo's horn. The published mechanism is a lighter revision of the hardware seen in the original FACTR paper. The CAD package identifies adaptations of the FACTR prints.

- [Original hardware guide, component list, and annotated assembly photos](https://github.com/JasonJZLiu/FACTR_Hardware/tree/081c832e6f3837c0f7d7a20e183d06699cf75262)
- [Original Franka teleoperation example reads trigger angle, publishes a position command and optionally feeds back gripper motor torque](https://github.com/JasonJZLiu/FACTR_Teleop/blob/7a07ab3629af03a91c0198df7c44a0082dca77ab/src/factr_teleop/factr_teleop/factr_teleop_franka_zmq.py#L84-L116)
- [Original repository license](https://github.com/JasonJZLiu/FACTR_Hardware/blob/081c832e6f3837c0f7d7a20e183d06699cf75262/LICENSE)

## Motors and frame drawings

ROBOTIS supplies the X330 external CAD geometry used to check the rear-case and stock-horn mounting interfaces. Some component identifiers in the files originate from the earlier XC330 model. The small servos in this build are **XL330-M288-T**, 20 × 34 × 26 mm and 18 g. ROBOTIS lists current control, current-based position control and encoder readback. At the recommended 5 V the listed stall torque is 0.52 N·m. Sustained force feedback requires a loaded prototype test. The XM430-W210-T uses a separate 12 V rail. Check the label before wiring. The XL330 accepts 3.7–6.0 V.

- [ROBOTIS XL330-M288-T specifications, controls and drawings](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)
- [ROBOTIS XL330-M288-T kit contents](https://robotis.us/products/dynamixel-xl330-m288-t)
- [ROBOTIS XM430-W210 specifications](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/)
- [ROBOTIS estimated continuous torque for XM430](https://robotis.us/products/dynamixel-xm430-w210-t)
- [Earlier XC330-T288-T design reference](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/)
- [Manufacturer STEP for XM430/XH430 with horn and idler](https://www.robotis.com/service/download.php?no=158)
- [Manufacturer STEP for XL/XC330](https://www.robotis.com/service/download.php?no=1987)
- [Manufacturer STEP for the original FACTR gripper's FPX330-S102 bracket](https://www.robotis.com/service/download.php?no=2025)

The retrieved Hexfellow URDF has SHA-256 `3f6e5ee6fcf9fa7030d63cb05e96c2ccdd21b9bae1d37c8b4ef95f3ed4c756dd`.
