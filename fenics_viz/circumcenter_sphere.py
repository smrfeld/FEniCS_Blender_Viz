
# See here
# https://math.stackexchange.com/questions/894794/sphere-equation-given-4-points

def circumcenter_sphere_from_pt_list(pts):
    return circumcenter_sphere_from_pts(pts[0],pts[1],pts[2],pts[3])

def circumcenter_sphere_from_pts(p1, p2, p3, p4):
    return circumcenter_sphere_from_pt_coords(p1[0],p1[1],p1[2],p2[0],p2[1],p2[2],p3[0],p3[1],p3[2],p4[0],p4[1],p4[2])

def circumcenter_sphere_from_pt_coords(p1x, p1y, p1z, p2x, p2y, p2z, p3x, p3y, p3z, p4x, p4y, p4z):
    r1s = pow(p1x,2)+pow(p1y,2)+pow(p1z,2)
    r2s = pow(p2x,2)+pow(p2y,2)+pow(p2z,2)
    r3s = pow(p3x,2)+pow(p3y,2)+pow(p3z,2)
    r4s = pow(p4x,2)+pow(p4y,2)+pow(p4z,2)

    ax2 = -p1x*p2z*p3y+p1x*p2y*p3z+p2z*p3y*p4x-p2y*p3z*p4x+p1x*p2z*p4y-p2z*p3x*p4y-p1x*p3z*p4y+p2x*p3z*p4y+p1z*( p2x*p3y-p3y*p4x+p2y*( -p3x+p4x )-p2x*p4y+p3x*p4y )+( -p1x*p2y+p2y*p3x+p1x*p3y-p2x*p3y )*p4z+p1y*( p2z*p3x-p2x*p3z-p2z*p4x+p3z*p4x+p2x*p4z-p3x*p4z )

    bx = p3z*p4y*r1s-p3y*p4z*r1s-p1z*p3y*r2s+p1y*p3z*r2s+p1z*p4y*r2s-p3z*p4y*r2s-p1y*p4z*r2s+p3y*p4z*r2s-p1z*p4y*r3s+p1y*p4z*r3s+p1z*p3y*r4s-p1y*p3z*r4s+p2z*(-p4y*r1s-p1y*r3s+p4y*r3s+p3y*(r1s-r4s)+p1y*r4s)+p2y*(-p3z*r1s+p4z*r1s+p1z*r3s-p4z*r3s-p1z*r4s+p3z*r4s)

    ay2 = -p1x*p2z*p3y+p1x*p2y*p3z+p2z*p3y*p4x-p2y*p3z*p4x+p1x*p2z*p4y-p2z*p3x*p4y-p1x*p3z*p4y+p2x*p3z*p4y+p1z*(p2x*p3y-p3y*p4x+p2y*(-p3x+p4x)-p2x*p4y+p3x*p4y)+(-p1x*p2y+p2y*p3x+p1x*p3y-p2x*p3y)*p4z+p1y*(p2z*p3x-p2x*p3z-p2z*p4x+p3z*p4x+p2x*p4z-p3x*p4z)

    by = -p3z*p4x*r1s+p3x*p4z*r1s+p1z*p3x*r2s-p1x*p3z*r2s-p1z*p4x*r2s+p3z*p4x*r2s+p1x*p4z*r2s-p3x*p4z*r2s+p1z*p4x*r3s-p1x*p4z*r3s-p1z*p3x*r4s+p1x*p3z*r4s+p2x*(p3z*r1s-p4z*r1s-p1z*r3s+p4z*r3s+p1z*r4s-p3z*r4s)+p2z*(p4x*r1s+p1x*r3s-p4x*r3s-p1x*r4s+p3x*(-r1s+r4s))

    az2 = -p1x*p2z*p3y+p1x*p2y*p3z+p2z*p3y*p4x-p2y*p3z*p4x+p1x*p2z*p4y-p2z*p3x*p4y-p1x*p3z*p4y+p2x*p3z*p4y+p1z*(p2x*p3y-p3y*p4x+p2y*(-p3x+p4x)-p2x*p4y+p3x*p4y)+(-p1x*p2y+p2y*p3x+p1x*p3y-p2x*p3y)*p4z+p1y*(p2z*p3x-p2x*p3z-p2z*p4x+p3z*p4x+p2x*p4z-p3x*p4z)

    bz = p3y*p4x*r1s-p3x*p4y*r1s-p1y*p3x*r2s+p1x*p3y*r2s+p1y*p4x*r2s-p3y*p4x*r2s-p1x*p4y*r2s+p3x*p4y*r2s-p1y*p4x*r3s+p1x*p4y*r3s+p1y*p3x*r4s-p1x*p3y*r4s+p2y*(-p4x*r1s-p1x*r3s+p4x*r3s+p3x*(r1s-r4s)+p1x*r4s)+p2x*(-p3y*r1s+p4y*r1s+p1y*r3s-p4y*r3s-p1y*r4s+p3y*r4s)

    dx = - bx / (2.0 * ax2)
    dy = - by / (2.0 * ay2)
    dz = - bz / (2.0 * az2)

    return [dx, dy, dz]
