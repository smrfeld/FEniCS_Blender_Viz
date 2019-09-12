import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os
from . import make_mesh_object
from . import objs
from . import import_xml_mesh_values

########################################
# Buttons
########################################

# Import mesh
class Obj_Import_Values(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.obj_import_values"
    bl_label = "Import XML Object Values"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")
    filename_ext = ".xml" # allowed extensions

    # Get the filename
    def execute(self, context):

        # store
        if self.properties.filepath[-4:] != self.filename_ext:
            raise SystemError("Must be: " + str(self.filename_ext) + " format but you chose: " + str(self.properties.filepath[-4:]) + "!")
        else:

            # Filename
            filename = os.path.basename(self.properties.filepath)[:-4]

            # Import
            vals = import_xml_mesh_values.import_xml_mesh_values(self.properties.filepath)

            

            # Run through all tets
            for tet_idx, tet in enumerate(tet_list):

                name = filename + "_%05d" % tet_idx

                # Get the verts
                verts = [ vert_list[tet[i]] for i in range(0,4) ]

                # Get the edges
                edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]

                # Get the faces
                faces = [[0,1,2],[0,1,3],[0,2,3],[1,2,3]]

                # Make the object in blender
                make_mesh_object.make_mesh_object(name, verts, edges, faces)

            # Add to the list
            context.scene.fviz.add_obj(filename, vert_list, tet_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
