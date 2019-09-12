import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os
from . import objs
from . import import_xml_mesh_values

########################################
# Buttons
########################################

# Import mesh
class Obj_Import_Values(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.read_values"
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

            # Go through all vals
            mesh_obj = context.scene.fviz.obj_list[context.scene.fviz.active_obj_idx]
            for val in vals:
                tet_idx = val[0]
                vert_idx = val[1]
                value = val[2]

                # Get the tet object
                tet_obj = mesh_obj.tet_list[tet_idx]

                # Set the value
                if vert_idx == 0:
                    vert_global = tet_obj.v0
                elif vert_idx == 1:
                    vert_global = tet_obj.v1
                elif vert_idx == 2:
                    vert_global = tet_obj.v2
                elif vert_idx == 3:
                    vert_global = tet_obj.v3

                # Get the vert
                vert_obj = mesh_obj.vert_list[vert_global]

                # Set the value
                vert_obj.value = value

            # Recalculate all the bases
            mesh_obj.recalculate_basis()

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
