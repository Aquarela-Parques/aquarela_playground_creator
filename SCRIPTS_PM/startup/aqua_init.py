import bpy
import os
import importlib
from sys import path


def ListagemModulos():
    """
    Generates a list of modules in the specified directory.

    Returns:
        A generator that yields tuples containing the name of the
        directory and the name of the file for each module found.
    """
    # Adicionar o caminho do diretório aos caminhos de módulo
    path.append(bpy.utils.script_paths_pref()[0])
    # Obter o caminho do diretório que contém os módulos
    module_dir = os.path.dirname(bpy.utils.script_paths_pref()[0])
    addons = "addons"
    bpy_plus = "bpy_plus"
    experimental = "experimental"
    templates = "templates"
    for root, dirs, files in os.walk(bpy.utils.script_paths_pref()[0]):
        if addons in dirs:
            dirs.remove(addons)
        if bpy_plus in dirs:
            dirs.remove(bpy_plus)
        if experimental in dirs:
            dirs.remove(experimental)
        if templates in dirs:
            dirs.remove(templates)

        for file in files:
            if (
                file.endswith(".py")
                and not os.path.basename(root).startswith("startup")
                and not os.path.basename(root).startswith("__")
                and not os.path.basename(root).startswith("INATIVO")
                and not os.path.basename(root).startswith("templates_py")
            ):
                yield os.path.basename(root), file


def RegistrarModulos():
    """
    Função para registrar módulos encontrados no diretório de scripts do Blender.

    Esta função itera sobre os módulos encontrados e tenta registrá-los.
    """
    for modulo_name in list(ListagemModulos()):
        module_name = os.path.splitext(modulo_name[1])[0]
        try:
            module = importlib.import_module(
                f"{modulo_name[0]}.{module_name}", package=None
            )
            module.register()
            # print("PASTA:", modulo_name[0], "MODULO:", module_name)
        except:
            module = importlib.import_module(module_name, package=None)
            module.register()
            # print("MODULO:", module_name)

    return {"FINISHED"}


RegistrarModulos()
classes = ()


def register():
    """
    Função de registro das classes.

    Esta função deve ser chamada para registrar as classes no Blender.
    """
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    """
    Função de desregistro das classes.

    Esta função deve ser chamada para desregistrar as classes no Blender.
    """
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
