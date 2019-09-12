import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import numpy as np
from numpy.linalg import inv

class EquivalentTetVert(bpy.types.PropertyGroup):
    tet_idx = IntProperty( default = 0, name="tet_idx" )
    vert_idx = IntProperty( default = 0, name="vert_idx")

class Tet(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    idx = IntProperty(default = 0, name="idx")

    v0 = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="v0" )
    v1 = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="v1" )
    v2 = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="v2" )
    v3 = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="v3" )

    val0 = FloatProperty( default = 0.0, name="val0" )
    val1 = FloatProperty( default = 0.0, name="val1" )
    val2 = FloatProperty( default = 0.0, name="val2" )
    val3 = FloatProperty( default = 0.0, name="val3" )

    # Vals for linear interpolation
    # a*x + b*y + c*z + d
    valA = FloatProperty( default = 0.0, name="colA" )
    valB = FloatProperty( default = 0.0, name="colB" )
    valC = FloatProperty( default = 0.0, name="colC" )
    valD = FloatProperty( default = 0.0, name="colD" )

    # Equivalent tet/vert to vertex..
    v0_equivalents = CollectionProperty(type=EquivalentTetVert, name="Equivalent verts for vert 0")
    v1_equivalents = CollectionProperty(type=EquivalentTetVert, name="Equivalent verts for vert 1")
    v2_equivalents = CollectionProperty(type=EquivalentTetVert, name="Equivalent verts for vert 2")
    v3_equivalents = CollectionProperty(type=EquivalentTetVert, name="Equivalent verts for vert 3")

    def refreshCols(self, colFunc):
        # colFunc takes input a value (float) and outputs a color (tuple of R,G,B)
        m = np.array([
            [self.v0.x,self.v0.y,self.v0.z,1.0],
            [self.v1.x,self.v1.y,self.v1.z,1.0],
            [self.v2.x,self.v2.y,self.v2.z,1.0],
            [self.v3.x,self.v3.y,self.v3.z,1.0]])
        minv = inv(m)
        vals = np.array([self.val0,self.val1,self.val2,self.val3])
        valsCoeffs = minv.vals
        self.valA = valsCoeffs[0]
        self.valB = valsCoeffs[1]
        self.valC = valsCoeffs[2]
        self.valD = valsCoeffs[3]

class Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    tet_list = CollectionProperty(type=Tet, name = "Tet list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )
