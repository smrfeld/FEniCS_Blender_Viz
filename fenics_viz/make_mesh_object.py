import bpy, bmesh

def make_mesh_object(obj_name, vert_list_wo_idxs, edge_list_wo_idxs=[], face_list_wo_idxs=[]):

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
