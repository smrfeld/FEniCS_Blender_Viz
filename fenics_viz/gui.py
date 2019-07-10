import bpy
# from bpy.app.handlers import persistent
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
import mathutils

from . import gui_tetgen
from . import gui_xml_objs
from . import gui_xml_operators

# Register
def register():
    bpy.utils.register_module(__name__)

# Unregister
def unregister():
    bpy.utils.unregister_module(__name__)

# Main panel class
class FVizVizPanel(bpy.types.Panel):
    bl_label = "DOLFIN/FEniCS XML viz" # Panel name
    bl_space_type = "VIEW_3D" # where to put panel
    bl_region_type = "TOOLS" # sub location
    bl_category = "DOLFIN/FEniCS XML viz"

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

    # List of mesh objects
    mesh_obj_list = CollectionProperty(type=gui_xml_objs.MeshObject, name="Mesh List")
    active_object_index = IntProperty(name="Active Object Index", default=0)

    # Draw
    def draw(self,layout):

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("Visualize DOLFIN/FEniCS XML", icon='SURFACE_DATA')

        row = box.row()
        col = row.column()

        col.template_list("FViz_UL_object", "",
                          self, "mesh_obj_list",
                          self, "active_object_index",
                          rows=2)

        col = row.column(align=True)
        col.operator("fviz.import_mesh", icon='ZOOMIN', text="")
        col.operator("fviz.mesh_object_remove", icon='ZOOMOUT', text="")
        col.operator("fviz.mesh_object_remove_all", icon='X', text="")

        row = box.row()
        row.label("Import TetGen Delaunay")
        row.operator("fviz.import_tetgen_delaunay")

        row = box.row()
        row.label("Create Voronoi from TetGen Delaunay")
        row.operator("fviz.create_voronoi")

        row = box.row()
        row.label("Import TetGen Voronoi")
        row.operator("fviz.import_tetgen_voronoi")

        row = box.row()
        row.label("Import TetGen Voronoi as separate objs")
        row.operator("fviz.import_tetgen_voronoi_separate")

        row = box.row()
        row.label("Subdivide faces")
        row.operator("fviz.subdivide_faces")

        row = box.row()
        row.label("Visualize timepoint")
        row.operator("fviz.visualize_timepoint")


    # Add a mesh object to the list
    def add_mesh_object(self, name, vert_list, face_list, tet_list):
        print("Adding mesh object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.mesh_obj_list]
        if not name in current_object_names:
            obj = self.mesh_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.mesh_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )

        obj.name = name
        for i in range(0,len(vert_list)):
            obj.vert_list.add()
            obj.vert_list[i].set_from_list_with_idx(vert_list[i])
        for i in range(0,len(face_list)):
            obj.face_list.add()
            obj.face_list[i].set_from_list_with_idx(face_list[i])
        for i in range(0,len(tet_list)):
            obj.tet_list.add()
            obj.tet_list[i].set_from_list_with_idx(tet_list[i])

    # Remove a mesh object
    def remove_mesh_object(self):
        print("Removing mesh object from the list")

        self.mesh_obj_list.remove ( self.active_object_index )
        if self.active_object_index > 0:
            self.active_object_index -= 1

    # Remove all mesh objects
    def remove_all_mesh_objects(self):
        print("Removing all mesh objects")

        while len(self.mesh_obj_list) > 0:
            self.mesh_obj_list.remove ( 0 )
        self.active_object_index = 0
