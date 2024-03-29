import re

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

        if len(s) > 0 and (s[0] == "<tetrahedron" or s[0] == "<triangle"):
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

    # Strip the idx
    vert_list = [x[1:] for x in vert_list]
    tet_list = [x[1:] for x in tet_list]

    return [vert_list, tet_list]
