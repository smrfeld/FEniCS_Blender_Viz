import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

class Voronoi_Obj_DrawSwitch(bpy.types.Operator):
    bl_idname = "fviz.voronoi_obj_draw_switch"
    bl_label = "Switch wire and textured draw types"

    # Get the filename
    def execute(self, context):

        # Iterate over all objects
        f = context.scene.fviz
        for obj in f.voronoi_obj_list:

            # Get the blender obj
            obj_blender = bpy.data.objects[obj.name]

            # Set draw type
            if obj_blender.draw_type == 'TEXTURED':
                obj_blender.draw_type = 'WIRE'
            elif obj_blender.draw_type == 'WIRE':
                obj_blender.draw_type = 'TEXTURED'

        return {'FINISHED'}


class Voronoi_Obj_Triangulate_All(bpy.types.Operator):
    bl_idname = "fviz.voronoi_obj_triangulate_all"
    bl_label = "Triangulate all objects"

    # Get the filename
    def execute(self, context):

        # Iterate over all objects
        f = context.scene.fviz
        for obj in f.voronoi_obj_list:

            # Get the blender obj
            obj_blender = bpy.data.objects[obj.name]

            # Select object
            obj_blender.select = True
            context.scene.objects.active = obj_blender

            # Select all faces
            bpy.ops.object.mode_set(mode='EDIT')
            # Face selection mode
            bpy.context.tool_settings.mesh_select_mode = (False, False, True)
            bpy.ops.mesh.select_all(action='SELECT')

            # Triangulate
            bpy.ops.mesh.quads_convert_to_tris()

            # Back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect
            obj_blender.select = False

        return {'FINISHED'}
