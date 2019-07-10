import bpy
# from bpy.app.handlers import persistent
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
import mathutils

from . import gui_tetgen
from . import gui_xml_objs
from . import gui_xml_operators
from . import gui_tetgen_delaunay_objs
from . import gui_tetgen_voronoi_objs

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

    # List of XML objects
    xml_obj_list = CollectionProperty(type=gui_xml_objs.XML_Obj_Mesh, name="XML Object List")
    active_xml_obj_idx = IntProperty(name="Active XML Object Index", default=0)

    # List of Delaunay objects (from tetgen)
    delaunay_obj_list = CollectionProperty(type=gui_tetgen_delaunay_objs.Delaunay_Obj_Mesh, name="Delaunay Object List")
    active_delaunay_obj_idx = IntProperty(name="Active Delaunay Object Index", default=0)

    # List of Voronoi objects (from tetgen)
    voronoi_obj_list = CollectionProperty(type=gui_tetgen_voronoi_objs.Voronoi_Obj_Mesh, name="Voronoi Object List")
    active_voronoi_obj_idx = IntProperty(name="Active Voronoi Object Index", default=0)

    # Draw
    def draw(self,layout):

        # XML

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("Visualize DOLFIN/FEniCS XML", icon='SURFACE_DATA')

        row = box.row()
        col = row.column()

        col.template_list("XML_Obj_UL_object", "",
                          self, "xml_obj_list",
                          self, "active_xml_obj_idx",
                          rows=2)

        col = row.column(align=True)
        col.operator("fviz.xml_obj_import", icon='ZOOMIN', text="")
        col.operator("fviz.xml_obj_remove", icon='ZOOMOUT', text="")
        col.operator("fviz.xml_obj_remove_all", icon='X', text="")

        row = box.row()
        row.label("Subdivide faces")
        row.operator("fviz.xml_obj_subdivide_faces")

        row = box.row()
        row.label("Visualize timepoint")
        row.operator("fviz.xml_obj_visualize_timepoint")

        # TETGEN

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("TetGen", icon='SURFACE_DATA')

        # Delaunay

        row = box.row()
        row.label("Delaunay meshes")

        row = box.row()
        col = row.column()

        col.template_list("Delaunay_Obj_UL_object", "",
                          self, "delaunay_obj_list",
                          self, "active_delaunay_obj_idx",
                          rows=2)

        col = row.column(align=True)
        col.operator("fviz.delaunay_obj_import", icon='ZOOMIN', text="")
        col.operator("fviz.delaunay_obj_remove", icon='ZOOMOUT', text="")
        col.operator("fviz.delaunay_obj_remove_all", icon='X', text="")

        '''
        row = box.row()
        row.label("Create Voronoi from TetGen Delaunay")
        row.operator("fviz.create_voronoi")
        '''

        # Voronoi

        row = box.row()
        row.label("Voronoi meshes")

        row = box.row()
        col = row.column()

        col.template_list("Voronoi_Obj_UL_object", "",
                          self, "voronoi_obj_list",
                          self, "active_voronoi_obj_idx",
                          rows=2)

        col = row.column(align=True)
        col.operator("fviz.voronoi_obj_import", icon='ZOOMIN', text="")
        col.operator("fviz.voronoi_obj_remove", icon='ZOOMOUT', text="")
        col.operator("fviz.voronoi_obj_remove_all", icon='X', text="")

        row = box.row()
        row.label("Import TetGen Voronoi as separate objs")
        row.operator("fviz.import_tetgen_voronoi_separate")

    # Add a mesh object to the list
    def add_xml_obj(self, name, vert_list, face_list, tet_list):
        print("Adding XML object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.xml_obj_list]
        if not name in current_object_names:
            obj = self.xml_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.xml_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )
            while len(obj.vertex_subdivided_face_list) > 0:
                obj.vertex_subdivided_face_list.remove ( 0 )

        obj.name = name
        for v in vert_list:
            obj.vert_list.add()
            obj.vert_list[-1].set_from_list(v)
            # Also add for subdivided faces
            obj.vertex_subdivided_face_list.add()
        for f in face_list:
            obj.face_list.add()
            obj.face_list[-1].set_from_list(f)
        for t in tet_list:
            obj.tet_list.add()
            obj.tet_list[-1].set_from_list(t)

    # Remove a mesh object
    def remove_xml_obj(self):
        print("Removing XML object from the list")

        self.xml_obj_list.remove ( self.active_xml_obj_idx )
        if self.active_xml_obj_idx > 0:
            self.active_xml_obj_idx -= 1

    # Remove all mesh objects
    def remove_all_xml_objs(self):
        print("Removing all XML objects")

        while len(self.xml_obj_list) > 0:
            self.xml_obj_list.remove ( 0 )
        self.active_xml_obj_idx = 0

    # Add a mesh object to the list
    def add_delaunay_obj(self, name, vert_list, face_list, tet_list):
        print("Adding Delaunay object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.delaunay_obj_list]
        if not name in current_object_names:
            obj = self.delaunay_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.delaunay_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )

        obj.name = name
        for v in vert_list:
            obj.vert_list.add()
            obj.vert_list[-1].set_from_list(v)
        for f in face_list:
            obj.face_list.add()
            obj.face_list[-1].set_from_list(f)
        for t in tet_list:
            obj.tet_list.add()
            obj.tet_list[-1].set_from_list(t)

    # Remove a mesh object
    def remove_delaunay_obj(self):
        print("Removing Delaunay object from the list")

        self.delaunay_obj_list.remove ( self.active_delaunay_obj_idx )
        if self.active_delaunay_obj_idx > 0:
            self.active_delaunay_obj_idx -= 1

    # Remove all mesh objects
    def remove_all_delaunay_objs(self):
        print("Removing all Delaunay objects")

        while len(self.delaunay_obj_list) > 0:
            self.delaunay_obj_list.remove ( 0 )
        self.active_delaunay_obj_idx = 0

    # Add a mesh object to the list
    def add_voronoi_obj(self, name, vert_list, face_list, cell_list):
        print("Adding Voronoi object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.voronoi_obj_list]
        if not name in current_object_names:
            obj = self.voronoi_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.voronoi_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.cell_list) > 0:
                obj.cell_list.remove ( 0 )

        obj.name = name
        for v in vert_list:
            obj.vert_list.add()
            obj.vert_list[-1].set_from_list(v)
        for f in face_list:
            obj.face_list.add()
            obj.face_list[-1].set_from_list(f)
        for c in cell_list:
            obj.cell_list.add()
            obj.cell_list[-1].set_from_list(c)

    # Remove a mesh object
    def remove_voronoi_obj(self):
        print("Removing Voronoi object from the list")

        self.voronoi_obj_list.remove ( self.active_voronoi_obj_idx )
        if self.active_voronoi_obj_idx > 0:
            self.active_voronoi_obj_idx -= 1

    # Remove all mesh objects
    def remove_all_voronoi_objs(self):
        print("Removing all Voronoi objects")

        while len(self.voronoi_obj_list) > 0:
            self.voronoi_obj_list.remove ( 0 )
        self.active_voronoi_obj_idx = 0
