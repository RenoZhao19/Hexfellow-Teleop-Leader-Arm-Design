# Static gravity and actuator headroom

The external-drum assembly uses three XM430-W210 units per arm at J1, J2 and J4, plus five XC330-T288 units at J3, J5, J6, J7 and the J8 trigger. A hand-guided leader can run with the operator supporting its weight. This calculation asks how much torque each joint would supply if the arm held itself still. In hand-guided use, the motors also encounter the operator’s forces, friction and acceleration. The release behavior depends on commanded current and friction. Verify it on a supported bench fixture.

| Joint | Motor | Published estimated continuous N·m | Reference N·m | Maximum within sampled local motions N·m | Maximum sampled over follower joint ranges N·m |
|---|---|---:|---:|---:|---:|
| J1 | XM430-W210 | 0.600 | 0.272 | 0.421 | 0.870 |
| J2 | XM430-W210 | 0.600 | 0.106 | 0.368 | 0.843 |
| J3 | XC330-T288 | 0.184 | 0.047 | 0.124 | 0.270 |
| J4 | XM430-W210 | 0.600 | 0.281 | 0.285 | 0.285 |
| J5 | XC330-T288 | 0.184 | 0.010 | 0.026 | 0.042 |
| J6 | XC330-T288 | 0.184 | 0.038 | 0.039 | 0.039 |
| J7 | XC330-T288 | 0.184 | 0.007 | 0.030 | 0.039 |
| J8 | XC330-T288 | 0.184 | 0.000 | 0.001 | 0.001 |

Numbers are absolute joint moments. Each table cell uses the larger left/right value for the nominal mass scenario. All compact joints and the trigger use the T288 model. The XM430 reference is at 12 V. The XC330 reference is at 11.1 V. ROBOTIS derives both continuous estimates from 20% of stall torque. Applying this fraction to the published XC330 12 V stall value would give 0.20 N·m. The 3.0 and 1.0 N·m stall values at 12 V describe momentary locked-shaft performance.

**Where gravity matters.** Across the broad samples, the nominal J1, J2 and J3 maxima exceed their published continuous estimates. The selected XM430 at J1 increases the margin for the horizontal shoulder axis compared with an XC330. Long unattended holds or sustained high feedback throughout the full joint range need a thermal and load test. For work in those extended poses, an external adjustable arm-weight support or deliberately limited task region can reduce sustained load. The local sampled maxima are group maxima and may be reached at different postures. At the reference pose, projecting a linear force at the modeled palm center into all seven joints gives an ideal worst-direction force magnitude of approximately 0.59 N before J3 reaches the manufacturer's estimated continuous figure including gravity. This is a single-pose static calculation for a pure force, with the hand applying no moment. Friction, heating, inertia, control latency and user support change what a real operator feels. It is not a validated haptic gain or a commanded force.

**Mass assumptions.** Each moving arm is estimated at 475.09 g nominal. Light and heavy scenarios give 409.77 and 570.24 g. The J1 case, fixed drum and torso are stationary and therefore excluded. The J1 drive horn moves and is modeled as aluminum at 2.70 g/cm³ nominal. Each moving XM430 contributes 82 g and each compact complete servo contributes 23 g. For XM430 J2/J4 the model uses the manufacturer's approximate center of gravity in its horn frame. Other parts use their nominal solid-volume centroids. The small servo's uncertain internal mass distribution changes these estimates by roughly 0.0011 N·m per upstream joint for each 23 g unit whose center is displaced by 5 mm. The separately modeled wrist and trigger fasteners use steel density.

For the curved printed links and additional supports, the assumed effective material densities are 0.52, 0.85 and 1.24 g/cm³. The published 21 g handle and 5 g trigger masses provide the nominal effective densities for the modified FACTR grip geometry. A separate allowance for wiring and unmodeled fasteners adds 0, 21 or 42 g per arm, distributed at the seven distal joint stations. Different print perimeters, material, harnesses, and specific hardware choices change the result. The item-level estimates are in `Gravity_part_masses.csv`.

**Motion tested.** The model calculates gravity torque with the standard signed projected moment for all downstream centers of mass, and cross-checks it by differentiating gravitational potential at the displayed pose. It includes 4,096 scrambled Sobol local configurations and 16,384 broad configurations **per arm**, with J8 sampled through its specified range. Local half-widths for J1 through J7 are [15, 15, 25, 20, 25, 15, 20]° relative to the reference, clipped to the follower limits. All other degrees of freedom are sampled independently within their ranges. Gravity sampling is separate from collision screening. Each maximum is an observed sample maximum. None establishes a continuous bound or a guaranteed operator workspace.

Reference angles for J1–J8 are [90, 100, 90, 90, 0, 0, 0, 0]° on the left and [-90, 100, -90, 90, 0, 0, 0, 0]° on the right. Per-joint sign range, heavy/light results and angles for the maximum nominal observed moment are in `Gravity_estimates.csv`.

[ROBOTIS XM430-W210-T product ratings](https://robotis.us/products/dynamixel-xm430-w210-t) · [ROBOTIS XC330-T288-T product ratings](https://robotis.us/products/dynamixel-xc330-t288-t) · [ROBOTIS XM430 reference inertia](https://www.robotis.com/service/download.php?no=717) · [FACTR gripper part weights](https://github.com/JasonJZLiu/FACTR_Hardware/tree/081c832e6f3837c0f7d7a20e183d06699cf75262)
