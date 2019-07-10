import sys
sys.path.append("../fenics_viz")
from import_tetgen import *

if __name__ == "__main__":

    neighs = import_tetgen_delaunay_neighbors("sphere.1.neigh")
    print(neighs)
