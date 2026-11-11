# Collision and workspace checks

The screen used all 115 component occurrences in the assembled CAD. File hashes identify the tested geometry. The working pose is left [90, 100, 90, 90, 0, 0, 0]° and right [−90, 100, −90, 90, 0, 0, 0]°. Each trigger is an eighth rotary degree of freedom. The checks below evaluate the assembly as nominal rigid solids. Operator fingers, loose cables, print errors, elastic deflection, and clearance for unrepresented hardware require a physical fit test.

## Measured outcomes

| Group | Configurations | Configurations with surface crossings | Description |
|---|---:|---:|---|
| Reference and repo hanging pose | 2 | 0 | Displayed working pose and the deployment repository's parked joint angles |
| Five two-handed task paths | 85 | 0 | 17 points each. Both hands move 65 mm forward, both move 50 mm lower, both widen, both reach toward the center, or one hand reaches independently |
| Park with upper rolls first | 34 | 0 | 17 points per stage. At the hanging pose, first move J3 to +90° left and −90° right; then bring all joints to the working pose |
| Direct park-to-working interpolation | 17 | 5 | Both grips swing into the center together |
| Nearby independent poses | 128 | 3 | Separate left/right joint draws across half-widths [15, 15, 25, 20, 25, 15, 20]° |
| Full independent joint limits | 128 | 2 | Follower URDF ranges on each joint. Wrist struck the chest in one posture and forearm struck the mast in another |
| Deliberate same-point hand target | 1 | 1 | Nominal palm reference points approach within 0.006 mm; the two palm bodies overlap by 6,281.4 mm³ |

Total: 395 configurations including named endpoints and duplicated endpoints across paths. The two random sets use scrambled 14-dimensional Sobol draws with both triggers open. The task and parking paths are linear in joint angle. The left trigger sweeps continuously from 0° to 30° as the right goes from 30° to 0° on the task paths and first parking segment. The trigger sweeps reverse on the second parking segment so that both the arms and grip levers follow a continuous two-stage parking route. No motion policy is included.

The bounding-box broad phase checks all moving arms against static torso hardware, left against right, and component pairs on the same arm separated by two or more moving joints. It tests triangle crossings using FCL on CAD surfaces tessellated at 0.10 mm / 0.18 rad. It skips directly adjacent moving-link interfaces and rigidly attached parts on the same side. The dedicated mechanical interface checks address those pairs. A surface-crossing screen can miss a part wholly contained in another; surface contact alone can also be intentional. For the reported interference cases, selected positives were checked with intersections of the exact CAD solids. The example CSV includes angles, component names and overlap volumes. The test distributions do not estimate field collision rates.

## Task clearance in millimeters

The two nominal palm centers move from 220.05 mm apart in the reference pose to 100.01 mm apart at the center-reaching target. Their actual surfaces and attachments are 69.87 mm apart at that target, for open, squeezed or opposite trigger endpoints. See `Bilateral_grip_clearance.csv`. Actual human hands can extend farther than these surfaces. These palm points describe the operator controls; the follower fingers have their own physical tool offsets.

Throughout the center-reaching trajectory, the complete left and right arm models remain separated horizontally by at least **44.57 mm**; the moving geometry remains at least **259.55 mm** above the tabletop. All seven prescribed task/parking segments have strictly positive arm-to-arm and tabletop clearance bounds. All seven verified paths maintain over 65 mm of moving-hardware tabletop clearance. See `continuous_arm_separation.csv`.

An additional independent 16-joint box about the displayed arm pose permits each arm joint to move independently by ±[2.5, 2.5, 4, 4, 5, 4, 5]° and each trigger to move independently over 0–30°. All arm geometry has at least **47.15 mm** of bilateral separation throughout this box. Its moving parts stay at least **195.62 mm** above the table. In particular, both triggers can be exercised independently at the reference posture. These specific bounds describe arm-to-arm and tabletop clearance. They do not alone prove clearance from the arch and nonadjacent parts of the same arm.

Each continuous bound uses exact-geometry bounding boxes, transported through the joint transforms. At the midpoint of a small joint interval, let r be a corner's radial distance to the current joint line and h the maximum angular change on either side of the midpoint. That joint contributes at most 2 r sin(h/2) of corner movement. Replace upstream rotations first while all remaining downstream rotations are still nominal, and sum the displacement bounds for the affected axes. The signed Y or positive Z coordinate minus the summed radial terms is concave over each local box, so the corner minimum bounds every point inside. We partition each task into 32 equal intervals. In the independent 16-joint test, each arm's eight angular intervals are bisected, giving 256 boxes per arm. Minimum extents include a further 0.02 mm margin per component. These are sufficient bounds; the actual gap can be larger.

The same center-reaching trajectory also passed a continuous check of all 5,192 screened nonadjacent same-arm, bilateral, and arm-to-frame pairs from moving groups J2 and beyond. This bound includes the stated opposite trigger motions. For each pair the calculation cancels shared upstream rotations, projects padded component bounds onto 13 directions, subdivides intervals as necessary, and checks exact OpenCascade solid distances for close pairs. Direct joint interfaces and operator hands remain outside this continuous check. See `trajectory_certificate.csv`.
