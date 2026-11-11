"""Write colored STEP assemblies from the checked occurrences and verify the interchange."""
import json,re,sys
from functools import lru_cache
from pathlib import Path
import cadquery as cq
import numpy as np
from OCP.gp import gp_Trsf
from compose import RELEASE,WORK
rows=json.loads((WORK/'scene.json').read_text())['parts']

@lru_cache(None)
def brep(path):
    shape=cq.Shape.importBrep(path)
    if not shape.Solids():
        raise ValueError(path)
    return shape

def location(matrix):
    m=np.array(matrix)
    assert np.allclose(m[:3,:3].T @ m[:3,:3],np.eye(3))
    t=gp_Trsf()
    t.SetValues(*m[:3,:].flatten())
    return cq.Location(t)

def color(p):
    if 'trigger' in p['local_name'].lower() and p['kind']=='print':
        return cq.Color(0.94,0.51,0.20)
    rgb={'print':(0.25,0.30,0.33),'stock':(0.57,0.60,0.62),'purchase':(0.39,0.40,0.41)}[p['kind']]
    return cq.Color(*rgb)

for assembly,selection in {'Bimanual_leader':rows,'Left_leader':[p for p in rows if p['side']=='Left'],'Right_leader':[p for p in rows if p['side']=='Right']}.items():
    target=RELEASE/'Assemblies'/(assembly+'.step')
    a=cq.Assembly(name=assembly)
    for p in selection:
        name=re.sub('[^a-zA-Z0-9_]+','_',p['name'])
        a.add(brep(p['path']),name=name,color=color(p),loc=location(p['matrix']))
    a.export(str(target))
    back=cq.Assembly.load(str(target))
    entities=list(back)
    assert len(entities)==len(selection),(assembly,len(entities),len(selection))
    originals={re.sub('[^a-zA-Z0-9_]+','_',p['name']):p for p in selection}
    errors=[]
    for shape,full_name,loc,_ in entities:
        item=originals[full_name.split('/')[-1]]
        expected=brep(item['path']).Center().toTuple()
        world=np.array(item['matrix'])@np.array([*expected,1.0])
        actual=np.array(shape.moved(loc).Center().toTuple())
        errors.append(np.linalg.norm(world[:3]-actual))
    worst=max(errors)
    if worst>.03:raise ValueError((assembly,'STEP centroid errors',worst))
    print(f'{assembly} maximum imported centroid error {worst:.6g} mm',flush=True)
    print(assembly,len(selection),target.stat().st_size,flush=True)
