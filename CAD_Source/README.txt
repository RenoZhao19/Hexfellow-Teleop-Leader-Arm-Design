Editable geometry sources

The supplied STEP, STL and FreeCAD files open independently of these source scripts. This folder is for someone changing the design parameters or regenerating solids. It contains CAD generation code only.

The unchanged FACTR source handle and trigger STEP files in grip/ are inputs to the adapted hand generator. The full attribution and Apache License 2.0 are in the package's Design directory. Download the matching ROBOTIS originals under arm/vendor as described in Required_input_files.txt before regeneration.

Use CadQuery 2.7 with numpy and scipy for the arm, geometry composition and STEP exchange, and a Python interpreter with FreeCAD Part, Mesh and MeshPart for the frame, grip and native FreeCAD assembly. The source layout used Debian FreeCAD with /usr/lib/freecad/lib on its Python path. Set that path appropriately for another installation.

Regenerate arm/design_arm.py, frame/source/frame.py and grip/build.py first. They write the component manifests and solids. Run integration/compose.py next to assemble the checked geometric data. Then run integration/export_parts.py, export_assemblies.py, poseable.py and grip_views.py with the matching interpreter. Outputs go under CAD_Source/dist/Hexfellow_Nero_Leader. Recheck attachment holes, kinematics, interference, trigger travel and load estimates after geometry edits. The included verification results apply to the supplied revision.
