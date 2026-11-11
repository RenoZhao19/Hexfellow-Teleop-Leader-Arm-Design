"""Nominal arm-frame kinematics for assembly export. Coordinates in mm, angles in degrees."""
import numpy as np
from scipy.spatial.transform import Rotation

PIVOTS=np.array([[0,0,0],[9.75,0,94.445],[9.75,0,192],[9.75,0,286.52],[9.75,0,373],[9.75,0,458.445],[32.75,0,458.445]])
SHAFTS=np.array([[0,0,1],[0,1,0],[0,0,-1],[0,1,0],[0,0,-1],[0,-1,0],[1,0,0]])
LIMITS=[(-160,160),(-70,125),(-160,160),(-60,125),(-160,160),(-50,50),(-45,45)]
MOUNT_SPAN=130.0
MOUNT_Z=560.0

def translation(vector):
    m=np.eye(4);m[:3,3]=vector
    return m

def about(axis,point,angle):
    m=np.eye(4)
    m[:3,:3]=Rotation.from_rotvec(np.array(axis)*np.deg2rad(angle)).as_matrix()
    m[:3,3]=point-m[:3,:3]@point
    return m

def mount(side):
    s=1 if side=='Left' else -1
    return translation([0,s*MOUNT_SPAN/2,MOUNT_Z])@about([1,0,0],np.zeros(3),-s*90)

def fk(side,angles,points=PIVOTS,axes=SHAFTS):
    out=[mount(side)]
    for p,a,q in zip(points,axes,angles):
        out.append(out[-1]@about(a,p,q))
    return out

def xyz(m,p):
    return m[:3,:3]@p+m[:3,3]

if __name__=='__main__':
    for q in [[90,110,90,90,0,0,0],[85,102,70,90,0,0,0],[90,95,90,88,0,0,0],[80,100,55,90,0,0,0],[80,110,58,90,0,0,0]]:
        f=fk('Left',q)
        print(q, [np.round(xyz(f[i],PIVOTS[i]),1).tolist() for i in [1,3,5,6]],'end +X',np.round(f[7][:3,0],2))
