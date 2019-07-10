import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper
import os

from . import make_subdivided_triangles
from . import import_xml_mesh_values
from . import make_materials_for_subdivided_mesh
from . import color_subdivided_mesh
from . import make_mesh_object

# Subdivide faces
class XML_Obj_SubdivideFaces(bpy.types.Operator):
    bl_idname = "fviz.xml_obj_subdivide_faces"
    bl_label = "Subdivide faces"

    def execute ( self, context ):

        # Get the selected object
        f = context.scene.fviz
        obj = f.xml_obj_list[f.active_xml_obj_idx]

        # Verts and faces
        vert_list = [v.get_list() for v in obj.vert_list]
        face_list = [f.get_list() for f in obj.face_list]

        # Make the subdivided faces
        vert_list_s, edge_list_s, face_list_s = make_subdivided_triangles.make_subdivided_triangles(vert_list, face_list)

        # Make the object
        new_obj = make_mesh_object.make_mesh_object("sub", vert_list_s, edge_list_s, face_list_s)

        # Store face idxs on the verts, so can change material color for animation!

        # Clear first
        for v_idx in range(0,len(obj.vert_list)):
            obj.vertex_subdivided_face_list[v_idx].faces = ""

        # Write in space deliminited format, for some stupid reason
        # Related to collection of collections not working
        idx_max = len(vert_list)
        for i_face in range(0,len(face_list_s)):
            for v_idx in face_list_s[i_face]:
                if v_idx < idx_max: # Other vertices are new ones; we only care about the existing
                    if obj.vertex_subdivided_face_list[v_idx].faces == "":
                        obj.vertex_subdivided_face_list[v_idx].faces = str(i_face)
                    else:
                        obj.vertex_subdivided_face_list[v_idx].faces += " " + str(i_face)
                    # No more will come for this face
                    break

        # Add materials
        vert_face_strings = [s.faces for s in obj.vertex_subdivided_face_list]
        make_materials_for_subdivided_mesh.make_materials_for_subdivided_mesh(context, new_obj, vert_face_strings)

        return {"FINISHED"}

class XML_Obj_VisualizeTimepoint(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.xml_obj_visualize_timepoint"
    bl_label = "Visualize a timpoint"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    filename_ext = ".xml" # allowed extensions

    # Get the filename
    def execute(self, context):

        # store
        if self.filepath[-4:] != self.filename_ext:
            raise SystemError("Must be: " + str(self.filename_ext) + " format but you chose: " + str(self.filepath[-4:]) + "!")
        else:

            # Filename
            filename = os.path.basename(self.filepath)[:-4]

            # Import
            vals = import_xml_mesh_values.import_xml_mesh_values(self.filepath)

            # Current object
            f = context.scene.fviz
            obj = f.xml_obj_list[f.active_xml_obj_idx]

            # Convert vals to verts
            vert_vals = []
            for val in vals:
                tet = obj.tet_list[val[0]]
                if val[1] == 0:
                    vert_vals.append([tet.v0,val[2]])
                elif val[1] == 1:
                    vert_vals.append([tet.v1,val[2]])
                elif val[1] == 2:
                    vert_vals.append([tet.v2,val[2]])
                else:
                    vert_vals.append([tet.v3,val[2]])

            # Sort by vertex
            vert_vals.sort(key=lambda x: x[0])

            vert_vals = [x[1] for x in vert_vals]

            min_val = 0.0 #min(vert_vals)
            max_val = 0.1 #max(vert_vals)

            # Update the colors on the materials
            obj = bpy.data.objects["sub"]
            color_subdivided_mesh.color_subdivided_mesh(context, obj, vert_vals, min_val, max_val)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
