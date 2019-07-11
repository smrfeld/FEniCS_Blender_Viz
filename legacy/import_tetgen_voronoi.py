# TetGen 1.5.1 has a bug where the tet list is incorrect
# Other versions also have other bugs for the Voronoi diagrams
# It is easier therefore to regenerate the Voronoi mesh as the dual of the Delaunay

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
        no_points_interior, vert_list, edge_list, face_list = import_tetgen.import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces)

        # Get voronoi cells - there is a bug in tetgen 1.5.1 that does not generate these correctly
        delaunay_vert_list = [v.get_list() for v in delaunay_obj.vert_list]
        delaunay_edge_list = [e.get_list() for e in delaunay_obj.edge_list]
        delaunay_tet_list = [t.get_list() for t in delaunay_obj.tet_list]
        cell_list = fix_tetgen_voronoi.make_cell_list(no_points_interior, vert_list, face_list, delaunay_vert_list, delaunay_edge_list, delaunay_tet_list)

        # Make object
        obj_name = fname_helper.get_base_name(fname_nodes)
        make_mesh_object.make_mesh_object(obj_name, vert_list, edge_list, face_list)

        # Add to the list
        context.scene.fviz.add_voronoi_obj(obj_name, vert_list, face_list, cell_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def import_tetgen_voronoi(fname_nodes, fname_edges, fname_faces):

    # Import points (nodes)
    point_list = import_simple(fname_nodes, 3, floats=True)
    no_points_interior = len(point_list)

    edge_list = []
    face_list = []

    # Import edges
    f = open(fname_edges,"r")

    dist = 1.0

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr == 0:
            # Get how many elements there are
            no_edges = int(s[0])

        elif len(s) == 3 and s[0] != "#":
            edge_list.append([int(s[0]),int(s[1]),int(s[2])])

        elif len(s) > 0 and s[0] != "#":
            # This edge extends to infinity; make a new point some distance away
            idx = int(s[0])
            vert0_idx = int(s[1])
            vert0_pt = point_list[vert0_idx]
            ray = [float(s[3]), float(s[4]), float(s[5])] # s[2] = -1 to indicate boundary
            vert1_pt = [vert0_pt[i] - dist*ray[i] for i in range(0,3)]
            # Add the vert
            vert1_idx = len(point_list)
            point_list.append(vert1_pt)
            edge_list.append([idx, vert0_idx, vert1_idx])

        line_ctr += 1

    # Close
    f.close()

    # Import faces
    f = open(fname_faces,"r")

    line_ctr = 0
    for line in f:
        s = line.split()

        if line_ctr == 0:
            # Get how many elements there are
            no_faces = int(s[0])

        elif len(s) > 0 and s[0] != "#":
            # Remove boundary marker
            if s[-1] == "-1":
                s = s[:-1]

            # 0 = idx
            idx = int(s[0])

            # 1,2 = boundary cells
            # ignore

            # 3 = # edges
            # ignore

            # 4 to end = edges
            edge_idxs = [int(x) for x in s[4:]]
            edge_verts = [edge_list[edge_idx][1:] for edge_idx in edge_idxs]

            # Now get the verts... difficult!

            # Check the orientation of the first two manually - if this is corrected, the rest can be oriented automatically!
            verts = []
            prev_vert = edge_verts[0][1]
            if not prev_vert in edge_verts[1]:
                # Need to flip the first edge verts!
                edge_verts[0].reverse()

            # Add
            verts.append(edge_verts[0][0])
            verts.append(edge_verts[0][1])
            prev_vert = edge_verts[0][1]

            # Orient all the other edges
            for vert_pair in edge_verts[1:]:
                if vert_pair[1] == prev_vert:
                    # Flip
                    vert_pair.reverse()
                # otherwise already correct!

                prev_vert = vert_pair[1]
                verts.append(prev_vert)

            # Do not close
            if verts[0] == verts[-1]:
                verts = verts[:-1]

            face_list.append([idx] + verts)

        line_ctr += 1

    # Close
    f.close()

    # Sort lists
    edge_list.sort(key=lambda x: x[0])
    face_list.sort(key=lambda x: x[0])

    # Strip idxs
    edge_list = [x[1:] for x in edge_list]
    face_list = [x[1:] for x in face_list]

    return [ no_points_interior, point_list, edge_list, face_list ]
