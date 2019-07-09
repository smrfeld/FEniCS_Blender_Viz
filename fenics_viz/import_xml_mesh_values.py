import re

def import_xml_mesh_values(fname):

    # Open
    f = open(fname, "r")

    eps = 1.0e-10
    vals = []

    for line in f:
        s = line.split()
        if len(s) > 0 and s[0] == "<dof":
            # Vertex; find quotes
            starts = [match.start() for match in re.finditer(re.escape("\""), line)]
            idx = int(line[starts[0]+1:starts[1]])
            value = float(line[starts[2]+1:starts[3]])
            cell = int(line[starts[4]+1:starts[5]])
            vert = int(line[starts[6]+1:starts[7]])

            # if abs(value) > eps:
            vals.append((cell,vert,value))

    # Close
    f.close()

    return vals
