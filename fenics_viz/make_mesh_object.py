import bpy, bmesh

# Make mesh object
def make_mesh_object_with_idxs(obj_name, vert_list, face_list, edge_list=None):

    # Strip the idxs
    vert_list_wo_idxs = [v[1:] for v in vert_list]
    face_list_wo_idxs = [f[1:] for f in face_list]

    return make_mesh_object(obj_name, vert_list_wo_idxs, face_list_wo_idxs, edge_list)

def make_mesh_object(obj_name, vert_list_wo_idxs, face_list_wo_idxs, edge_list_wo_idxs=None):

    if edge_list_wo_idxs == None:
        edge_list_wo_idxs = []
        for f in face_list_wo_idxs:
            edge_list_wo_idxs.append([f[0],f[1]])
            edge_list_wo_idxs.append([f[1],f[2]])
            edge_list_wo_idxs.append([f[0],f[2]])

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
