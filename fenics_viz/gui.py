import bpy
# from bpy.app.handlers import persistent
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
import mathutils

from . import objs
from . import obj_buttons
from . import button_read_values

# Register
def register():
    bpy.utils.register_module(__name__)

# Unregister
def unregister():
    bpy.utils.unregister_module(__name__)

# Main panel class
class FVizVizPanel(bpy.types.Panel):
    bl_label = "FEniCS viz" # Panel name
    bl_space_type = "VIEW_3D" # where to put panel
    bl_region_type = "TOOLS" # sub location
    bl_category = "FEniCS viz"

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):
        context.scene.fviz.draw ( self.layout )

#######################################################
#######################################################
# Main GUI property group
#######################################################
#######################################################

# Class for context that contains all the functions
class FVizPropGroup(bpy.types.PropertyGroup):

    # List of XML objects
    obj_list = CollectionProperty(type=objs.Mesh, name="Object List")
    active_obj_idx = IntProperty(name="Active Object Index", default=0)

    # Draw
    def draw(self,layout):

        # XML

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("FEniCS Viz", icon='SURFACE_DATA')

        row = box.row()
        col = row.column()

        col.template_list("Obj_UL_object", "",
                          self, "obj_list",
                          self, "active_obj_idx",
                          rows=2)

        col = row.column(align=True)
        col.operator("fviz.obj_import", icon='ZOOMIN', text="")
        col.operator("fviz.obj_remove", icon='ZOOMOUT', text="")
        col.operator("fviz.obj_remove_all", icon='X', text="")

        row = box.row()
        row.label("Read values")
        row.operator("fviz.read_values")

    # Add a mesh object to the list
    def add_obj(self, name, vert_list, tet_list):
        print("Adding object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.obj_list]
        if not name in current_object_names:
            obj = self.obj_list.add()
            obj.name = name
        else:
            idx = current_object_names.index(name)
            obj = self.obj_list[idx]
            obj.name = name

            # Clear any current tets and verts
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )

        # Go through tets
        for tet_idx, tet in enumerate(tet_list):
            tet_name = name + "_%05d" % tet_idx

            # Make the tet!
            tet_obj = obj.tet_list.add()
            tet_obj.name = tet_name
            tet_obj.idx = tet_idx
            tet_obj.v0 = tet[0]
            tet_obj.v1 = tet[1]
            tet_obj.v2 = tet[2]
            tet_obj.v3 = tet[3]

        # Go through verts
        for vert_idx, vert in enumerate(vert_list):
            # Make the vert!
            vert_obj = obj.vert_list.add()
            vert_obj.idx = vert_idx
            vert_obj.xval = vert[0]
            vert_obj.yval = vert[1]
            vert_obj.zval = vert[2]


    # Remove a mesh object
    def remove_obj(self):
        print("Removing object from the list")

        self.obj_list.remove ( self.active_obj_idx )
        if self.active_obj_idx > 0:
            self.active_obj_idx -= 1

    # Remove all mesh objects
    def remove_all_objs(self):
        print("Removing all objects")

        while len(self.obj_list) > 0:
            self.obj_list.remove ( 0 )
        self.active_obj_idx = 0
