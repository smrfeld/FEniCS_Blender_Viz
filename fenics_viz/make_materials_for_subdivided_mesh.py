import bpy

def make_materials_for_subdivided_mesh(context, obj, vert_face_strings):

    # Select the object
    obj.select = True
    context.scene.objects.active = obj

    # Clear all materials on the object
    bpy.ops.object.mode_set(mode='OBJECT')
    for i in range(0,context.object.material_slots.__len__()):
        context.object.active_material_index = 1
        bpy.ops.object.material_slot_remove()
    obj.data.materials.clear()

    # Assign a material to each region
    for i_vert in range(0,len(vert_face_strings)):
        s = vert_face_strings[i_vert].split()
        faces = [int(x) for x in s]

        # Deselect all vertices
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')

        # Must be in object mode to select the faces
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select these faces
        for f in faces:
            obj.data.polygons[f].select = True

        # Must be back in edit mode to assign faces to the material
        bpy.ops.object.mode_set(mode='EDIT')

        # Add a material slot
        bpy.ops.object.material_slot_add()

        # Assign a material to the last slot
        name = "vertex_%04i"%i_vert
        context.object.material_slots[bpy.context.object.material_slots.__len__() - 1].material = bpy.data.materials.new(name=name)

        # The name automatically gets something appended to it, because stupid things are stupid... change it back to the name we want
        context.object.material_slots[context.object.material_slots.__len__() - 1].material.name = name

        # Assign the material on the selected vertices
        bpy.ops.object.material_slot_assign()

    # Return in object mode
    bpy.ops.object.mode_set(mode='OBJECT')
