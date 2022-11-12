import bpy

from bpy.props import (StringProperty,
                       FloatProperty,
                       BoolProperty,
                       PointerProperty,
                       )

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class Properties(PropertyGroup):

    foo: StringProperty(
        name="Foo",
        description=":",
        default="",
        maxlen=1024,
        )


    bar: StringProperty(
        name="Bar",
        description=":",
        default="",
        maxlen=1024,
        )

    flt: FloatProperty(name='Flt', description=':')

    bool: BoolProperty(name='Bool', description=':')
