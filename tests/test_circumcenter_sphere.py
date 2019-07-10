import sys
sys.path.append("../fenics_viz")
from voronoi_from_delaunay import *

if __name__ == "__main__":

    p1 = [3, 2, 1]
    p2 = [1, -2, -3]
    p3 = [2, 1 ,3]
    p4 = [-1, 1, 2]

    x_center, y_center, z_center = circumcenter_sphere_from_pts(p1, p2, p3, p4)
    print([x_center, y_center, z_center])
