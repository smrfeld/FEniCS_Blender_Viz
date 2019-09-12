import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ImportHelper

import numpy as np
from numpy.linalg import inv

class Vertex(bpy.types.PropertyGroup):
    idx = IntProperty( default=0, name="idx")
    xval = FloatProperty( default= 0.0, precision=8, name="x" )
    yval = FloatProperty( default= 0.0, precision=8, name="y" )
    zval = FloatProperty( default= 0.0, precision=8, name="z" )
    value = FloatProperty( default = 0.0, name="value" )

class Tet(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    idx = IntProperty(default = 0, name="idx")

    v0 = IntProperty( default = 0, name="v0" )
    v1 = IntProperty( default = 0, name="v1" )
    v2 = IntProperty( default = 0, name="v2" )
    v3 = IntProperty( default = 0, name="v3" )

    # Vals for linear interpolation
    # a*x + b*y + c*z + d
    valA = FloatProperty( default = 0.0, name="colA" )
    valB = FloatProperty( default = 0.0, name="colB" )
    valC = FloatProperty( default = 0.0, name="colC" )
    valD = FloatProperty( default = 0.0, name="colD" )

class Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    tet_list = CollectionProperty(type=Tet, name = "Tet list")
    vert_list = CollectionProperty(type=Vertex, name= "Vert list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

    def recalculate_basis(self):

        # Do it for every tet
        for tet in self.tet_list:

            v0 = self.vert_list[tet.v0]
            v1 = self.vert_list[tet.v1]
            v2 = self.vert_list[tet.v2]
            v3 = self.vert_list[tet.v3]

            # colFunc takes input a value (float) and outputs a color (tuple of R,G,B)
            m = np.array([
                [v0.xval,v0.yval,v0.zval,1.0],
                [v1.xval,v1.yval,v1.zval,1.0],
                [v2.xval,v2.yval,v2.zval,1.0],
                [v3.xval,v3.yval,v3.zval,1.0]])
            minv = inv(m)
            vals = np.array([v0.value,v1.value,v2.value,v3.value])
            valsCoeffs = np.dot(minv, vals)
            tet.valA = valsCoeffs[0]
            tet.valB = valsCoeffs[1]
            tet.valC = valsCoeffs[2]
            tet.valD = valsCoeffs[3]
