# Torso and supported shoulder

The J1 axes run through the two circular ends of the upper chest. Their origins are 130 mm apart and 560 mm above the tabletop. The mast center is 96 mm behind the shaft line. With 94.445 mm of arm-side offset between J1 and the shoulder pitch center, the J2 centers are 318.89 mm apart at zero, equivalent to 0.65 × 490.6 mm on the Hexfellow. The torso arch, socket bells and post collar form one custom print. The assembled-coordinate print envelope is 165.5 × 130 × 177 mm. The foot is 136 × 138 × 85 mm. A complete motor cassette withdraws outward after removing the mounting screws and unplugging its leads. The separate cup lets the motor case screws be installed before the bearings.

The two shoulder modules are identical. Each contains one XM430-W210-T and two 6805ZZ shielded radial bearings in its fixed socket. The motor horn turns a machined spindle that carries the first arm link. The two bearings carry transverse loads through the sleeve into the torso. The nominal support-center span is 12 mm. Their presence does not establish a permissible load on the printed chest, bolt group or assembled station.

For the bench sequence, use the [illustrated assembly guide](Shoulder_assembly.md). For thread pitches, head sizes, insert models and order quantities, use the [hardware buying guide](Hardware_buying_guide.md).

## Hardware quantities for the complete torso and both J1 joints

| Item | Quantity | Fit or function |
|---|---:|---|
| F01 chest and F02 foot | 1 each | Custom printed structure; inspect layer orientation and fit at the first physical build |
| Square aluminum tube | 1 | 40 × 40 × 2 mm, length 562 mm. The foot supports the tube 8 mm above the table. Tube centerline is x = −96 mm. |
| F04 internal mast sleeves | 4 | OD 10, ID 6.6, length 36 mm. Insert through the open tube ends and align at the four cross holes. |
| M6 × 65 crossbolts | 3 | Y-directed holes at 56, 443 and 532 mm from tube bottom |
| M6 × 75 crossbolt | 1 | X-directed hole at 18 mm from tube bottom |
| M6 hardware | 4 nuts and 8 washers | Crossbolts. Representative plain washer and nominal hex envelopes are modeled. |
| Table fasteners | 4 × M6 | Foot bores Ø6.6 on a 100 × 102 mm rectangle. Bolt length depends on bench and backing thickness. |
| XM430-W210-T | 2 | The powered case/horn front face is the face with the two M2.5 mounting threads. The reference STEP uses the ROBOTIS XM430/XH430 hinge envelope. Confirm horn and accessories on the purchased units. |
| M2.5 × 6 low-head screws | 4 | J1 case to printed cassette. Two per servo through a 3 mm land; 3 mm available case thread. Keep head within Ø4.6 × 1.7 mm. |
| M2 × 5 socket-head screws | 8 | Four per horn, diagonally indexed on Ø16 PCD; 3 mm spindle grip and 2 mm horn thread. Head must pass Ø4.06 mm tool bore. |
| M3 × 10 socket-head screws | 8 | Per arm four on Ø24 PCD. The first arm link is 5 mm thick. Tap M3 × 0.5 through the spindle flange. |
| M3 × 35 with M3 heat-set inserts | 8 each | Four per cartridge, through the 3 mm cap and bearing cup to the cassette. CNC Kitchen M3 × 5.7 mm inserts fit Ø4.0 × 6.9 mm pockets with Ø3.3 mm through relief. |
| M4 × 14 unflanged button-head screws and M4 heat-set inserts | 8 each | Four per cassette on Ø70 PCD. Use ruthex RX-M4Sx4.0 short inserts in the Ø5.6 × 7.4 mm pockets. The nominal 5.5 mm screw projection extends 1.5 mm past the brass into the pocket. |
| 6805ZZ bearing | 4 | 25 × 37 × 7 mm, two per spindle. Fit against the selected bearing and verify both can turn freely. |
| 25 mm external circlip | 2 | DIN 471 family. The CAD ring conservatively encloses the manufacturer's sprung diameter at the ears; it does not duplicate the purchased ear profile. |
| J08 outer and J09 inner spacers | 2 each | Both 5 mm long. Outer Ø36.8/34.7; inner Ø27/25.1. Machine the two to closely matched lengths. |
| J10 inner shim | 2 | Nominal 0.2 mm, OD 27, ID 25.1. Select thickness from actual assembled endplay. |
| J06 spindle | 2 | Turn and drill aluminum. The narrow journal tolerance and the small horn screw access holes make this a machined part. |

