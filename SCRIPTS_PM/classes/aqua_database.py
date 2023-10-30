import bpy
from bpy_plus.file_system import Path
import os
from sqlite3 import connect


class Database:
    def __init__(self, database_name, database_folder):
        self.database_name = database_name
        self.database_folder = database_folder

    def criar_database(self, database_name, database_folder):
        if not os.path.exists(blender_path):
            os.mkdir(blender_path)  # > ASSEGURAR QUE A PASTA É CRIADA CASO NÃO EXISTA

        blender_path = os.path.join(
            Path.blender(), database_folder
        )  # > CAMINHO DO PLAYMAKER

        conect = connect(
            os.path.join(blender_path, database_name)
        )  # > CONNECT DO SQLITE3

        pm_db = conect.cursor()
        return pm_db, conect


classes = ()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


if __name__ == "__main__":
    register()
