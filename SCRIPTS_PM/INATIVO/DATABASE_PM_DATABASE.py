import contextlib
import os
import socket
import sqlite3

# import pandas as pd

# # import duckdb as dk
# import bpy
# import requests
# from bpy.props import BoolProperty

# import pyodbc

# from bpy_plus.file_system import Path

# # IPaddress = socket.gethostbyname(socket.gethostname())


# def conexao_banco():
#     blender_path = os.path.join(Path.blender(), "database")  # > CAMINHO DO PLAYMAKER
#     if not os.path.exists(blender_path):
#         os.mkdir(blender_path)  # > ASSEGURAR QUE A PASTA É CRIADA CASO NÃO EXISTA

#     conect = sqlite3.connect(
#         os.path.join(blender_path, "playmaker.db")
#     )  # > CONNECT DO SQLITE3

#     pm_db = conect.cursor()
#     return pm_db, conect


# senior_db = pyodbc.connect(
#     "Driver={SQL Server};"
#     "Server=191.238.216.86,1515;"
#     "Database=AquSap_prd;"
#     "UID=usrAquBIread;"
#     "PWD=Ll1ne3-8Yx$c4p;"
# )
# senior_cursor = senior_db.cursor()

# senior_tb_produtos = """
#     select p.codpro, d.codder, p.despro, d.desder, p.codori, p.codfam, p.codmod, p.tippro, p.unimed, d.precus, d.premed, d.pesliq, d.pesbru, p.sitpro, d.sitder
#     from e075pro p
#     left join e075der d on (p.codemp = d.codemp and p.codpro = d.codpro)
#     where p.tippro not in ('S', 'D')
#         and p.codemp = 2
#         and p.codori not in (30, 60, 70, 90, 92, 330, 500)
#         and p.codfam not in (530, 540, 550, 560, 590) """

# senior_tb_componentes = """
#         select distinct codmod, codder, seqmod, codcmp, dercmp, qtduti, unime2
#         from e700ctm
#         group by codmod, codder, seqmod, codcmp, dercmp, qtduti, unime2
#         order by codmod"""


# def xlxs_tb_produtos():
#     senior_df = pd.read_sql_query(senior_tb_produtos, senior_db)

#     tb_produtos = os.path.join(blender_path, "tb_produtos.xlsx")

#     senior_df.to_excel(
#         tb_produtos,
#         sheet_name="tb_produtos",
#     )
#     tb_produtos_frame = pd.read_excel(tb_produtos)

#     pm_database = dk.register("tb_produtos", tb_produtos_frame)

#     return pm_database


# def xlxs_tb_componentes():
#     senior_df = pd.read_sql_query(senior_tb_produtos, senior_db)

#     tb_componenes = os.path.join(blender_path, "tb_componentes.xlsx")

#     senior_df.to_excel(
#         tb_componenes,
#         sheet_name="tb_componentes",
#     )
#     senior_tb_componentes = pd.read_excel(tb_componenes)

#     pm_database = dk.register("tb_componentes", senior_tb_componentes)

#     return pm_database


# TODO: CRIAR TABELA EM playmaker.db PARA CONTER TODOS AS PROPRIEDADES DOS PRODUTOS (ALIMENTADO DIRETO DA SENIOR)
# TODO: TABELA RELACIONAL COM DERIVAÇÕES E KITS PF PARA OS PRODUTOS DO PM
# TODO: CRIAR DIFERENCA ENTRE DATAS PARA O BACKUP LOCAL
# TODO: ESTUDAR E USAR SQLALCHEMY PARA FAZER A PONTE ENTRE PANDAS E SENIOR


classes = ()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.notificacao_banco = BoolProperty(default=False)


def unregister():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


if __name__ == "__main__":
    register()
