
# File formats are described here:
# http://wias-berlin.de/software/tetgen/1.5/doc/manual/manual006.html

def import_tetgen_delaunay_neighbors(fname_neigh):

    neigh_list = import_simple(fname_neigh, 4)

    # Remove -1
    neigh_list = [[neigh for neigh in neighs if neigh != -1] for neighs in neigh_list]

    return neigh_list


def import_simple(fname, length, floats=False):

    objs = []

    # Import
    f = open(fname,"r")

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr != 0 and len(s) > 0 and s[0] != "#":
            if floats:
                vals = [float(x) for x in s[1:1+length]]
            else:
                vals = [int(x) for x in s[1:1+length]]
            objs.append([int(s[0])] + vals)

        line_ctr += 1

    # Close
    f.close()

    # Sort
    objs.sort(key=lambda x: x[0])

    # Strip idxs
    objs = [x[1:] for x in objs]

    return objs



def import_tetgen_delaunay(fname_nodes, fname_edges, fname_faces, fname_elements):

    point_list = import_simple(fname_nodes, 3, floats=True)
    edge_list = import_simple(fname_edges, 2)
    face_list = import_simple(fname_faces, 3)
    tet_list = import_simple(fname_elements, 4)

    return [ point_list, edge_list, face_list, tet_list ]
