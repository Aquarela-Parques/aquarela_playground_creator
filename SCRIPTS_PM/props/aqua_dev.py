import bpy
import os
from bpy.props import (
    StringProperty,
    IntProperty,
    CollectionProperty,
    BoolProperty,
    PointerProperty,
)
import sys
from bpy.types import Operator, PropertyGroup


class AQUA_PG_propriedades_dev(PropertyGroup):
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    meus_documentos = os.path.expanduser("~")
    python_exe = os.path.join(sys.prefix, "bin", "python.exe")
    modulos = bpy.props.StringProperty(name="modulos", default="Modulo")


classes = (AQUA_PG_propriedades_dev,)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.dev = PointerProperty(type=AQUA_PG_propriedades_dev)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