**Identify the matching prints.** The four M3 cap screws lie on a Ø47 mm pitch circle. Their centers form a 23.50 × 40.70 mm rectangle in J03, J04 and J05. The former square pattern left very little material between two inserts and the motor. Replace these three prints as a set if upgrading an earlier build.

**Measured insert clearance.** A solid-model check of the complete 5.7 mm installed length found at least 3.44 mm of radial plastic beyond the M3 insert’s Ø4.6 mm outer envelope, and 3.80 mm from that envelope to the XM430 case. On the torso, each flush-mounted Ø6.3 × 4.0 mm M4 insert has approximately 2.1 mm of radial plastic at the narrowest section of the bell. Gauge the first printed bell and follow the specified insert dimensions. The CAD clearance check does not measure pull-out strength. [CNC Kitchen insert dimensions](https://cnckitchen.com/s/CNCKitchen_Heat-Set-Insert-Dimensions-and-Design-Guidelines.pdf) · [Hardware buying guide](Hardware_buying_guide.md)

The harness shape, table fastener lengths and bearing endplay depend on the physical build. Install an unplugged XM430 from the rear of its loose cassette. Assemble both bearings, both spacers, the shim and circlip on the spindle at the bench. Slide the retained spindle into the cup from its open front, small nose first. The outer-race cap slips over the Ø33 mm output flange before the first arm link is fitted. The bracket provides at least 2.7 mm nominal body-side extraction clearance for the bare motor through the chest opening. Connector plugs, tubing corners and cable loops require a first-fit trial.

## J06 spindle machining reference

Axial coordinates below are measured along +z in the arm frame, with z = 0 at the torso mounting face. The inboard horn face is at z = 7.50 and the arm mating face is at z = 43.00. The nominal turning envelope is given by the stock STEP.

| Span (mm) | Diameter (mm) | Function |
|---|---:|---|
| 7.50–12.50 | 22.00 | Inboard horn seat |
| 12.50–13.50 | 24.98 | Rear circlip land |
| 13.50–14.80 | 23.88 | DIN 471–25 groove, nominal width 1.30 |
| 14.80–34.00 | 24.98 | Nominal CAD journal for actual 25 mm bearings; gauge both bearings before final machining |
| 34.00–37.50 | 27.00 | Inner-ring front abutment |
| 37.50–43.00 | 33.00 | Four M3 × 0.5 flange taps on Ø24 PCD, cardinal axes |

The central bore is Ø9.2 through. Drill four Ø2.2 horn clearance bores on Ø16 PCD rotated 45° from the flange pattern, and counterbore Ø4.06 from the outboard face to z = 10.5. Specify bearing-seat surface finish and gauge the actual shaft and housing fit before machining a batch. Keep bearing shoulder radii at or below the selected bearing's chamfer allowance. The housing seat is nominally Ø37.16 in printed CAD. Wear, printer compensation, bearing fits and present screw head sizes can change the practical clearances.

## CAD checks and exclusions

All custom torso solids and J1 prints/stocks were checked as single valid CAD solids. The complete frame was checked against both mounted J1 modules at the reference position. The static frame and nominal J1 component checks recorded only screw-thread engagements. The 0.0181 mm³ between the modeled horn screws and the fixed motor case comes from the artificial 0.004 mm separation plane used to partition the vendor's single outside-housing solid into fixed and rotating faces. The large reported values at the spindle screws are the nominal screw major diameters intersecting the modeled tap minor diameters. Pair details are in the attached CSV. The J1 arm-link foot was separately checked against the spindle and all four outboard screws with zero positive common volume.

A full-revolution check swept conservative external profiles of the spindle, clip, spacer, shim and four-screw groups against the fixed cartridge. All 25 potential pairs surviving the bounding-box test had zero positive common volume throughout rotation. Mating surfaces and motor-internal screw engagement are intentional. The wrist-to-torso motion, populated wire routing, fatigue, operator hands, motor temperature and stable force reflection require separate evaluation.

[ROBOTIS XM430-W210 drawings and specifications](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/), [NSK 6805ZZ](https://www.nsk.com/my-en/engineering/6805zz-apn.html), [DIN471-025 ring dimensions](https://americanring.com/products/snap-ring.aspx?item=DIN471-025&units=metric).
