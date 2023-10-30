import bpy
import os
import subprocess
import sys
import pkg_resources
from bpy.app.handlers import persistent


@persistent
def InstalarModulos(self, context):
    python_exe = os.path.join(sys.prefix, "bin", "python.exe")
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted([i.key for i in installed_packages])

    lista_modulos_necessarios = [
        "activecampaign-python",
        "fpdf2",
        "brazilcep",
        "mariadb",
        "pandas",
        "more_itertools",
        "pyodbc",
        "unidecode",
        "psycopg2",
        "onstro-db",
        "seaborn",
        "timeout_decorator",
        "func_timeout ",
        "Office365-REST-Python-Client",
    ]

    # for i in lista_modulos_necessarios:
    #     if i not in installed_packages_list:
    #         subprocess.call([python_exe, "-m", "pip", "install", f"{i}"])
    #     else:
    #         pass


classes = ()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.app.handlers.load_post.append(InstalarModulos)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
