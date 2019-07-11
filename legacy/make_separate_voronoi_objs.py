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
