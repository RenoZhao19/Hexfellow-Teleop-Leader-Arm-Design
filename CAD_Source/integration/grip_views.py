"""Two separately openable grip STEP positions, in a common, centered coordinate system."""
import json
from pathlib import Path
import cadquery as cq
import numpy as np
from OCP.gp import gp_Trsf
from compose import ROOT,RELEASE,readlist
from geometry import about,translation
parts=[p for p in readlist(ROOT/'grip'/'manifest.json') if str(p.get('side','left')).lower()=='left']
data=json.loads((ROOT/'grip'/'trigger.json').read_text())['Left']
axis=np.array(data['axis']);point=np.array(data['pivot'])
for key,q in zip(['released','squeezed'],data['limits']):
    asm=cq.Assembly(name='Left_grip_'+key)
    for p in parts:
        shape=cq.Shape.importBrep(p['path']);matrix=translation(-point)
        if p['group']==8:matrix=matrix@about(axis,point,q)
        t=gp_Trsf();t.SetValues(*matrix[:3,:].flatten())
        rgb=(.96,.48,.18) if p['kind']=='print' and p['group']==8 else ((.25,.30,.32) if p['kind']=='print' else (.55,.56,.58))
        asm.add(shape,name=p['name'],color=cq.Color(*rgb),loc=cq.Location(t))
    dest=RELEASE/'Assemblies'/('Grip_'+key+'.step')
    asm.export(str(dest))
    assert len(list(cq.Assembly.load(str(dest))))==len(parts)
    print(dest.name,len(parts),q)
