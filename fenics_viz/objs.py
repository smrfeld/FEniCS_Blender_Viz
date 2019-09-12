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
    colA = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="colA" )
    colB = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="colB" )
    colC = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="colC" )
    colD = FloatVectorProperty( default = (0.0, 0.0, 0.0), name="colD" )

class Mesh(bpy.types.PropertyGroup):
    name = StringProperty ( name="Name", default="", description="Object Name" )
    tet_list = CollectionProperty(type=Tet, name = "Tet list")
    vert_list = CollectionProperty(type=Vertex, name= "Vert list")

    # Draw in list of objects
    def draw_item_in_row ( self, row ):
        col = row.column()
        col.label ( str(self.name) )

    def recalculate_basis(self, minVal, maxVal, minColor, maxColor):

        # Do it for every tet
        for tet in self.tet_list:

            # Verts
            v0 = self.vert_list[tet.v0]
            v1 = self.vert_list[tet.v1]
            v2 = self.vert_list[tet.v2]
            v3 = self.vert_list[tet.v3]

            # Convert values to fracs
            fracs = [ (v0.value - minVal) / (maxVal - minVal),
                (v1.value - minVal) / (maxVal - minVal),
                (v2.value - minVal) / (maxVal - minVal),
                (v3.value - minVal) / (maxVal - minVal) ]

            # Convert fracs to colors in each channel
            # 4 x 3
            cols = [ [ minColor[icol] + fracs[iv] * (maxColor[icol] - minColor[icol]) for icol in range(0,3) ] for iv in range(0,4) ]

            # colFunc takes input a value (float) and outputs a color (tuple of R,G,B)
            # 4 x 4
            m = np.array([
                [v0.xval,v0.yval,v0.zval,1.0],
                [v1.xval,v1.yval,v1.zval,1.0],
                [v2.xval,v2.yval,v2.zval,1.0],
                [v3.xval,v3.yval,v3.zval,1.0]])
            minv = inv(m)
            colscoeffs = np.dot(minv, np.array(cols))
            # Result us 4 x 3
            tet.colA = colscoeffs[0]
            tet.colB = colscoeffs[1]
            tet.colC = colscoeffs[2]
            tet.colD = colscoeffs[3]
