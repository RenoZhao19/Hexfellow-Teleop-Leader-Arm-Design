"""Exterior purchased fastener geometry. Shanks inside vendor housings are omitted."""
import math
import cadquery as cq

def hardware_groups(a):
    V=a.V
    groups={k:[] for k in range(1,7)}
    def envelope(p,d,r,h):return a.cyl(p,d,r,h)
    def xc_screws(j,t):
        for x in (-8.,8.):
            for y in (-22.5,7.5):
                groups[j-1].append(envelope((x,y,-23.7),(0,0,-1),2.15,1.7).moved(t))
        if j!=7:
            for x,y in [(6,0),(0,6),(-6,0),(0,-6)]:
                groups[j].append(envelope((x,y,10.7),a.Z,2.15,1.7).moved(t))
    for j,pitch in [(2,a.Z2),(4,a.Z4)]:
        for xx in (a.C-28,a.C-4):
            for yy in (-6,6):
                groups[j-1].append(envelope((xx,yy,pitch-18.55),(0,0,-1),2.55,2.3))
        for sign in (-1,1):
            for ang in (45,135,225,315):
                x=a.C+8*math.cos(math.radians(ang));z=pitch+8*math.sin(math.radians(ang))
                groups[j].append(envelope((x,sign*23.35,z),(0,sign,0),2.1,1.5))
        for z in (pitch+27,pitch+39):
            x=a.C+4.8
            loc=a.loc((x,29,z),a.X,a.Y)
            nut=cq.Workplane('XY').polygon(6,6.35).extrude(4.0).val().moved(loc)
            groups[j]+=[a.union([envelope((x,19.5,z),a.Y,1.5,16),
                                 envelope((x,19.5,z),a.Y,3.5,.5),
                                 envelope((x,28.5,z),a.Y,3.5,.5),
                                 envelope((x,17.75,z),a.Y,2.85,1.75),nut])]
    for j,T in [(3,a.xc_roll(a.Z3)),(5,a.xc_roll(a.Z5)),(6,a.xc_pitch()),(7,a.xc_last())]:
        xc_screws(j,T)
    return groups
