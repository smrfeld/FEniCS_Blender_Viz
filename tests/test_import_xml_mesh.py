import sys
sys.path.append("../fenics_viz")
from import_xml_mesh import *

if __name__ == "__main__":

    vert_list, face_list = import_xml_mesh("test.xml")

    print(vert_list)

    print(face_list)
