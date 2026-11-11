"""Export the full and individual arm STEP files and round-trip their instances and placements."""
import json
from functools import lru_cache
from pathlib import Path
import cadquery as cq
import numpy as np
from OCP.gp import gp_Trsf

from compose import RELEASE, WORK

@lru_cache(None)
def shape(path):
    value=cq.Shape.importBrep(path)
    assert value.Solids(), path
    return value

def as_loc(matrix):
    m=np.asarray(matrix)
    assert np.allclose(m[:3,:3].T@m[:3,:3],np.eye(3))
    assert np.isclose(np.linalg.det(m[:3,:3]),1)
    trsf=gp_Trsf()
    trsf.SetValues(*m[:3,:].ravel())
    return cq.Location(trsf)

def colour(p):
    name=p['local_name'].lower()
    if p['kind']=='print':
        if 'trigger' in name:return '#E97725'
        if p.get('external_shoulder') and p['group']==1 and any(s in name for s in ('faceplate','face_plate','rotating_plate','drive_plate','rotor_plate')):return '#B86E3C'
        if p.get('external_shoulder') and p['group']==0:return '#41474C'
        return '#383E42' if p['side']=='Frame' else '#3B4449'
    if 'insert' in name:return '#B99355'
    if p['kind']=='stock':return '#9CA2A6'
    if any(s in name for s in ('horn','idler')) and 'screw' not in name:return '#7B8287'
    if any(s in name for s in ('case','xm430','xc330')) and not any(s in name for s in ('screw','bolt','fastener','mount_')):return '#3D454A'
    return '#70777C'

def subgroup(p):
    if p['side']=='Frame':return 'Frame_and_mast'
    if p.get('external_shoulder') or p['local_name'].startswith(('M2_XM430','F1_Exterior','L2_Upper')):return p['side']+'_shoulder'
    if p['group']>=7:return p['side']+'_grip'
    return p['side']+'_arm'

def build(rows, target, name):
    top=cq.Assembly(name=name)
    groups={}
    for row in rows:
        group=subgroup(row)
        if group not in groups:groups[group]=cq.Assembly(name=group)
        groups[group].add(shape(row['path']), name=row['name'],loc=as_loc(row['matrix']),color=cq.Color(colour(row)))
    for child in groups.values():top.add(child)
    top.export(str(target))

def verify(rows, target):
    loaded=cq.Assembly.load(str(target))
    parts_by_name={p['name']:p for p in rows}
    occurrences=list(loaded)
    assert len(occurrences)==len(rows)
    largest=0.
    seen=set()
    for item,pathname,loc,color in occurrences:
        name=pathname.split('/')[-1]
        assert name not in seen,pathname
        # OCCT restores a multipart purchased component's appearance on its constituent solids.
        if len(item.Solids())==1:assert color is not None,pathname
        seen.add(name)
        row=parts_by_name[name]
        original=shape(row['path']); m=np.asarray(row['matrix'])
        expect=m@np.array([*original.Center().toTuple(),1.])
        returned=item.moved(loc)
        error=np.linalg.norm(expect[:3]-np.array(returned.Center().toTuple()))
        largest=max(largest,error)
        assert len(item.Solids())==len(original.Solids()),name
        assert abs(item.Volume()-original.Volume())<max(.2,1e-4*abs(original.Volume())),name
        assert error<.02,(name,error)
    assert seen==set(parts_by_name)
    print('Round-trip verified',len(seen),'named occurrences. Maximum centroid drift',largest,'mm. Bytes',target.stat().st_size,flush=True)

if __name__ == '__main__':
    parts = json.loads((WORK/'scene.json').read_text())['parts']
    assemblies = (
        ('Bimanual_leader', 'Hexfellow_External_Drum_Leader', parts),
        ('Left_leader', 'Left_leader', [p for p in parts if p['side'] == 'Left']),
        ('Right_leader', 'Right_leader', [p for p in parts if p['side'] == 'Right']),
    )
    for filename, label, rows in assemblies:
        target = RELEASE/'Assemblies'/(filename+'.step')
        build(rows, target, label)
        verify(rows, target)
