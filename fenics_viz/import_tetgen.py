
# File formats are described here:
# http://wias-berlin.de/software/tetgen/1.5/doc/manual/manual006.html

# def import_tetgen_delaunay(fname_nodes, fname_edges, fname_faces, fname_elements):

def import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces, fname_cells):

    point_list = []
    edge_list = []
    face_list = []
    cell_list = []

    # Import points (nodes)
    f = open(fname_nodes,"r")

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr == 0:
            # Get how many elements there are
            no_points = int(s[0])

        elif len(s) > 0 and s[0] != "#":
            point_list.append([int(s[0]),float(s[1]),float(s[2]),float(s[3])])

        line_ctr += 1

    # Close
    f.close()

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
            print(idx)
            print(ray)
            print(vert0_pt)
            vert1_pt = [vert0_pt[i+1] - dist*ray[i] for i in range(0,3)] # i+1 because 0 element is the idx
            print(vert1_pt)
            # Add the vert
            vert1_idx = len(point_list)
            point_list.append([vert1_idx] + vert1_pt)
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

    # Import cells
    f = open(fname_cells,"r")

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr == 0:
            # Get how many elements there are
            no_cells = int(s[0])

        elif len(s) > 0 and s[0] != "#":
            if s[-1] == "-1":
                s = s[:-1]
            cell_list.append(tuple([int(x) for x in s]))

        line_ctr += 1

    # Close
    f.close()

    # Sort lists
    point_list.sort(key=lambda x: x[0])
    edge_list.sort(key=lambda x: x[0])
    face_list.sort(key=lambda x: x[0])
    cell_list.sort(key=lambda x: x[0])

    return [ point_list, edge_list, face_list, cell_list ]
