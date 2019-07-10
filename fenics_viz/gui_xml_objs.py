import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os

from . import import_xml_mesh
from . import make_mesh_object

class VertexObj(bpy.types.PropertyGroup):
    xval = FloatProperty( default= 0.0, precision=8, name="x" )
    yval = FloatProperty( default= 0.0, precision=8, name="y" )
    zval = FloatProperty( default= 0.0, precision=8, name="z" )
    idx = IntProperty( default = 0, name="idx" )
    # subDividedFaceIdxs = CollectionProperty(type=IntProperty, name="Subdivided face list")
    subDividedFaceIdxs = StringProperty ( name="Subdivided face list", default="", description="Subdivided face list" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.xval = arr[1]
        self.yval = arr[2]
        self.zval = arr[3]

    def get_list(self):
        return [self.xval,self.yval,self.zval]

    def get_list_with_idx(self):
        return [self.idx,self.xval,self.yval,self.zval]

class FaceObj(bpy.types.PropertyGroup):
    idx = IntProperty( default = 0, name="idx" )
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.v0 = arr[1]
        self.v1 = arr[2]
        self.v2 = arr[3]

    def get_list(self):
        return [self.v0,self.v1,self.v2]

    def get_list_with_idx(self):
        return [self.idx,self.v0,self.v1,self.v2]

class TetObj(bpy.types.PropertyGroup):
    idx = IntProperty( default = 0, name="idx" )
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )
    v3 = IntProperty( default = 0, name="v3" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.v0 = arr[1]
        self.v1 = arr[2]
        self.v2 = arr[3]
        self.v3 = arr[4]

    def get_list(self):
        return [self.v0,self.v1,self.v2,self.v3]

    def get_list_with_idx(self):
        return [self.idx,self.v0,self.v1,self.v2,self.v3]

# Class to hold the object
class MeshObject(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=VertexObj, name = "Vertex list")
    face_list = CollectionProperty(type=FaceObj, name = "face list")
    tet_list = CollectionProperty(type=TetObj, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

########################################
# List
########################################

# Model object item to draw in the list
class FViz_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

# Button to remove model object
class FVizObjectRemove(bpy.types.Operator):
    bl_idname = "fviz.mesh_object_remove"
    bl_label = "Remove a Mesh Object"
    bl_description = "Remove a mesh object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_mesh_object()
        return {'FINISHED'}

# Button to remove all model objects
class FVizObjectRemoveAll(bpy.types.Operator):
    bl_idname = "fviz.mesh_object_remove_all"
    bl_label = "Remove all Mesh Objects"
    bl_description = "Remove all mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_all_mesh_objects()
        return {'FINISHED'}

# Import mesh
class ImportMesh(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.import_mesh"
    bl_label = "Import mesh"

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
            context.scene.fviz.add_mesh_object(filename, vert_list, face_list, tet_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
