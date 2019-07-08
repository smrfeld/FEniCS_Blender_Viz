import re

def import_xml_mesh(fname):

    # Open
    f = open(fname, "r")

    vert_list = []
    face_list = []

    for line in f:
        s = line.split()
        if len(s) > 0 and s[0] == "<vertex":
            # Vertex; find quotes
            starts = [match.start() for match in re.finditer(re.escape("\""), line)]
            idx = int(line[starts[0]+1:starts[1]])
            points = [float(line[starts[2*i]+1:starts[2*i+1]]) for i in range(1,4)]
            vert_list.append([idx] + points)

        if len(s) > 0 and s[0] == "<triangle":
            # Elements; find quotes
            starts = [match.start() for match in re.finditer(re.escape("\""), line)]
            idx = int(line[starts[0]+1:starts[1]])
            verts = [int(line[starts[2*i]+1:starts[2*i+1]]) for i in range(1,4)]
            face_list.append([idx] + verts)

    # Close
    f.close()

    return [vert_list, face_list]
