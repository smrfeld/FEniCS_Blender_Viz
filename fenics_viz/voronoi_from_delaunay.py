
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

def check_if_vert_on_boundary(i_vert, vert_list, tet_list):

    on_boundary = False
    bdry_faces = []

    # Get all tets attached to this vert
    for i_tet in range(0,len(tet_list)):
        tet = tet_list[i_tet]

        if i_vert in tet:
            # This tet is attached

            # Go through all faces, check if they exist
            for i in range(0,4):
                for j in range(i+1,4):
                    for k in range(j+1,4):
                        vert_idxs = [tet[i],tet[j],tet[k]]
                        if i_vert in vert_idxs:
                            if not check_if_face_exists(vert_idxs,tet_list,i_tet):
                                on_boundary = True
                                vert_pts = [vert_list[v] for v in vert_idxs]
                                bdry_faces.append(BoundaryFace(i_tet, vert_idxs, vert_pts))

    return [on_boundary, bdry_faces]

def check_if_face_exists(verts, tet_list, not_this_idx):

    # Check against all other tets
    for i_tet_other in range(0,len(tet_list)):
        if i_tet_other != not_this_idx:
            # Do the faces match?
            tet_other = tet_list[i_tet_other]
            if verts[0] in tet_other and verts[1] in tet_other and verts[2] in tet_other:
                print("Face is not on the boundary: " + str(tet_other))
                return True

    return False

class BoundaryFace:

    def __init__(self, tet_idx, idxs, pts):
        self.tet_idx = tet_idx
        self.idxs = idxs
        self.pts = pts

        self.center = [0.333*(self.pts[0][i_coord] + self.pts[1][i_coord] + self.pts[2][i_coord]) for i_coord in range(0,3)]

        # Like a linked list!
        self.edge_crossing_next = None
        self.edge_crossing_prev = None
        self.idx_in_loop = None

    def check_borders(self, other_face):
        if self.idxs[0] in other_face.idxs and self.idxs[1] in other_face.idxs:
            return [True, [0,1]]
        elif self.idxs[0] in other_face.idxs and self.idxs[2] in other_face.idxs:
            return [True, [0,2]]
        elif self.idxs[1] in other_face.idxs and self.idxs[2] in other_face.idxs:
            return [True, [1,2]]
        return [False, None]

class EdgeCrossing:

    def __init__(self, face_prev, face_next):
        self.face_prev = face_prev
        self.face_next = face_next

        _, vert_idxs = self.face_prev.check_borders(self.face_next)

        self.edge_pt = [0.5*(self.face_prev.pts[vert_idxs[0]][i_coord] + self.face_prev.pts[vert_idxs[1]][i_coord]) for i_coord in range(0,3)]

        self.vert_idx_of_this_edge = None

class FaceLoop:

    def __init__(self, faces):

        self.starting_face = faces[0]
        self.starting_face.idx_in_loop = 0
        faces_done = [0]

        # Rest
        current_face = self.starting_face
        while len(faces_done) != len(faces):

            # Find neighboring face
            for i_face in range(0,len(faces)):
                if i_face in faces_done:
                    continue # skip

                next_face = faces[i_face]

                # Check borders
                borders, _ = current_face.check_borders(next_face)
                if borders:
                    next_face.idx_in_loop = current_face.idx_in_loop + 1
                    faces_done.append(i_face)

                    # Edge crossing object
                    edge_crossing = EdgeCrossing(current_face, next_face)
                    current_face.edge_crossing_next = edge_crossing
                    next_face.edge_crossing_prev = edge_crossing

                    # current = next
                    current_face = next_face

                    # Next
                    break

        # Final edge crossing looping around
        edge_crossing = EdgeCrossing(current_face, self.starting_face)
        current_face.edge_crossing_next = edge_crossing
        self.starting_face.edge_crossing_prev = edge_crossing



