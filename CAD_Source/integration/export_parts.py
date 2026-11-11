"""Export BOM and printable part solids in standalone coordinates, then check each STL."""
import csv, json, re, sys
from collections import Counter, defaultdict
from release_paths import WORK, RELEASE as target
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as F,Part,Mesh,MeshPart
def weld_boundary_slivers(mesh, tolerance=0.00003):
    # OCC can split a single vertex at the seam between a fillet and its tangent face.
    # Merge only vertices on a boundary edge shorter than 30 nanometres.
    vertices, triangles = mesh.Topology
    edges = Counter(tuple(sorted(edge)) for face in triangles for edge in zip(face, face[1:] + face[:1]))
    replace = {b: a for (a,b),count in edges.items() if count == 1 and (vertices[a] - vertices[b]).Length < tolerance}
    if not replace:
        return mesh
    faces = [tuple(replace.get(i,i) for i in face) for face in triangles]
    return Mesh.Mesh((vertices,[f for f in faces if len(set(f)) == 3]))

def purchase_note(part):
    name = part['local_name']
    if name.startswith('F05_'):
        return 'Each occurrence is one M6 crossbolt, two washers and one nut.'
    if re.fullmatch(r'F[1-6]_Exterior_fasteners', name):
        return 'Each occurrence groups the fasteners at one arm interface. See Design/Hardware_buying_guide.md for individual order quantities.'
    if name.endswith(('XC330_horn', 'J8_XC330_T288T_horn')):
        return 'ROBOTIS stock plastic XC330 horn and factory axial screw'
    if name.endswith('J8_XC330_T288T_case'):
        return 'ROBOTIS XC330-T288-T'
    shoulder = {
        'J1_XM430_fixed_case': 'ROBOTIS XM430-W210-T',
        'J1_XM430_drive_horn': 'ROBOTIS HN12-N101 driven horn and factory retainer',
        'J1_Drum_mount_M4x14': 'Each occurrence contains four M4 x 14 button-head screws.',
        'J1_Torso_M4_inserts': 'Each occurrence contains four short M4 heat-set inserts.',
        'J1_Case_mount_M25x7': 'Each occurrence contains four M2.5 x 7 case-mount screws.',
        'J1_Horn_drive_screws_M2x6': 'Each occurrence contains four M2 x 6 horn screws.',
        'J1_Saddle_screws_M3x10': 'Each occurrence contains three M3 x 10 saddle screws.',
        'J1_Saddle_captive_nuts_M3': 'Each occurrence contains three DIN 934 M3 plain hex nuts, 5.5 mm across flats x 2.4 mm high.',
    }
    return shoulder.get(name) or part.get('vendor') or part.get('hardware_notes') or part.get('note') or 'Purchased reference geometry'

parts=json.loads((WORK/'scene.json').read_text())['parts']
grouped=defaultdict(list)
for p in parts:
    ident=p.get('part_id',p.get('sku',p['local_name']))
    if str(ident).startswith('F04_Mast_sleeve_'):
        ident='F04_Mast_sleeve_36mm'
    grouped[(p['kind'],ident)].append(p)
with (target/'Design'/'CAD_parts_and_quantities.csv').open('w', newline='') as out:
    writer=csv.writer(out);writer.writerow(['Part ID','Total occurrences','Type','File','X mm','Y mm','Z mm','CAD cm3','Notes'])
    for (kind,part_id),items in sorted(grouped.items()):
        p=items[0];name=re.sub('[^A-Za-z0-9_-]+','_',str(part_id)).strip('_')
        if kind=='purchase':
            writer.writerow([part_id,len(items),kind,'','','','','',purchase_note(p)]);continue
        shape=Part.read(p['path'])
        if not shape.isValid() or len(shape.Solids)!=1:
            raise RuntimeError(('expected one valid manufactured body',p['name'],len(shape.Solids),shape.isValid()))
        s=shape.Solids[0].copy()
        b=s.BoundBox;s.translate(F.Vector(-b.Center.x,-b.Center.y,-b.ZMin))
        folder='Parts/Printable_STEP' if kind=='print' else 'Parts/Metal'
        f=target/folder/(name+'.step')
        f.parent.mkdir(parents=True,exist_ok=True);s.exportStep(str(f))
        back=Part.read(str(f));assert back.isValid() and len(back.Solids)==1 and abs(back.Volume-s.Volume)<max(.1,s.Volume*.0005)
        if kind=='print':
            stl=target/'Parts/Printable_STL'/(name+'.stl')
            for chord,ang in [(.06,.17),(.04,.13),(.10,.22),(.12,.21)]:
                mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=chord,AngularDeflection=ang,Relative=False)
                mesh.removeDuplicatedPoints();mesh.removeDuplicatedFacets();mesh.fixDegenerations();mesh.harmonizeNormals()
                if not mesh.isSolid(): mesh=weld_boundary_slivers(mesh)
                mesh.write(str(stl))
                check=Mesh.Mesh(str(stl))
                if check.isSolid() and not check.hasNonManifolds() and check.countComponents()==1 and abs(abs(check.Volume)-s.Volume)<.006*s.Volume:
                    break
            else: raise ValueError(('STL QA',name,check.isSolid(),check.hasNonManifolds(),check.countComponents()))
        # Measure the exported surface. The loose control-point box can substantially overstate print size.
        bounds=back.optimalBoundingBox(False)
        writer.writerow([part_id,len(items),kind,str(f.relative_to(target)),*[round(a,2) for a in (bounds.XLength,bounds.YLength,bounds.ZLength,s.Volume/1000)],p.get('material') or p.get('note','')]);print('Verified',kind,name,len(items),flush=True)
