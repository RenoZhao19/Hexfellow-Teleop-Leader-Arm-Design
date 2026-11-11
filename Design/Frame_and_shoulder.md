# Frame and external shoulder drum

Each J1 XM430 sits inside a short cylinder attached to the **outside** of the arched torso. Four radial screws fasten the rear end of its case to a pad in the drum wall. The stock driven horn carries a round faceplate and keyed J2 saddle. The drum has a flat mounting base, an open outboard rim and two side windows for servicing the cable plugs. Only the harness passes into the torso opening.

[Whole station STEP](../Assemblies/Bimanual_leader.step) · [Exploded assembly and mast drilling](Shoulder_assembly.md) · [Hardware buying guide](Hardware_buying_guide.md)

## Datums and interfaces

All distances are in mm. Station heights refer to the tabletop. Shoulder axial distances are measured from the flat round **outside face of F01**, increasing outward toward each arm.

| Feature | Nominal dimensions | How to use them |
|---|---|---|
| F02 foot | 136 × 138 × 85, 8 floor, four Ø6.6 bench holes on 100 × 102 centers | The post stands on the floor. Length under a bench-bolt head includes 8 of print. |
| F03 mast | 40 × 40 × 2 square tube, 453 cut length | Ends stand at 8 and 461 above the table. Drill at 18, 56, 419 and 442 from the lower cut end. Fit a 36-long sleeve at each bolt. [Mast STEP](../Parts/Metal/F03_Square_mast_40x40x2_L453.step) |
| F01 arched chest | Approximate installed envelope 167.1 front–back × 130 left–right × 189.5 tall | Post center is 96 behind the J1 shaft line. J1 face centers are 130 apart and 560 above the tabletop. |
| J1 fixed drum | Ø84.2 round body, flange Ø86.7, outboard rim ends 51.5 from F01 | Four flange screws on Ø70 bolt circle at 45°, 135°, 225°, 315°. Four motor-case screws in the back wall on a 16 × 12 rectangle. |
| Drive horn and faceplate | Horn seating face at 53.0. Central relief Ø10.2 around the factory retainer. Four M2 screws on Ø16 bolt circle. | Stationary rim ends 1.5 inboard of the nearest point of the faceplate in CAD. The outer face of the center boss registers the removable saddle. |
| J2 saddle | Rounded rectangular register and 3 M3 screws in a triangular pattern | Viewed in the CAD's local J1 face plane, screw centers are (−29.2, 0), (−2.4, +21.3) and (−2.4, −21.3), relative to the horn center. Rear-loaded M3 nuts secure the saddle. |
| J2 pitch axis | 94.445 outboard of F01's mating face and 9.75 forward of J1 in the zero pose | Zero-pose J2 spacing is 318.89, matching the 0.65-scale shoulder spacing. This is an independent operator station. [Hexfellow geometry](../Checks/Hexfellow_geometry.md) |

## Load path and fit

At J1 the load passes from the arm, through the saddle and four perimeter horn screws, into the XM430 output and its internal bearing support. The case mount transfers that load to the drum and the printed torso. **The drum rim is a clearance surface.** If it touches the faceplate when a hand bears on the grip, the actual assembly has deflected or the horn, insert, or register is loose. Check with the complete arm supported first, then measure sag and rim clearance under progressively applied hand loads.

ROBOTIS lists a 40 N radial load at **10 mm from the horn** and a 20 N axial load for the XM430. The leader carries a long offset arm and can develop a bending moment at J1. Those catalog figures do not yield a permissible grip force or demonstrate a service life for this assembly. Rigid CAD also cannot predict how a printed insert seat will creep or how a released arm will move. [XM430-W210 specifications](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/) · [Gravity and release considerations](../Checks/Gravity_and_actuators.md)

The F01 insert pockets are Ø5.6 × 7.4 deep and accept the specified Ø6.3 × 4 ruthex knurl. The CAD checks found material around each seat to Ø10.5 for the first 4 of depth, leaving at least 2.1 radially outside the knurl in that region. Before fastening the first drum, inspect the cooled insert, the outside surface of the bell and the screw-tip relief below the insert. Print settings, material and actual insertion temperature affect retention.

## Evidence for the first build

The model checks include bare-motor insertion from the outboard side, access for case and torso fasteners, the J1 horn screws through rotation and J2 motion past the drum. Sampled station poses also contain actual interferences. Real cable latches, cable loops, hardware tolerances, elastic deflection and force-reflection control require a physical trial. Start with the short routed movements identified in the workspace report. [Shoulder fit measurements](../Checks/Shoulder_interfaces.md) · [Station checks and known collisions](../Checks/Collision_and_workspace.md)
