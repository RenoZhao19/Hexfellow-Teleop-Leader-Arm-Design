Rebuild the external-drum Hexfellow leader

The published STEP, STL and FreeCAD files open directly. The scripts in this
directory rebuild their geometry from the two original ROBOTIS actuator
assemblies and the supplied FACTR handle and trigger. The vendor filenames,
download pages and SHA-256 digests are in arm/vendor/Required_input_files.txt.
The FACTR license and attribution are in the repository's Design directory.

Run these commands from CAD_Source. "python" below has CadQuery 2.7, NumPy
and SciPy. "/usr/bin/python3" is the Debian interpreter for FreeCAD's Part,
Mesh and MeshPart modules. On another system use the interpreter and library
path for your OpenCascade/FreeCAD installation. All CAD dimensions are mm.

  python arm/design_arm.py
  /usr/bin/python3 grip/build.py
  /usr/bin/python3 frame/source/frame.py
  python frame/source/rotating_shoulder.py
  python integration/compose.py

frame.py makes the torso, foot, drilled mast, spacer sleeves and pin hardware,
then invokes fixed_shoulder.py to make the external drum and partition the
actual X430 model into its fixed case and rotating horn. rotating_shoulder.py
makes the faceplate, J2 saddle and their screws and nuts. Each generator writes
its own intermediate solids and manifest. compose.py places each occurrence
in the same coordinate frame as the released bimanual STEP. The release pose
uses the default joint angles in compose.py. If experimenting with a local
integration/posture.json, remove it to reproduce the released pose.

  /usr/bin/python3 frame/source/check_shoulder_fasteners.py
  /usr/bin/python3 grip/check_grip_fasteners.py
  /usr/bin/python3 integration/export_parts.py
  python integration/export_assemblies.py
  /usr/bin/python3 integration/poseable.py
  python integration/grip_views.py

The export directory is dist/Hexfellow_External_Drum_Leader. export_parts.py checks the
printable meshes and writes the part inventory. export_assemblies.py verifies
names, solid counts, volumes and placements after STEP reimport. poseable.py
reopens the generated native assembly and exercises J1, J2, J4 and J8 on both
arms. Open Assemblies/Poseable_leader.FCStd and edit the JointAngle property
of a joint to inspect movement. Each side STEP contains that arm's components
at assembly coordinates. See Checks in the repository for the scope of the
geometry checks, and the installation and purchasing guides for hardware.
