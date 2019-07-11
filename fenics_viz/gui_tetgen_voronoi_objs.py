import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

from . import gui_common_objs
from . import fname_helper
from . import import_tetgen
from . import make_mesh_object
from . import voronoi_from_delaunay

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

        # Get current object
        f = context.scene.fviz
        if len(f.delaunay_obj_list) == 0:
            raise SystemError("Must have already imported and selected Delaunay mesh!")
        obj = f.delaunay_obj_list[f.active_delaunay_obj_idx]

        # Import neighbors
        extensions_required = [".neigh"]
        fname_neighs = fname_helper.get_fnames(extensions_required, self.files, self.directory)[0]
        neigh_list = import_tetgen.import_tetgen_delaunay_neighbors(fname_neighs)

        # Create voronoi
        delaunay_vert_list = [v.get_list() for v in obj.vert_list]
        delaunay_edge_list = [e.get_list() for e in obj.edge_list]
        delaunay_tet_list = [t.get_list() for t in obj.tet_list]

        verts_for_each_cell, faces_for_each_cell = voronoi_from_delaunay.voronoi_from_delaunay(delaunay_vert_list, delaunay_edge_list, delaunay_tet_list, neigh_list)

        # Make objects
        for i in range(0,len(verts_for_each_cell)):
            obj_name = "voronoi_%04i" % i
            make_mesh_object.make_mesh_object(obj_name, vert_list=verts_for_each_cell[i], edge_list=[], face_list=faces_for_each_cell[i])

            # Add to the list
            cell_list = [list(range(0,len(faces_for_each_cell[i])))]
            context.scene.fviz.add_voronoi_obj(obj_name, verts_for_each_cell[i], faces_for_each_cell[i], cell_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
