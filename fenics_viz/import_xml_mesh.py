import re

def edge_list_from_tet_list_with_idxs(tet_list):
    edge_list = []
    for t in tet_list:
        edge_list.append(sorted([t[1],t[2]]))
        edge_list.append(sorted([t[1],t[3]]))
        edge_list.append(sorted([t[1],t[4]]))
        edge_list.append(sorted([t[2],t[3]]))
        edge_list.append(sorted([t[2],t[4]]))
        edge_list.append(sorted([t[3],t[4]]))

    # Delete duplicate edges
    tmp = set(tuple(x) for x in edge_list)
    edge_list = [ list(x) for x in tmp ]

    # Add idxs
    for i in range(0, len(edge_list)):
        edge_list[i] = [i] + edge_list[i]

    return edge_list

def face_list_from_tet_list_with_idxs(tet_list):

    # Faces from tets
    face_list = []
    for t in tet_list:
        face_list.append(sorted([t[1],t[2],t[3]]))
        face_list.append(sorted([t[1],t[2],t[4]]))
        face_list.append(sorted([t[1],t[3],t[4]]))
        face_list.append(sorted([t[2],t[3],t[4]]))

    # Delete duplicate faces
    tmp = set(tuple(x) for x in face_list)
    face_list = [ list(x) for x in tmp ]

    # Add idxs
    for i in range(0, len(face_list)):
        face_list[i] = [i] + face_list[i]

    return face_list


def import_xml_mesh(fname):

    # Open
    f = open(fname, "r")

    vert_list = []
    tet_list = []

    for line in f:
        s = line.split()
        if len(s) > 0 and s[0] == "<vertex":
            # Vertex; find quotes
            starts = [match.start() for match in re.finditer(re.escape("\""), line)]
            idx = int(line[starts[0]+1:starts[1]])
            points = [float(line[starts[2*i]+1:starts[2*i+1]]) for i in range(1,4)]
            vert_list.append([idx] + points)

        if len(s) > 0 and s[0] == "<tetrahedron":
            # Elements; find quotes
            starts = [match.start() for match in re.finditer(re.escape("\""), line)]
            idx = int(line[starts[0]+1:starts[1]])
            verts = [int(line[starts[2*i]+1:starts[2*i+1]]) for i in range(1,5)]
            tet_list.append([idx] + verts)

    # Close
    f.close()

    # Sort the lists by the idx
    vert_list.sort(key=lambda x: x[0])
    tet_list.sort(key=lambda x: x[0])

    return [vert_list, edge_list_from_tet_list_with_idxs(tet_list), face_list_from_tet_list_with_idxs(tet_list), tet_list]
