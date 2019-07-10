import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty

class Vertex(bpy.types.PropertyGroup):
    xval = FloatProperty( default= 0.0, precision=8, name="x" )
    yval = FloatProperty( default= 0.0, precision=8, name="y" )
    zval = FloatProperty( default= 0.0, precision=8, name="z" )

    def set_from_list(self, arr):
        self.xval = arr[0]
        self.yval = arr[1]
        self.zval = arr[2]

    def get_list(self):
        return [self.xval,self.yval,self.zval]

class Edge(bpy.types.PropertyGroup):
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )

    def set_from_list(self, arr):
        self.v0 = arr[0]
        self.v1 = arr[1]

    def get_list(self):
        return [self.v0,self.v1]

class TetFace(bpy.types.PropertyGroup):
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )

    def set_from_list(self, arr):
        self.v0 = arr[0]
        self.v1 = arr[1]
        self.v2 = arr[2]

    def get_list(self):
        return [self.v0,self.v1,self.v2]

class Tet(bpy.types.PropertyGroup):
    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )
    v3 = IntProperty( default = 0, name="v3" )

    def set_from_list(self, arr):
        self.v0 = arr[0]
        self.v1 = arr[1]
        self.v2 = arr[2]
        self.v3 = arr[3]

    def get_list(self):
        return [self.v0,self.v1,self.v2,self.v3]

class Idx(bpy.types.PropertyGroup):
    idx = IntProperty( default = 0 )

class CellFace(bpy.types.PropertyGroup):
    verts = CollectionProperty(type=Idx, name="Verts")

    def set_from_list(self, arr):
        for v in arr:
            self.verts.add()
            self.verts[-1].idx = v

    def get_list(self):
        return [v.idx for v in self.verts]

class Cell(bpy.types.PropertyGroup):
    faces = CollectionProperty(type=Idx, name="Faces")

    def set_from_list(self, arr):
        for f in arr:
            self.faces.add()
            self.faces[-1].idx = f

    def get_list(self):
        return [f.idx for f in self.faces]
