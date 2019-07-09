import sys
sys.path.append("../fenics_viz")
from import_tetgen import *

if __name__ == "__main__":

    fname_nodes = "sphere.1.v.node"
    fname_edge = "sphere.1.v.edge"
    fname_face = "sphere.1.v.face"
    fname_cell = "sphere.1.v.cell"

    point_list, edge_list, face_list, cell_list = import_tetgen_voronoi(fname_nodes, fname_edge, fname_face, fname_cell)

    print("No points: " + str(len(point_list)))
    print("No faces: " + str(len(face_list)))
    print("No cells: " + str(len(cell_list)))
    print(point_list)
