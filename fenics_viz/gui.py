import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy.app.handlers import persistent
import mathutils
from bpy_extras.io_utils import ImportHelper

import os

from . import import_xml_mesh
from . import make_mesh_object
from . import make_subdivided_triangles
from . import import_xml_mesh_values
from . import make_materials_for_subdivided_mesh
from . import color_subdivided_mesh

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
# Tet object list
#######################################################
#######################################################

class VertexObj(bpy.types.PropertyGroup):
    xval = FloatProperty( default= 0.0, precision=8, name="x" )
    yval = FloatProperty( default= 0.0, precision=8, name="y" )
    zval = FloatProperty( default= 0.0, precision=8, name="z" )
    idx = IntProperty( default = 0, name="idx" )
    # subDividedFaceIdxs = CollectionProperty(type=IntProperty, name="Subdivided face list")
    subDividedFaceIdxs = StringProperty ( name="Subdivided face list", default="", description="Subdivided face list" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.xval = arr[1]
        self.yval = arr[2]
        self.zval = arr[3]

    def get_list(self):
        return [self.xval,self.yval,self.zval]

    def get_list_with_idx(self):
        return [self.idx,self.xval,self.yval,self.zval]

class EdgeObj(bpy.types.PropertyGroup):
    idx = IntProperty( default = 0, name="idx" )
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.v0 = arr[1]
        self.v1 = arr[2]

    def get_list(self):
        return [self.v0,self.v1]

    def get_list_with_idx(self):
        return [self.idx,self.v0,self.v1]

class FaceObj(bpy.types.PropertyGroup):
    idx = IntProperty( default = 0, name="idx" )
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.v0 = arr[1]
        self.v1 = arr[2]
        self.v2 = arr[3]

    def get_list(self):
        return [self.v0,self.v1,self.v2]

    def get_list_with_idx(self):
        return [self.idx,self.v0,self.v1,self.v2]

class TetObj(bpy.types.PropertyGroup):
    idx = IntProperty( default = 0, name="idx" )
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )
    v3 = IntProperty( default = 0, name="v3" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.v0 = arr[1]
        self.v1 = arr[2]
        self.v2 = arr[3]
        self.v3 = arr[4]

    def get_list(self):
        return [self.v0,self.v1,self.v2,self.v3]

    def get_list_with_idx(self):
        return [self.idx,self.v0,self.v1,self.v2,self.v3]

# Subdivide faces
class SubdivideFaces(bpy.types.Operator):
    bl_idname = "fviz.subdivide_faces"
    bl_label = "Subdivide faces"

    def execute ( self, context ):

        # Get the selected object
        f = context.scene.fviz
        obj = f.mesh_obj_list[f.active_object_index]

        # Verts and faces
        vert_list = [v.get_list() for v in obj.vert_list]
        face_list = [f.get_list() for f in obj.face_list]

        # Make the subdivided faces
        vert_list_s, edge_list_s, face_list_s = make_subdivided_triangles.make_subdivided_triangles(vert_list, face_list)

        # Make the object
        new_obj = make_mesh_object.make_mesh_object("sub", vert_list_s, edge_list_s, face_list_s)

        # Store face idxs on the verts, so can change material color for animation!

        # Clear first
        for v in obj.vert_list:
            v.subDividedFaceIdxs = ""

        # Write in space deliminited format, for some stupid reason
        # Related to collection of collections not working
        idx_max = len(vert_list)
        for i_face in range(0,len(face_list_s)):
            for v_idx in face_list_s[i_face]:
                if v_idx < idx_max: # Other vertices are new ones; we only care about the existing
                    v = obj.vert_list[v_idx]
                    if v.subDividedFaceIdxs == "":
                        v.subDividedFaceIdxs = str(i_face)
                    else:
                        v.subDividedFaceIdxs += " " + str(i_face)
                    # No more will come for this face
                    break

        # Add materials
        vert_face_strings = [v.subDividedFaceIdxs for v in obj.vert_list]
        make_materials_for_subdivided_mesh.make_materials_for_subdivided_mesh(context, new_obj, vert_face_strings)

        return {"FINISHED"}

class VisualizeTimepoint(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.visualize_timepoint"
    bl_label = "Visualize a timpoint"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    filename_ext = ".xml" # allowed extensions

    # Get the filename
    def execute(self, context):

        # store
        if self.filepath[-4:] != self.filename_ext:
            raise SystemError("Must be: " + str(self.filename_ext) + " format but you chose: " + str(self.filepath[-4:]) + "!")
        else:

            # Filename
            filename = os.path.basename(self.filepath)[:-4]

            # Import
            vals = import_xml_mesh_values.import_xml_mesh_values(self.filepath)

            # Current object
            f = context.scene.fviz
            obj = f.mesh_obj_list[f.active_object_index]

            # Convert vals to verts
            vert_vals = []
            for val in vals:
                tet = obj.tet_list[val[0]]
                if val[1] == 0:
                    vert_vals.append([tet.v0,val[2]])
                elif val[1] == 1:
                    vert_vals.append([tet.v1,val[2]])
                elif val[1] == 2:
                    vert_vals.append([tet.v2,val[2]])
                else:
                    vert_vals.append([tet.v3,val[2]])

            # Sort by vertex
            vert_vals.sort(key=lambda x: x[0])
            vert_vals = [x[1] for x in vert_vals]
            min_val = min(vert_vals)
            max_val = max(vert_vals)

            # Update the colors on the materials
            obj = bpy.data.objects["sub"]
            color_subdivided_mesh.color_subdivided_mesh(context, obj, vert_vals, min_val, max_val)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Class to hold the object
class MeshObject(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=VertexObj, name = "Vertex list")
    edge_list = CollectionProperty(type=EdgeObj, name = "Edge list")
    face_list = CollectionProperty(type=FaceObj, name = "face list")
    tet_list = CollectionProperty(type=TetObj, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

# Model object item to draw in the list
class FViz_UL_object(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The item will be a MeshObject
        # Let it draw itself in a new row:
        item.draw_item_in_row ( layout.row() )

# Button to remove model object
class FVizObjectRemove(bpy.types.Operator):
    bl_idname = "fviz.mesh_object_remove"
    bl_label = "Remove a Mesh Object"
    bl_description = "Remove a mesh object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_mesh_object()
        return {'FINISHED'}

# Button to remove all model objects
class FVizObjectRemoveAll(bpy.types.Operator):
    bl_idname = "fviz.mesh_object_remove_all"
    bl_label = "Remove all Mesh Objects"
    bl_description = "Remove all mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.fviz.remove_all_mesh_objects()
        return {'FINISHED'}

class ImportMesh(bpy.types.Operator, ImportHelper):
    bl_idname = "fviz.import_mesh"
    bl_label = "Import mesh"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    filename_ext = ".xml" # allowed extensions

    # Get the filename
    def execute(self, context):

        # store
        if self.filepath[-4:] != self.filename_ext:
            raise SystemError("Must be: " + str(self.filename_ext) + " format but you chose: " + str(self.filepath[-4:]) + "!")
        else:

            # Filename
            filename = os.path.basename(self.filepath)[:-4]

            # Import
            vert_list, edge_list, face_list, tet_list = import_xml_mesh.import_xml_mesh(self.filepath)

            # Make the objects
            make_mesh_object.make_mesh_object_with_idxs(filename, vert_list, edge_list, face_list)

            # Add to the list
            context.scene.fviz.add_mesh_object(filename, vert_list, edge_list, face_list, tet_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#######################################################
#######################################################
# Main GUI property group
#######################################################
#######################################################

# Class for context that contains all the functions
class FVizPropGroup(bpy.types.PropertyGroup):

    # List of mesh objects
    mesh_obj_list = CollectionProperty(type=MeshObject, name="Mesh List")
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
        row.label("Subdivide faces")
        row.operator("fviz.subdivide_faces")

        row = box.row()
        row.label("Visualize timepoint")
        row.operator("fviz.visualize_timepoint")


    # Add a mesh object to the list
    def add_mesh_object(self, name, vert_list, edge_list, face_list, tet_list):
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
            while len(obj.edge_list) > 0:
                obj.edge_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )

        obj.name = name
        for i in range(0,len(vert_list)):
            obj.vert_list.add()
            obj.vert_list[i].set_from_list_with_idx(vert_list[i])
        for i in range(0,len(edge_list)):
            obj.edge_list.add()
            obj.edge_list[i].set_from_list_with_idx(edge_list[i])
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
