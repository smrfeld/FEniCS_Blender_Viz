import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import os
from . import objs

########################################
# Buttons
########################################

class Obj_Setup_Materials(bpy.types.Operator):
    bl_idname = "fviz.setup_materials"
    bl_label = "Setup materials for the objects"

    # Get the filename
    def execute(self, context):

        # Switch to cycle render
        # THIS IS VERY VERY VERY IMPORTANT!
        # else nothing works
        bpy.data.scenes["Scene"].render.engine = "CYCLES"

        # Run through the tets
        mesh_obj = context.scene.fviz.obj_list[context.scene.fviz.active_obj_idx]
        for tet in mesh_obj.tet_list:

            print("Making materials for tet %d / %d" % (tet.idx, len(mesh_obj.tet_list)))

            # Get the object in blender
            obj = bpy.data.objects[tet.name]

            # Select the object
            obj.select = True
            context.scene.objects.active = obj

            # Clear all materials on the object
            bpy.ops.object.mode_set(mode='OBJECT')
            for i in range(0,context.object.material_slots.__len__()):
                context.object.active_material_index = 1
                bpy.ops.object.material_slot_remove()
            obj.data.materials.clear()

            # Make material
            mat_name = "mat_%05d" % tet.idx
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True

            # Remove default
            mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))

            # Add new script node
            # https://docs.blender.org/api/2.79b/bpy.types.Node.html#bpy.types.Node
            # Later, find this again using:
            # mat.node_tree.nodes['Script']
            script_node = mat.node_tree.nodes.new(type='ShaderNodeScript')
            script_node.mode = "EXTERNAL"
            script_node.filepath = "/Users/oernst/Desktop/shader.osl"

            # Hook up the script node to the volume
            inp = mat.node_tree.nodes['Material Output'].inputs['Volume']
            outp = script_node.outputs['BSDF']
            mat.node_tree.links.new(inp,outp)

            # Assign the material to the object
            obj.active_material = mat

            # Deselect the object
            obj.select = False

        return {'FINISHED'}


class Obj_Setup_Materials_Surf(bpy.types.Operator):
    bl_idname = "fviz.setup_materials_surf"
    bl_label = "Setup materials with transparent surfaces"

    # Get the filename
    def execute(self, context):

        # Switch to cycle render
        # THIS IS VERY VERY VERY IMPORTANT!
        # else nothing works
        bpy.data.scenes["Scene"].render.engine = "CYCLES"

        # Run through the tets
        mesh_obj = context.scene.fviz.obj_list[context.scene.fviz.active_obj_idx]
        for tet in mesh_obj.tet_list:

            print("Making materials for tet %d / %d" % (tet.idx, len(mesh_obj.tet_list)))

            # Get the object in blender
            obj = bpy.data.objects[tet.name]

            # Select the object
            obj.select = True
            context.scene.objects.active = obj

            # Clear all materials on the object
            bpy.ops.object.mode_set(mode='OBJECT')
            for i in range(0,context.object.material_slots.__len__()):
                context.object.active_material_index = 1
                bpy.ops.object.material_slot_remove()
            obj.data.materials.clear()

            # Make material
            mat_name = "mat_%05d" % tet.idx
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True

            # Remove default
            mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))

            # Add new transparent bsdf node
            '''
            tbsdf_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')

            # Hook up the node to the surface
            inp = mat.node_tree.nodes['Material Output'].inputs['Surface']
            outp = tbsdf_node.outputs['BSDF']
            mat.node_tree.links.new(inp,outp)
            '''

            # Add new script node
            # https://docs.blender.org/api/2.79b/bpy.types.Node.html#bpy.types.Node
            # Later, find this again using:
            # mat.node_tree.nodes['Script']
            script_node = mat.node_tree.nodes.new(type='ShaderNodeScript')
            script_node.mode = "EXTERNAL"
            script_node.filepath = "/Users/oernst/Desktop/shaderSurface.osl"

            # Hook up the script node
            '''
            inp = tbsdf_node.inputs['Color']
            outp = script_node.outputs['out']
            mat.node_tree.links.new(inp,outp)
            '''

            # Hook up the script node
            inp = mat.node_tree.nodes['Material Output'].inputs['Surface']
            outp = script_node.outputs['out']
            mat.node_tree.links.new(inp,outp)

            # Assign the material to the object
            obj.active_material = mat

            # Deselect the object
            obj.select = False

        return {'FINISHED'}
