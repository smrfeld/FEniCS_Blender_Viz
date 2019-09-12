import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os
from . import make_mesh_object
from . import objs
from . import import_xml_mesh

########################################
# List
########################################

# Model object item to draw in the list
class Obj_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

########################################
# Buttons
########################################

# Button to remove model object
class Obj_Remove(bpy.types.Operator):
    bl_idname = "fviz.obj_remove"
    bl_label = "Remove a Mesh Object"
    bl_description = "Remove a mesh object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_obj()
        return {'FINISHED'}

# Button to remove all model objects
class Obj_Remove_All(bpy.types.Operator):
    bl_idname = "fviz.obj_remove_all"
    bl_label = "Remove all Mesh Objects"
    bl_description = "Remove all mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_all_objs()
        return {'FINISHED'}

# Import mesh
class Obj_Import(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.obj_import"
    bl_label = "Import XML Object"

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
            vert_list, tet_list = import_xml_mesh.import_xml_mesh(self.properties.filepath)

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
