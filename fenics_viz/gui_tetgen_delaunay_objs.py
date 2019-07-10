import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

from . import gui_general_tet_objs
from . import fname_helper
from . import import_tetgen
from . import make_mesh_object

# Class to hold the object
class Delaunay_Obj_Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=gui_general_tet_objs.TetVertex, name = "Vertex list")
    face_list = CollectionProperty(type=gui_general_tet_objs.TetFace, name = "Face list")
    tet_list = CollectionProperty(type=gui_general_tet_objs.Tet, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

########################################
# List
########################################

# Model object item to draw in the list
class Delaunay_Obj_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

# Button to remove model object
class Delaunay_Obj_Remove(bpy.types.Operator):
    bl_idname = "fviz.delaunay_obj_remove"
    bl_label = "Remove a Delaunay Object"
    bl_description = "Remove a Delaunay object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_delaunay_obj()
        return {'FINISHED'}

# Button to remove all model objects
class Delaunay_Obj_Remove_All(bpy.types.Operator):
    bl_idname = "fviz.delaunay_obj_remove_all"
    bl_label = "Remove all Delaunay Objects"
    bl_description = "Remove all Delaunay objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_all_delaunay_objs()
        return {'FINISHED'}

class Delaunay_Obj_Import(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.delaunay_obj_import"
    bl_label = "Import Delaunay from TetGen"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        extensions_required = [".node", ".edge", ".face", ".ele"]
        fname_nodes, fname_edges, fname_faces, fname_elements = fname_helper.get_fnames(extensions_required, self.files, self.directory)

        # Import
        point_list, edge_list, face_list, tet_list = import_tetgen.import_tetgen_delaunay(fname_nodes, fname_edges, fname_faces, fname_elements)

        # Make object
        obj_name = fname_helper.get_base_name(fname_nodes)
        make_mesh_object.make_mesh_object_with_idxs(obj_name, point_list, edge_list, face_list)

        # Add to the list
        context.scene.fviz.add_delaunay_obj(obj_name, point_list, face_list, tet_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
