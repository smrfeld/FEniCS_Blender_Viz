import numpy as np

def make_subdivided_triangles(vert_list, face_list):

    # New verts, faces, edges
    new_vert_list = []
    new_edge_list = []
    new_face_list = []

    # Init vert list to current
    new_vert_list = vert_list.copy()

    # Pairs done for the Midpoints
    pairs_done_midpoints = []
    pairs_done_midpoints_idxs = []

    for f in face_list:

        # Get the verts
        v0 = vert_list[f[0]]
        v1 = vert_list[f[1]]
        v2 = vert_list[f[2]]

        # Midpoints

        # Index
        idxs01 = sorted([f[0],f[1]])
        # Check not already done
        if not idxs01 in pairs_done_midpoints:
            # Vert
            m01 = [0.5*(v0[j]+v1[j]) for j in range(0,3)]
            new_vert_list.append(m01)
            # Idx
            i01 = len(new_vert_list) - 1
            # Done
            pairs_done_midpoints.append(idxs01)
            pairs_done_midpoints_idxs.append(i01)
        else:
            # Idx
            i01 = pairs_done_midpoints_idxs[pairs_done_midpoints.index(idxs01)]

        # Index
        idxs02 = sorted([f[0],f[2]])
        # Check not already done
        if not idxs02 in pairs_done_midpoints:
            # Vert
            m02 = [0.5*(v0[j]+v2[j]) for j in range(0,3)]
            # Add
            new_vert_list.append(m02)
            i02 = len(new_vert_list) - 1
            # Done
            pairs_done_midpoints.append(idxs02)
            pairs_done_midpoints_idxs.append(i02)
        else:
            # Idx
            i02 = pairs_done_midpoints_idxs[pairs_done_midpoints.index(idxs02)]

        # Index
        idxs12 = sorted([f[1],f[2]])
        # Check not already done
        if not idxs12 in pairs_done_midpoints:
            # Vert
            m12 = [0.5*(v1[j]+v2[j]) for j in range(0,3)]
            new_vert_list.append(m12)
            # Idx
            i12 = len(new_vert_list) - 1
            # Done
            pairs_done_midpoints.append(idxs12)
            pairs_done_midpoints_idxs.append(i12)
        else:
            # Idx
            i12 = pairs_done_midpoints_idxs[pairs_done_midpoints.index(idxs12)]

        # TBD: Triangle circumcenter
        # c = [0.5*(v0.x + v1.x + v2.x)]
        # Currently: average :/
        c = [0.333*(v0[j]+v1[j]+v2[j]) for j in range(0,3)]
        new_vert_list.append(c)
        ic = len(new_vert_list) - 1

        # Faces
        new_face_list.append([f[0],i01,ic,i02])
        new_face_list.append([f[1],i12,ic,i01])
        new_face_list.append([f[2],i12,ic,i02])

        # Edges
        new_edge_list.append(sorted([f[0],i01]))
        new_edge_list.append(sorted([i01,ic]))
        new_edge_list.append(sorted([ic,i02]))
        new_edge_list.append(sorted([i02,f[0]]))

        new_edge_list.append(sorted([f[1],i12]))
        new_edge_list.append(sorted([i12,ic]))
        new_edge_list.append(sorted([ic,i01]))
        new_edge_list.append(sorted([i01,f[1]]))

        new_edge_list.append(sorted([f[2],i12]))
        new_edge_list.append(sorted([i12,ic]))
        new_edge_list.append(sorted([ic,i02]))
        new_edge_list.append(sorted([i02,f[2]]))

    # Delete duplicate edges
    tmp = set(tuple(x) for x in new_edge_list)
    new_edge_list = [ list(x) for x in tmp ]

    # Faces are already guaranteed unique

    return new_vert_list, new_edge_list, new_face_list
