import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty

class Delaunay_Obj_Vertex(bpy.types.PropertyGroup):
    xval = FloatProperty( default= 0.0, precision=8, name="x" )
    yval = FloatProperty( default= 0.0, precision=8, name="y" )
    zval = FloatProperty( default= 0.0, precision=8, name="z" )
    idx = IntProperty( default = 0, name="idx" )

    def set_from_list_with_idx(self, arr):
        self.idx = arr[0]
        self.xval = arr[1]
        self.yval = arr[2]
        self.zval = arr[3]

    def get_list(self):
        return [self.xval,self.yval,self.zval]

    def get_list_with_idx(self):
        return [self.idx,self.xval,self.yval,self.zval]

class Delaunay_Obj_Face(bpy.types.PropertyGroup):
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

class Delaunay_Obj_Tet(bpy.types.PropertyGroup):
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

# Class to hold the object
class Delaunay_Obj_Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    vert_list = CollectionProperty(type=XML_Obj_Vertex, name = "Vertex list")
    face_list = CollectionProperty(type=XML_Obj_Face, name = "Face list")
    tet_list = CollectionProperty(type=XML_Obj_Tet, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )
