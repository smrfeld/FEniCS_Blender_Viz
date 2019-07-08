import bpy, bmesh

# Make mesh object
def make_mesh_object_with_idxs(obj_name, vert_list, tet_list, edge_list=None):

    # Strip the idxs
    vert_list_wo_idxs = [v[1:] for v in vert_list]
    tet_list_wo_idxs = [f[1:] for f in tet_list]

    return make_mesh_object(obj_name, vert_list_wo_idxs, tet_list_wo_idxs, edge_list)

def make_mesh_object(obj_name, vert_list_wo_idxs, tet_list_wo_idxs, edge_list_wo_idxs=None):

    if edge_list_wo_idxs == None:
        edge_list_wo_idxs = []
        for f in tet_list_wo_idxs:
            edge_list_wo_idxs.append(sorted([f[0],f[1]]))
            edge_list_wo_idxs.append(sorted([f[0],f[2]]))
            edge_list_wo_idxs.append(sorted([f[0],f[3]]))
            edge_list_wo_idxs.append(sorted([f[1],f[2]]))
            edge_list_wo_idxs.append(sorted([f[1],f[3]]))
            edge_list_wo_idxs.append(sorted([f[2],f[3]]))

        # Delete duplicate edges
        tmp = set(tuple(x) for x in edge_list_wo_idxs)
        edge_list_wo_idxs = [ list(x) for x in tmp ]

    # Faces from tets
    face_list_wo_idxs = []
    for t in tet_list_wo_idxs:
        face_list_wo_idxs.append(sorted([t[0],t[1],t[2]]))
        face_list_wo_idxs.append(sorted([t[0],t[1],t[3]]))
        face_list_wo_idxs.append(sorted([t[0],t[2],t[3]]))
        face_list_wo_idxs.append(sorted([t[1],t[2],t[3]]))

    # Delete duplicate faces
    tmp = set(tuple(x) for x in face_list_wo_idxs)
    face_list_wo_idxs = [ list(x) for x in tmp ]

    # New object
    mesh_new = bpy.data.meshes.new(obj_name)

    # Build the object
    mesh_new.from_pydata(vert_list_wo_idxs,edge_list_wo_idxs,face_list_wo_idxs)

    # Update
    mesh_new.validate(verbose=False) # Important! and i dont know why
    mesh_new.update()

    # Object
    obj_new = bpy.data.objects.new(obj_name,mesh_new)

    # Something
    scene = bpy.context.scene
    scene.objects.link(obj_new)

    return obj_new
