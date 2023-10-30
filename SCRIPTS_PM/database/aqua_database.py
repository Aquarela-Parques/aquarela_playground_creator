import os

# import socket
import sqlite3

# from pathlib import Path as Pathlib

# import bpy

# import duckdb as dk
# import pandas as pd
# import pyodbc
# import sqlalchemy as sql
# from bpy.props import BoolProperty
# from pyodbc import connect
# from sqlalchemy.engine import URL, create_engine
# from tcp_latency import measure_latency

# from bpy_plus.file_system import Path


def conexao_banco_local():
    from bpy_plus.file_system import Path

    database_path = os.path.join(Path.blender(), "database", "playmaker.db")
    conect = sqlite3.connect(database_path)
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
