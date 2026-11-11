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

ROBOTIS supplies the dimensional models for checking the purchased components. The specified XM430-W210-T and XC330-T288-T support current control and position readback. At 12 V the vendor lists stall torques of 3.0 and 1.0 N·m respectively. The US product pages list estimated continuous torques of 0.60 N·m for XM430 at 12 V and 0.184 N·m for XC330-T288 at 11.1 V. Hardware thermal duty and sustained feedback need a loaded test. XC330-M181-T shares the external envelope but requires 3.7–6.0 V (5.0 V recommended). A common 12 V harness would overvoltage M181 units.

- [ROBOTIS XC330-T288-T specifications](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/)
- [ROBOTIS XM430-W210 specifications](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/)
- [ROBOTIS XC330-M181-T specifications](https://emanual.robotis.com/docs/en/dxl/x/xc330-m181/)
- [ROBOTIS estimated continuous torque for XM430](https://robotis.us/products/dynamixel-xm430-w210-t)
- [ROBOTIS estimated continuous torque for XC330](https://robotis.us/products/dynamixel-xc330-t288-t)
- [Manufacturer STEP for XM430/XH430 with horn and idler](https://www.robotis.com/service/download.php?no=158)
- [Manufacturer STEP for XL/XC330](https://www.robotis.com/service/download.php?no=1987)
- [Manufacturer STEP for the original FACTR gripper's FPX330-S102 bracket](https://www.robotis.com/service/download.php?no=2025)

The retrieved Hexfellow URDF has SHA-256 `3f6e5ee6fcf9fa7030d63cb05e96c2ccdd21b9bae1d37c8b4ef95f3ed4c756dd`.
