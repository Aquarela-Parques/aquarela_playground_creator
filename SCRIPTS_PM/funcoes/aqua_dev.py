import bpy
from bpy.types import Operator, Panel
from funcoes.aqua_funcoes import painel_aviso
import os
import sys
import subprocess

python_exe = os.path.join(sys.prefix, "bin", "python.exe")

bpy.types.Scene.modulos = bpy.props.StringProperty(name="modulos", default="Modulo")


def Upgrade_PIP():
    subprocess.call([python_exe, "-m", "ensurepip"])
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
    return {"FINISHED"}


def Install_Modules():
    modulo = bpy.context.scene.modulos
    subprocess.call([python_exe, "-m", "pip", "install", f"{modulo}"])
    return {"FINISHED"}


def Update_Modules():
    modulo = bpy.context.scene.modulos
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", f"{modulo}"])
    return {"FINISHED"}


def Uninstall_Modules():
    modulo = bpy.context.scene.modulos
    subprocess.call([python_exe, "-m", "pip", "uninstall", f"{modulo}"])
    return {"FINISHED"}


classes = ()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
