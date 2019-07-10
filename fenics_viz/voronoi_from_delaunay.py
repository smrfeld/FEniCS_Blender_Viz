
from . import circumcenter_sphere

def get_edges_connected_to_vert(i_vert, edge_list):

    edges_connected_to_vert = []
    for i_edge in range(0,len(edge_list)):
        edge = edge_list[i_edge]
        if i_vert in edge:
            edges_connected_to_vert.append(i_edge)

    return edges_connected_to_vert

def get_tets_connected_to_edge(edge, tet_list):

    tets_connected_to_edge = []
    for i_tet in range(0,len(tet_list)):
        tet = tet_list[i_tet]
        if edge[0] in tet and edge[1] in tet:
            tets_connected_to_edge.append(i_tet)

    return tets_connected_to_edge

def order_tet_list_into_loop_by_neighbors(tets, tet_neighbors):

    # Strategy:
    # Pick a random starting tet, go around according to the neighbors
    # Watch out for the edge! In this case, reverse the chain and try again
    tets_ordered = []

    # Start
    local_idx = 0
    i_tet_last = tets[local_idx]
    neighbors_last = tet_neighbors[i_tet_last]
    tets_ordered.append(i_tet_last)
    del tets[local_idx]
    # print("      Ordering init: " + str(tets_ordered) + " remaining: " + str(tets) + " neighbors last: " + str(neighbors_last))

    # Go through remaining
    while len(tets) > 0:
        # Get a connected tet
        did_get_a_new_tet = False
        for local_idx in range(0,len(tets)):
            i_tet = tets[local_idx]
            if i_tet in neighbors_last:
                # Connected
                i_tet_last = tets[local_idx]
                neighbors_last = tet_neighbors[i_tet_last]
                tets_ordered.append(i_tet_last)
                del tets[local_idx]
                # print("      Ordering added: " + str(tets_ordered) + " remaining: " + str(tets) + " neighbors last: " + str(neighbors_last))
                # Next!
                did_get_a_new_tet = True
                break

        # Check if we hit the edge
        if did_get_a_new_tet == False and len(tets) != 0:
            # We hit the edge
            # Solution: reverse the list to add tets to the other side!
            tets_ordered.reverse()
            i_tet_last = tets_ordered[-1]
            neighbors_last = tet_neighbors[i_tet_last]
            # print("      Hit an edge; reversed: " + str(tets_ordered) + " remaining: " + str(tets) + " neighbors last: " + str(neighbors_last))

    return tets_ordered

def voronoi_from_delaunay(vert_list, edge_list, tet_list, tet_neighbors):

    print(tet_neighbors)

    # Go through all tets, get circumcenters
    circumcenters = []
    for tet in tet_list:
        pts = [vert_list[v] for v in tet]
        circumcenters.append(circumcenter_sphere.circumcenter_sphere_from_pt_list(pts))

    # Go through all verts; each gets a cell
    faces_for_each_cell = []
    verts_for_each_cell = []
    for i_vert in range(0,len(vert_list)):

        print("Doing vert: " + str(i_vert) + " / " + str(len(vert_list)))

        # New entry
        faces_for_each_cell.append([])

        # Get all edges connected to this vert
        edges_connected_to_vert = get_edges_connected_to_vert(i_vert, edge_list)

        print("Edges connected to vert: " + str(edges_connected_to_vert))

        # Go through all edges; make faces
        for i_edge in edges_connected_to_vert:
            edge = edge_list[i_edge]

            print("   Making face from edge: " + str(i_edge))

            # Get the tets connected to this edge
            tets_connected_to_edge = get_tets_connected_to_edge(edge, tet_list)

            print("   Tets connected to this edge: " + str(tets_connected_to_edge))

            # These are the verts of thise face, but they are not ordered correctly!
            # Instead: get the order of the tets right first
            tets_connected_to_edge_ordered = order_tet_list_into_loop_by_neighbors(tets_connected_to_edge, tet_neighbors)

            print("   Verts of this face: " + str(tets_connected_to_edge_ordered))

            # Add faces
            faces_for_each_cell[-1].append(tets_connected_to_edge_ordered)

        # Convert to local idxs
        all_verts = []
        global_to_local_idx_dict = {}
        for face in faces_for_each_cell[-1]:
            for vert in face:
                if not vert in all_verts:
                    all_verts.append(vert)
                    global_to_local_idx_dict[vert] = len(all_verts) - 1

        # New entry
        verts_for_each_cell.append([circumcenters[i_vert] for i_vert in all_verts])

        # Convert face idxs to local idxs
        faces_for_each_cell[-1] = [[global_to_local_idx_dict[i_vert] for i_vert in face] for face in faces_for_each_cell[-1]]

    return [ verts_for_each_cell, faces_for_each_cell ]
