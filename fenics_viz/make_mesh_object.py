import bpy, bmesh

def make_mesh_object(obj_name, vert_list, edge_list=[], face_list=[]):

    # New object
    mesh_new = bpy.data.meshes.new(obj_name)

    # Build the object
    mesh_new.from_pydata(vert_list,edge_list,face_list)

    # Update
    mesh_new.validate(verbose=False) # Important! and i dont know why
    mesh_new.update()

    # Object
    obj_new = bpy.data.objects.new(obj_name,mesh_new)

    # Something
    scene = bpy.context.scene
    scene.objects.link(obj_new)

    return obj_new
