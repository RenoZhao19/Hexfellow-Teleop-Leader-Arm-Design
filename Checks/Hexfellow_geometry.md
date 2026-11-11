# Hexfellow geometry

The source is `robot_resources/urdf/maver_x4_gp80.urdf` from the [team deployment repository](https://github.com/ZiWang1105/hexfellow-deploy-106/blob/9ba8ea5f0aa7115a9d2f9b905c8a456904f92dd9/robot_resources/urdf/maver_x4_gp80.urdf) at commit `9ba8ea5f0aa7115a9d2f9b905c8a456904f92dd9`. The comparative calculations use both complete seven-joint URDF chains. The linear scale is 0.65. For each joint, the direction and perpendicular position of the planned shaft line equal those of the scaled follower. The longitudinal location of a motor along its own shaft can differ without changing the kinematics. The CSV lists both the source origin and the leader's representative point. I independently extracted actual cylindrical faces from the exported horn B-reps on all seven axes. The 19.5 mm-diameter XM430 and 16 mm-diameter XC330 outer horn faces are collinear with the specified axes to numerical precision on each arm. See `Measured_CAD_shafts.csv`. Cylinder direction is unsigned; encoder polarity still requires calibration. J7 is ±45 degrees on both follower arms.

| Measurement | Follower | Leader |
|---|---:|---:|
| Shoulder mounting-plane separation | 200 mm | 130 mm |
| J2–J2 lateral separation, joints at zero | 490.60 mm | 318.89 mm |
| J2–J4 span along arm | 295.50 mm | 192.075 mm |
| J4–J6 span along arm | 264.50 mm | 171.925 mm |

The left and right mounting rotations are respectively −90 and +90 degrees about +X. World +X points toward the working space, +Y to the leader's left, and +Z upward from the tabletop. The leader shoulder-mount midpoint is (0, 0, 560) mm. The deployment model uses an adjustable lift. The above comparison centers each system at its shoulder-mount midpoint and does not model lift or mobile-base commands.

The grip assembly rotates about the J7 axis; its palm and trigger are offset from the wrist center. For the wrist-center test, we used the intersection of J6 and J7. Independent explicit URDF forward kinematics and the proposed line-of-rotation kinematics were compared over 256 seven-joint Sobol samples on each side. Maximum wrist-center error was 1.47e-06 mm; maximum orientation error was 3.21e-09 rad. These residuals include the URDF's rounding of ±π/2. The test covers cross-arm registration because the 130 mm shoulder span is also scaled. A zero match here applies to the ideal joint lines. Comparison of actual machined hardware, encoder signs, joint zeros and grip-to-follower tool calibration requires a prototype.

The repo's arm angles captured for a hanging position are from [calibration/config/hardware/hexfellow_default_pose_both_j6.yaml](https://github.com/ZiWang1105/hexfellow-deploy-106/blob/9ba8ea5f0aa7115a9d2f9b905c8a456904f92dd9/calibration/config/hardware/hexfellow_default_pose_both_j6.yaml). Its migration metadata marks hardware verification as false. The clearance audit uses those angles only as a nominal follower pose for an independent geometric check.
