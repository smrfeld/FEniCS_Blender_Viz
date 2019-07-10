import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os

from . import import_xml_mesh
from . import make_mesh_object
from . import gui_general_tet_objs

class XML_Obj_Vertex_Subdivded_Faces(bpy.types.PropertyGroup):
    faces = StringProperty ( name="Faces", default="", description="Subdivided faces for this vertex" )
    idx = IntProperty( default = 0, name="idx" )

# Class to hold the object
class XML_Obj_Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=gui_general_tet_objs.TetVertex, name = "Vertex list")
    face_list = CollectionProperty(type=gui_general_tet_objs.TetFace, name = "Face list")
    tet_list = CollectionProperty(type=gui_general_tet_objs.Tet, name = "Tet list")
    vertex_subdivided_face_list = CollectionProperty(type=XML_Obj_Vertex_Subdivded_Faces, name = "Subdivided face list for each vertex")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

########################################
# List
########################################

# Model object item to draw in the list
class XML_Obj_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

# Button to remove model object
class XML_Obj_Remove(bpy.types.Operator):
    bl_idname = "fviz.xml_obj_remove"
    bl_label = "Remove a Mesh Object"
    bl_description = "Remove a mesh object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_xml_obj()
        return {'FINISHED'}

# Button to remove all model objects
class XML_Obj_Remove_All(bpy.types.Operator):
    bl_idname = "fviz.xml_obj_remove_all"
    bl_label = "Remove all Mesh Objects"
    bl_description = "Remove all mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_all_xml_objs()
        return {'FINISHED'}

# Import mesh
class XML_Obj_Import(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.xml_obj_import"
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
            vert_list, edge_list, face_list, tet_list = import_xml_mesh.import_xml_mesh(self.properties.filepath)

            # Make the objects
            make_mesh_object.make_mesh_object_with_idxs(filename, vert_list, edge_list, face_list)

            # Add to the list
            context.scene.fviz.add_xml_obj(filename, vert_list, face_list, tet_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