def voronoi_from_delaunay(vert_list, edge_list, tet_list, tet_neighbors):

    # Go through all tets, get circumcenters
    circumcenters = []
    for tet in tet_list:
        pts = [vert_list[v] for v in tet]
        circumcenters.append(circumcenter_sphere.circumcenter_sphere_from_pt_list(pts))

    faces_for_each_cell = []
    verts_for_each_cell = []
    edges_for_each_cell = []

    # Go through all verts; each gets a cell
    for i_vert in range(0,len(vert_list)):

        # print("Doing vert: " + str(i_vert) + " / " + str(len(vert_list)))

        # New entry
        faces_for_each_cell.append([])

        # Get all edges connected to this vert
        edges_connected_to_vert = get_edges_connected_to_vert(i_vert, edge_list)

        # print("Edges connected to vert: " + str(edges_connected_to_vert))

        # Go through all edges; make faces
        for i_edge in edges_connected_to_vert:
            edge = edge_list[i_edge]

            # print("   Making face from edge: " + str(i_edge))

            # Get the tets connected to this edge
            tets_connected_to_edge = get_tets_connected_to_edge(edge, tet_list)

            # print("   Tets connected to this edge: " + str(tets_connected_to_edge))

            # These are the verts of thise face, but they are not ordered correctly!
            # Instead: get the order of the tets right first
            tets_connected_to_edge_ordered = order_tet_list_into_loop_by_neighbors(tets_connected_to_edge, tet_neighbors)

            # print("   Verts of this face: " + str(tets_connected_to_edge_ordered))

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

        print(global_to_local_idx_dict)

        # Verts on the boundary have a problem; they need more points
        on_boundary, bdry_faces = check_if_vert_on_boundary(i_vert, vert_list, tet_list)

        if on_boundary:

            # This is a vert on the boundary!
            print(str(i_vert) + " is on the boundary!")

            # Make a point for the vert
            verts_for_each_cell[-1].append(vert_list[i_vert])
            i_vert_local_idx = len(verts_for_each_cell[-1]) - 1

            # Make a loop of the faces
            face_loop = FaceLoop(bdry_faces)

            # Go through all faces in the loop using the linked list
            # Get the first face
            bdry_face = face_loop.starting_face
            # Loop
            while True:

                # Make two triangular faces: the centroid of the tet, the center of the boundary triangle face, and the edge point (two different)
                vert_idx_centroid = global_to_local_idx_dict[bdry_face.tet_idx]

                # Add center point
                verts_for_each_cell[-1].append(bdry_face.center)
                vert_idx_center = len(verts_for_each_cell[-1]) - 1

                # Add edge pts if needed
                if bdry_face.edge_crossing_next.vert_idx_of_this_edge == None:
                    verts_for_each_cell[-1].append(bdry_face.edge_crossing_next.edge_pt)
                    bdry_face.edge_crossing_next.vert_idx_of_this_edge = len(verts_for_each_cell[-1]) - 1
                if bdry_face.edge_crossing_prev.vert_idx_of_this_edge == None:
                    verts_for_each_cell[-1].append(bdry_face.edge_crossing_prev.edge_pt)
                    bdry_face.edge_crossing_prev.vert_idx_of_this_edge = len(verts_for_each_cell[-1]) - 1

                # Add two faces
                faces_for_each_cell[-1].append([vert_idx_centroid, vert_idx_center, bdry_face.edge_crossing_prev.vert_idx_of_this_edge])
                faces_for_each_cell[-1].append([vert_idx_centroid, vert_idx_center, bdry_face.edge_crossing_next.vert_idx_of_this_edge])

                # Make another face from the two centroids and the edge point
                vert_idx_centroid_next = global_to_local_idx_dict[bdry_face.edge_crossing_next.face_next.tet_idx]

                # Make face
                faces_for_each_cell[-1].append([vert_idx_centroid, vert_idx_centroid_next, bdry_face.edge_crossing_next.vert_idx_of_this_edge])

                # Make the covering two faces from the vertex to the center of the triangle to the edges
                faces_for_each_cell[-1].append([i_vert_local_idx, vert_idx_center, bdry_face.edge_crossing_prev.vert_idx_of_this_edge])
                faces_for_each_cell[-1].append([i_vert_local_idx, vert_idx_center, bdry_face.edge_crossing_next.vert_idx_of_this_edge])

                # Get the next face
                bdry_face = bdry_face.edge_crossing_next.face_next

                # Check if we are back at the beginning; if so, stop
                if bdry_face.idx_in_loop == 0:
                    # Back to the beginning; stop
                    break

        # Remove any faces that only have 2 verts (why does this happen?)
        faces_for_each_cell[-1] = [face for face in faces_for_each_cell[-1] if len(face) >= 3]

        # Make edge list
        edges_for_each_cell.append([])

        # Go through all faces
        for face in faces_for_each_cell[-1]:
            e01 = sorted([face[0], face[1]])
            e02 = sorted([face[0], face[2]])
            e12 = sorted([face[1], face[2]])
            if not e01 in edges_for_each_cell[-1]:
                edges_for_each_cell[-1].append(e01)
            if not e02 in edges_for_each_cell[-1]:
                edges_for_each_cell[-1].append(e02)
            if not e12 in edges_for_each_cell[-1]:
                edges_for_each_cell[-1].append(e12)

    return [ verts_for_each_cell, edges_for_each_cell, faces_for_each_cell ]
