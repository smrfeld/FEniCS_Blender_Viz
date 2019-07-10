from . import circumcenter_sphere
import numpy as np

# TetGen 1.5.1 has a bug where the cell list produced is incorrect
# If we start with a constrained surface mesh (i.e. constrained delaunay)
# Reconstruct manually which faces belong to which cells!

def make_cell_list(voronoi_no_verts_interior, voronoi_vert_list, voronoi_face_list, delaunay_vert_list, delaunay_edge_list, delaunay_tet_list):

    cell_list = []

    # Recreate the circumcenters from the sphere
    circumcenters = []
    for tet in delaunay_tet_list:
        pts = [delaunay_vert_list[v] for v in tet]
        circumcenters.append(circumcenter_sphere.circumcenter_sphere_from_pt_list(pts))
    circumcenters = np.array(circumcenters)

    # Each cirucmcenter corresponds to some point in the voronoi_vert_list
    # Establish this correspondence
    voronoi_vert_arr_interior = np.array(voronoi_vert_list[:voronoi_no_verts_interior])
    circumcenter_to_voronoi_vert = {}
    for idx_circumcenter in range(0,len(circumcenters)):
        c = circumcenters[idx_circumcenter]

        # Get the closest
        dr = c - voronoi_vert_arr_interior
        dists_squared = np.sum(dr*dr, axis=1)

        # Min
        idx_voronoi = np.argmin(dists_squared)

        # Store
        circumcenter_to_voronoi_vert[idx_circumcenter] = idx_voronoi

    # Each vert in delaunay gets one cell in voronoi
    for i_vert_delaunay in range(0,len(delaunay_vert_list)):

        # Get all edges attached to this vertex
        delaunay_edges_connected = []
        for i_edge in range(0,len(delaunay_edge_list)):
            edge = delaunay_edge_list[i_edge]

            # Check if edge involves this vert
            if i_vert_delaunay in edge:
                delaunay_edges_connected.append(i_edge)

        cell_faces = []

        # Go through each edge
        for i_edge in delaunay_edges_connected:
            edge = delaunay_edge_list[i_edge]

            # Get all tets that share this edge
            delaunay_tets_connected = []
            for i_tet in range(0,len(delaunay_tet_list)):
                if edge[0] in delaunay_tet_list[i_tet] and edge[1] in delaunay_tet_list[i_tet]:
                    delaunay_tets_connected.append(i_tet)

            if len(delaunay_tets_connected) == 2:
                print("This edge is on the boundary in the Delaunay mesh; skip")
                continue

            # Each tet corresponds -> a circumcenter -> an index in the voronoi mesh
            voronoi_verts = sorted([circumcenter_to_voronoi_vert[tet] for tet in delaunay_tets_connected])
            print("For voronoi cell: " + str(i_vert_delaunay) + " constructed face for edge: " + str(i_edge) + " whose verts are: " + str(voronoi_verts) + " and cutoff is: " + str(voronoi_no_verts_interior))

            # These verts (in some ordering) form a single face
            # Find the face that has all these verts
            for i_face in range(0,len(voronoi_face_list)):
                face = voronoi_face_list[i_face]
                if sorted(face) == voronoi_verts:
                    # This face belongs to this voronoi cell
                    cell_faces.append(i_face)
                    break

        # Store
        cell_list.append(cell_faces)

    # Check: each face should appear exactly twice!
    counts = {}
    for i_face in range(0,len(voronoi_face_list)):
        counts[i_face] = 0
    for cell in cell_list:
        for face in cell:
            counts[face] += 1
    print(counts)
    for count in counts.values():
        if count != 2:
            print("Warning! Not right")
            break

    print(cell_list)

    return cell_list
