"""Compose the Nero-inspired bimanual leader from independently authored mechanical CAD."""
import json
from pathlib import Path
import numpy as np
from geometry import PIVOTS, SHAFTS, LIMITS, fk
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'integration'
RELEASE=ROOT/'dist'/'Hexfellow_Nero_Leader'
HOME={'Left':[90,100,90,90,0,0,0], 'Right':[-90,100,-90,90,0,0,0]}

def readlist(manfile):
    data=json.loads(manfile.read_text())
    rows=data if isinstance(data,list) else data['parts']
    for part in rows:
        row=part.copy()
        options=[manfile.parent/row['path'], ROOT/row['path'],Path(row['path'])]
        row['path']=str(next(p for p in options if p.is_file()).resolve())
        row['name']=str(row['name'])
        row['group']=int(row.get('group',0))
        if row.get('kind') not in ['print','stock','purchase']:
            raise ValueError(row)
        yield row

def compose():
    for sub in ['Assemblies','Design','Checks','Parts/Printable_STEP','Parts/Printable_STL','Parts/Metal']:
        (RELEASE/sub).mkdir(parents=True,exist_ok=True)
    frame=list(readlist(ROOT/'frame'/'manifest.json'))
    canonical=[]
    for name in ['frame/root_manifest','arm/manifest','grip/manifest']:
        canonical.extend(readlist(ROOT/(name+'.json')))
    trigger=json.loads((ROOT/'grip'/'trigger.json').read_text())
    posefile=WORK/'posture.json'
    home=json.loads(posefile.read_text()) if posefile.is_file() else HOME
    scenes=[]
    for item in frame:
        scenes.append(dict(item,side='Frame',local_name=item['name'],matrix=np.eye(4).tolist()))
    arms={}
    for side in home:
        local=[r for r in canonical if str(r.get('hand',r.get('side','both'))).lower() in ['both','common',side.lower()]]
        tg=trigger[side]
        angles=home[side]+[tg['home']]
        points=np.vstack([PIVOTS,tg['pivot']])
        axes=np.vstack([SHAFTS,tg['axis']])
        transforms=fk(side,angles,points,axes)
        arms[side]=dict(angles=angles,points=points.tolist(),axes=axes.tolist(),limits=LIMITS+[tg['limits']])
        for item in local:
            g=item['group']
            scenes.append(dict(item,side=side,name=(item['name'] if item['name'].startswith(side+'_') else f"{side}_{item['name']}"),local_name=item['name'],matrix=transforms[g].tolist()))
    if len({p['name'] for p in scenes})!=len(scenes):
        raise ValueError('Repeated component occurrence labels')
    (WORK/'scene.json').write_text(json.dumps({'parts':scenes,'arms':arms},indent=2))
    return scenes

if __name__=='__main__':
    print(len(compose()),'component occurrences')
