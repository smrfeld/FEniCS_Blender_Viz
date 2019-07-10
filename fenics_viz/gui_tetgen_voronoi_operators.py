import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

from . import make_mesh_object
from . import import_tetgen
from . import fname_helper
from . import voronoi_from_delaunay

class Voronoi_Obj_Separate(bpy.types.Operator):
    bl_idname = "fviz.voronoi_obj_separate"
    bl_label = "Make separate Voronoi objects"

    # Get the filename
    def execute(self, context):

        # Get the selected object
        f = context.scene.fviz
        obj = f.voronoi_obj_list[f.active_voronoi_obj_idx]

        # Make separate objects for each cell
        for i_cell in range(0,len(obj.cell_list)):
            name = "voronoi_%04i" % i_cell

            cell = obj.cell_list[i_cell]
            face_idxs = [f.idx for f in cell.faces]

            vert_idxs = []
            global_to_local_idx_dict = {}
            for f in face_idxs:
                for v in obj.face_list[f].verts:
                    if not v.idx in vert_idxs:
                        vert_idxs.append(v.idx)
                        global_to_local_idx_dict[v.idx] = len(vert_idxs) - 1

            verts = [obj.vert_list[v].get_list() for v in vert_idxs]
            faces = [[global_to_local_idx_dict[v.idx] for v in obj.face_list[f].verts] for f in face_idxs]

            # Make the object
            make_mesh_object.make_mesh_object(name, verts, edge_list=[], face_list=faces)

        return {'FINISHED'}


class Voronoi_Obj_Create_from_Delaunay(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.voronoi_obj_create_from_delaunay"
    bl_label = "Create Voronoi from TetGen Delaunay"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        # Get current object
        f = context.scene.fviz
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

        # Make object
        for i in range(0,len(verts_for_each_cell)):
            name = "voronoi_%04i" % i
            make_mesh_object.make_mesh_object(name, vert_list=verts_for_each_cell[i], edge_list=[], face_list=faces_for_each_cell[i])

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
