import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os

from . import make_mesh_object
from . import import_tetgen
from . import voronoi_from_delaunay

def get_fnames(extensions_required, files, directory):

    fnames = len(extensions_required) * [None]

    if len(files) != len(extensions_required):
        raise SystemError("Must select " + str(len(extensions_required)) + " files: " + str(extensions_required))

    for filename in files:
        full_name = os.path.join(directory, filename.name)
        _, extension = os.path.splitext(full_name)
        if not extension in extensions_required:
            raise SystemError("Allowed extensions are: " + str(extensions_required) + " but chosen is: " + str(extension))

        idx = extensions_required.index(extension)
        fnames[idx] = full_name

    # Check all extensions are present
    for fname in fnames:
        if fname == None:
            raise SystemError("Missing files! Required are: " + str(extensions_required) + " but got: " + str(fnames))

    return fnames


class ImportTetGenDelaunay(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.import_tetgen_delaunay"
    bl_label = "Import Delaunay from TetGen"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        extensions_required = [".node", ".edge", ".face", ".ele"]
        fname_nodes, fname_edges, fname_faces, fname_elements = get_fnames(extensions_required, self.files, self.directory)

        # Import
        point_list, edge_list, face_list, tet_list = import_tetgen.import_tetgen_delaunay(fname_nodes, fname_edges, fname_faces, fname_elements)

        # Make object
        make_mesh_object.make_mesh_object_with_idxs("delaunay", point_list, edge_list, face_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class CreateVoronoiFromDelaunay(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.create_voronoi"
    bl_label = "Create Voronoi from TetGen Delaunay"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        extensions_required = [".node", ".edge", ".face", ".ele", ".neigh"]
        fname_nodes, fname_edges, fname_faces, fname_elements, fname_neighs = get_fnames(extensions_required, self.files, self.directory)

        # Import
        point_list, edge_list, face_list, tet_list = import_tetgen.import_tetgen_delaunay(fname_nodes, fname_edges, fname_faces, fname_elements)
        neigh_list = import_tetgen.import_tetgen_delaunay_neighbors(fname_neighs)

        # Create voronoi
        nodes_for_each_cell, edges_for_each_cell = voronoi_from_delaunay.voroni_from_delaunay(point_list, tet_list, neigh_list)
        print(nodes_for_each_cell)
        print(edges_for_each_cell)

        # Make object
        for i in range(0,len(nodes_for_each_cell)):
            name = "voronoi_%04i" % i
            make_mesh_object.make_mesh_object(name, nodes_for_each_cell[i], edges_for_each_cell[i])

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



class ImportTetGenVoronoi(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.import_tetgen_voronoi"
    bl_label = "Import Voronoi from TetGen"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        extensions_required = [".node", ".edge", ".face", ".cell"]
        fname_nodes, fname_edges, fname_faces, fname_cells = get_fnames(extensions_required, self.files, self.directory)

        # Import
        point_list, edge_list, face_list, cell_list = import_tetgen.import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces, fname_cells)

        # Make object
        make_mesh_object.make_mesh_object_with_idxs("voronoi", point_list, edge_list, face_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ImportTetGenVoronoiSeparate(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.import_tetgen_voronoi_separate"
    bl_label = "Import Voronoi from TetGen into separate objects"

    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory = StringProperty(subtype='DIR_PATH')

    # Get the filename
    def execute(self, context):

        extensions_required = [".node", ".edge", ".face", ".cell"]
        fname_nodes, fname_edges, fname_faces, fname_cells = get_fnames(extensions_required, self.files, self.directory)

        # Import
        point_list, edge_list, face_list, cell_list = import_tetgen.import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces, fname_cells)

        # Make separate objects for each cell
        for i_cell in range(0,1):
            cell = cell_list[i_cell]
            name = "voronoi_%04i" % i_cell

            points = []
            edges = []
            faces = []

            # Dict from idxs in point_list to idx in points
            point_idx_dict = {}

            # Go through the faces
            for face_idx in cell[1:]:
                face_points = face_list[face_idx][1:]

                # Add all the points
                for point in face_points:
                    if not point in point_idx_dict:
                        point_idx_dict[point] = len(points)
                        points.append(point_list[point][1:])

                # Add all the edges
                for i_point in range(0,len(face_points)-1):
                    v1 = point_idx_dict[face_points[i_point]]
                    v2 = point_idx_dict[face_points[i_point+1]]
                    edges.append(sorted([v1,v2]))

                # Add the face
                faces.append([point_idx_dict[point] for point in face_points])

            # Make the object
            make_mesh_object.make_mesh_object(name, points, edges, faces)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
