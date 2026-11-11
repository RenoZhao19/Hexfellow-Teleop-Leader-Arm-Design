# FACTR-style proportional grip

Each hand holds a fixed palm and moves a small finger lever. Its shaft drives a separate XC330-T288-T horn, so the eighth encoder measures squeeze angle. The modeled travel is 0° open to 30° closed. Calibrate these two physical endpoints against the GP80's actual open and closed commands during control bring-up. A halfway squeeze can command an intermediate width. This CAD contains no grip force sensor, passive return spring or controller. The operator may reopen the lever, or a later controller may provide a return torque.

**Origin.** The public FACTR Franka hardware includes a printable gripper handle and finger trigger. The handle bolts to a bracket on J7. A separate XC330-T288-T sits in the handle and four screws attach the trigger to its horn. The authors identify this published unit as a simplified, lighter update to their paper apparatus. The Nero footage is a visual reference; it does not identify the internal Nero trigger. The two published gripper STEP files supplied the geometry for the palm and finger lever here. The bimanual leader uses the altered parts supplied with this model.

**Changes.** Each palm has a curved integral J7 mounting bridge with a concentric horn register and four recessed driver holes. The palm hangs forward and below the wrist in the working pose. The adapted handle opens the J8 motor pocket and cable approach, provides radial stop pads, and mates straight to the J7 horn. The adapted finger lever incorporates a stop tab and a relieved underside. The opposite-hand prints mirror the palm and lever. The purchased motor is physically rotated to fit the mirrored shell. Electrical squeeze sign will therefore need calibration per hand. There is one working cable route to the last device in each chain.

| Item per hand | Quantity | Drawing basis |
|---|---:|---|
| Handed palm and finger lever | 1 each | Custom printable STEP/STL, derived from published FACTR geometries |
| J8 XC330-T288-T with included plastic horn | 1 | ROBOTIS solid reference; rear passive idler excluded |
| J7 horn-to-palm fasteners | 4 | 2 × 6 mm plastic tapping screws, head ≤ Ø3.8 × 1.7 mm. Modeled shank engagement in the stock horn is 2.3 mm. |
| J8 motor-case fasteners | 4 | 2 × 10 mm plastic tapping screws, head ≤ Ø3.7 × 1.8 mm. The 3 mm palm wall and 4.5 mm clearance entry leave 2.5 mm of nominal reach into the narrower rear pilot. Check the pilot depth on your motor before seating the screws. |
| Trigger-to-J8-horn fasteners | 4 | 2 × 6 mm plastic tapping screws, head ≤ Ø3.7 × 1.8 mm. Through the 4 mm trigger land, a 6 mm screw enters the stock horn 2 mm. The ROBOTIS horn drawing specifies a 3 mm maximum. |
| J7-to-J8 cable | 1 | TTL connector compatible with XC330-T288-T. Test with the actual plug and loop |

The CAD represents each fastener with a plain head and shank. The screw-tip profile determines how much of the nominal pilot reach carries a full thread. The adapted grip mounting does not require the original FPX330-S102 bracket. The stock J8 horn and J7 horn are installed before the palm and trigger. Orient the trigger horn near the middle of the encoder's useful range before fixing the trigger. The modeled 30° corresponds to about 25.5 mm chord travel at a point 49.2 mm from the hinge. The finger presses the broad edge of the lever. Hand comfort and pinch clearance need a trial with the operator.

Both 8 mm screw callouts in the earlier grip drawing have been corrected. At the rear case an 8 mm screw reached only 0.5 mm into the narrower pilot. At the trigger it reached 4 mm into the horn. The corrected shank lengths and straight driver access were checked at all 16 J8 holes across the two grips. [Per-hole measurements](../Checks/Grip_fastener_fit.csv)

**Mechanical checks.** The trigger and palm have hard stop contact at 0° and 30°. The check sampled both hands every 2° over this range, and deliberately advanced the trigger to −1° and 31°. The forbidden poses produced about 3.01 mm³ of print overlap on each side. The nominal measured trigger-to-case clearance at each endpoint was 0.70 mm. Both J7 mounts cleared a 4.10 mm diameter driver shaft at all four screw positions. J7 face-to-grip contact is intentional, and the print cleared the J7 case by at least 1.75 mm in the three tested roll poses. These checks use nominal rigid CAD. Actual horn seating, front clearance, trigger friction, print stiffness, cable motion and the operator's fingers need physical checks.

[FACTR hardware, commit 081c832e6f3837c0f7d7a20e183d06699cf75262](https://github.com/JasonJZLiu/FACTR_Hardware/tree/081c832e6f3837c0f7d7a20e183d06699cf75262)  
[Original handle and trigger STEP files](https://github.com/JasonJZLiu/FACTR_Hardware/tree/081c832e6f3837c0f7d7a20e183d06699cf75262/CAD_files/STEP_files)  
[Original illustrated gripper assembly](https://github.com/JasonJZLiu/FACTR_Hardware#gripper-teleop-leader)  
[FACTR 2 website, Nero contact video](https://jasonjzliu.com/factr2/)  
[ROBOTIS XC330-T288-T](https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/)

The original FACTR files are by Jason Jingzhou Liu, Yulong Li, Kenneth Shaw, Tony Tao, Ruslan Salakhutdinov and Deepak Pathak. The repository distributes the Apache License 2.0. The complete upstream license accompanies this adaptation.
