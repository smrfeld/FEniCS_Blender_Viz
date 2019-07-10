
# File formats are described here:
# http://wias-berlin.de/software/tetgen/1.5/doc/manual/manual006.html
# TetGen 1.5.0 has a bug for the Voronoi cell list - its indexes are not correct in the face list
# Use TetGen 1.4.3 instead available here:
# http://wias-berlin.de/software/tetgen/tetgen143.html

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





def import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces):

    # Import points (nodes)
    point_list = import_simple(fname_nodes, 3, floats=True)
    no_points_interior = len(point_list)

    edge_list = []
    face_list = []

    # Import edges
    f = open(fname_edges,"r")

    dist = 1.0

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr == 0:
            # Get how many elements there are
            no_edges = int(s[0])

        elif len(s) == 3 and s[0] != "#":
            edge_list.append([int(s[0]),int(s[1]),int(s[2])])

        elif len(s) > 0 and s[0] != "#":
            # This edge extends to infinity; make a new point some distance away
            idx = int(s[0])
            vert0_idx = int(s[1])
            vert0_pt = point_list[vert0_idx]
            ray = [float(s[3]), float(s[4]), float(s[5])] # s[2] = -1 to indicate boundary
            vert1_pt = [vert0_pt[i] - dist*ray[i] for i in range(0,3)]
            # Add the vert
            vert1_idx = len(point_list)
            point_list.append(vert1_pt)
            edge_list.append([idx, vert0_idx, vert1_idx])

        line_ctr += 1

    # Close
    f.close()

    # Import faces
    f = open(fname_faces,"r")

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr == 0:
            # Get how many elements there are
            no_faces = int(s[0])

        elif len(s) > 0 and s[0] != "#":
            # Remove boundary marker
            if s[-1] == "-1":
                s = s[:-1]

            # 0 = idx
            idx = int(s[0])

            # 1,2 = boundary cells
            # ignore

            # 3 = # edges
            # ignore

            # 4 to end = edges
            edge_idxs = [int(x) for x in s[4:]]
            edge_verts = [edge_list[edge_idx][1:] for edge_idx in edge_idxs]

            # Now get the verts... difficult!

            # Check the orientation of the first two manually - if this is corrected, the rest can be oriented automatically!
            verts = []
            prev_vert = edge_verts[0][1]
            if not prev_vert in edge_verts[1]:
                # Need to flip the first edge verts!
                edge_verts[0].reverse()

            # Add
            verts.append(edge_verts[0][0])
            verts.append(edge_verts[0][1])
            prev_vert = edge_verts[0][1]

            # Orient all the other edges
            for vert_pair in edge_verts[1:]:
                if vert_pair[1] == prev_vert:
                    # Flip
                    vert_pair.reverse()
                # otherwise already correct!

                prev_vert = vert_pair[1]
                verts.append(prev_vert)

            # Do not close
            if verts[0] == verts[-1]:
                verts = verts[:-1]

            face_list.append([idx] + verts)

        line_ctr += 1

    # Close
    f.close()

    # Sort lists
    edge_list.sort(key=lambda x: x[0])
    face_list.sort(key=lambda x: x[0])

    # Strip idxs
    edge_list = [x[1:] for x in edge_list]
    face_list = [x[1:] for x in face_list]

    return [ no_points_interior, point_list, edge_list, face_list ]
