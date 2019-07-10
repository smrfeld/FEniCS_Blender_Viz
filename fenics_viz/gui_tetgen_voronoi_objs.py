import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

from . import gui_common_objs
from . import fname_helper
from . import import_tetgen
from . import make_mesh_object

# Class to hold the object
class Voronoi_Obj_Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=gui_common_objs.Vertex, name = "Vertex list")
    face_list = CollectionProperty(type=gui_common_objs.CellFace, name = "Face list")
    cell_list = CollectionProperty(type=gui_common_objs.Cell, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

########################################
# List
########################################

# Model object item to draw in the list
class Voronoi_Obj_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

# Button to remove model object
class Voronoi_Obj_Remove(bpy.types.Operator):
    bl_idname = "fviz.voronoi_obj_remove"
    bl_label = "Remove a Voronoi Object"
    bl_description = "Remove a Voronoi object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_voronoi_obj()
        return {'FINISHED'}

# Button to remove all model objects
class Voronoi_Obj_Remove_All(bpy.types.Operator):
    bl_idname = "fviz.voronoi_obj_remove_all"
    bl_label = "Remove all Voronoi Objects"
    bl_description = "Remove all Voronoi objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_all_voronoi_objs()
        return {'FINISHED'}

class Voronoi_Obj_Import(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.voronoi_obj_import"
    bl_label = "Import Voronoi from TetGen"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        # Get the active delaunay object
        f = context.scene.fviz
        if len(f.delaunay_obj_list) == 0:
            raise SystemError("Must have already imported and selected Delaunay mesh!")
        delaunay_obj = f.delaunay_obj_list[f.active_delaunay_obj_idx]

        # Get the selected filenames
        extensions_required = [".node", ".edge", ".face"]
        fname_nodes, fname_edges, fname_faces = fname_helper.get_fnames(extensions_required, self.files, self.directory)

        # Import
        vert_list, edge_list, face_list = import_tetgen.import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces)

        # Get voronoi cells - there is a bug in tetgen 1.5.1 that does not generate these correctly
        delaunay_vert_list = [v.get_list() for v in delaunay_obj.vert_list]
        delaunay_tet_list = [t.get_list() for t in delaunay_obj.tet_list]
        vert_list_wo_idxs = [v[1:] for v in vert_list]
        face_list_wo_idxs = [f[1:] for f in face_list]
        cell_list = fix_tetgen_voronoi.make_cell_list(vert_list_wo_idxs, face_list_wo_idxs, delaunay_vert_list, delaunay_tet_list)

        # Make object
        obj_name = fname_helper.get_base_name(fname_nodes)
        make_mesh_object.make_mesh_object(obj_name, vert_list, edge_list, face_list)

        # Add to the list
        context.scene.fviz.add_voronoi_obj(obj_name, vert_list, face_list, cell_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
