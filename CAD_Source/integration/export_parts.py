"""Export BOM and printable part solids in standalone coordinates, then check each STL."""
import csv,json,os,re,sys
from collections import defaultdict
from pathlib import Path
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as F,Part,Mesh,MeshPart
root=Path(__file__).resolve().parents[1]; target=root/'dist'/'Hexfellow_Nero_Leader'
parts=json.loads((root/'integration'/'scene.json').read_text())['parts']
grouped=defaultdict(list)
for p in parts:
    ident=p.get('part_id',p.get('sku',p['local_name']))
    if str(ident).startswith('F04_Mast_sleeve_'):
        ident='F04_Mast_sleeve_36mm'
    grouped[(p['kind'],ident)].append(p)
with (target/'Design'/'CAD_parts_and_quantities.csv').open('w') as out:
    writer=csv.writer(out);writer.writerow(['Part ID','Total occurrences','Type','File','X mm','Y mm','Z mm','CAD cm3','Notes'])
    for (kind,part_id),items in sorted(grouped.items()):
        p=items[0];name=re.sub('[^A-Za-z0-9_-]+','_',str(part_id)).strip('_')
        if kind=='purchase':
            writer.writerow([part_id,len(items),kind,'','','','','',p.get('vendor') or p.get('hardware_notes') or p.get('note','Purchased reference geometry')]);continue
        shape=Part.read(p['path'])
        if not shape.isValid() or len(shape.Solids)!=1:
            raise RuntimeError(('expected one valid manufactured body',p['name'],len(shape.Solids),shape.isValid()))
        s=shape.Solids[0].copy()
        b=s.BoundBox;s.translate(F.Vector(-b.Center.x,-b.Center.y,-b.ZMin))
        folder='Parts/Printable_STEP' if kind=='print' else 'Parts/Metal'
        f=target/folder/(name+'.step')
        f.parent.mkdir(parents=True,exist_ok=True);s.exportStep(str(f))
        back=Part.read(str(f));assert back.isValid() and len(back.Solids)==1 and abs(back.Volume-s.Volume)<max(.1,s.Volume*.0001)
        if kind=='print':
            stl=target/'Parts/Printable_STL'/(name+'.stl')
            for chord,ang in [(.06,.17),(.04,.13),(.10,.22),(.12,.21)]:
                mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=chord,AngularDeflection=ang,Relative=False)
                mesh.removeDuplicatedPoints();mesh.removeDuplicatedFacets();mesh.fixDegenerations();mesh.harmonizeNormals();mesh.write(str(stl))
                check=Mesh.Mesh(str(stl))
                if check.isSolid() and not check.hasNonManifolds() and check.countComponents()==1 and abs(abs(check.Volume)-s.Volume)<.006*s.Volume:
                    break
            else: raise ValueError(('STL QA',name,check.isSolid(),check.hasNonManifolds(),check.countComponents()))
        writer.writerow([part_id,len(items),kind,str(f.relative_to(target)),*[round(a,2) for a in (b.XLength,b.YLength,b.ZLength,s.Volume/1000)],p.get('material') or p.get('note','')]);print('Verified',kind,name,len(items),flush=True)
