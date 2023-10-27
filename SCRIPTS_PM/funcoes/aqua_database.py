import os
import sqlite3
import bpy
from funcoes.aqua_funcoes import conexao_banco
from database.aqua_database import conexao_banco_local

pm_produtos = conexao_banco_local()[0]


def conexao_banco_local():
    from bpy_plus.file_system import Path

    database_path = os.path.join(Path.blender(), "database", "playmaker.db")
    conect = sqlite3.connect(database_path)
    pm_db = conect.cursor()
    return pm_db, conect


def select_kits_pf():
    pm_produtos = conexao_banco()[0]
    for produto in pm_produtos.execute(
        """select codpro, despro from tb_produtos where codpro like ('3003020%')"""
    ).fetchall():
        yield produto[0], produto[1]


def create_database_tb_itens(db_file):
    pm_db = db_file

    tb_itens_create = """
        CREATE TABLE IF NOT EXISTS tb_itens (

        codigo integer,
        nome text,
        derivacao_ativa text,
        kits_pf text,
        lista_derivacao text,
        peso real,
        tipo_derivacao text,
        imagem BLOB,
        parametro text,

        UNIQUE ("nome", "parametro")
        UNIQUE ("codigo","nome","derivacao_ativa","kits_pf","lista_derivacao")

        )"""

    pm_db.execute(tb_itens_create)

    conexao_banco()[1].commit()
    conexao_banco()[1].close()


def MapeamentoCores_Senior_Playmaker(cor_objeto):
    CorSenior = ""
    traducao_derivacao_senior = {
        "CINZA": "15_cinza",
        "AMARELO": "20_amarelo",
        "AZUL": "30_azul",
        "LARANJA": "40_laranja",
        "LILAS": "50_lilas",
        "VERDE": "60_verde",
        "LIMAO": "61_limao",
        "VERMELH": "70_vermelho",
        "SORTIDA": "98_sortida",
        "COLORID": "99_colorida",
    }
    for senior, playmaker in traducao_derivacao_senior.items():
        if playmaker == cor_objeto:
            CorSenior = senior
            return CorSenior


def salvar_dados_itens_obj():
    obj_ctx = bpy.context.object.aqua
    nome_objeto = obj_ctx.nome
    codigo_objeto = obj_ctx.codigo
    peso_objeto = obj_ctx.peso

    aqua_db = conexao_banco(database_name="aqua_creator.db", database_folder="database")
    create_database_tb_itens(aqua_db[0])

    pm_db = aqua_db[0]
    con = aqua_db[1]

    tb_itens_insert = """
        INSERT OR REPLACE INTO tb_itens (
            codigo,
            nome,
            derivacao_ativa,
            kits_pf,
            lista_derivacao,
            peso,
            tipo_derivacao,
            parametro
    )
        VALUES (
            ?,  -- codigo
            ?,  -- nome
            ?,  -- derivacao_ativa
            ?,  -- kits_pf
            ?,  -- lista_derivacao
            ?,  -- peso
            ?,  -- tipo_derivacao
            "OBJETO"
    );
    """

    def lista_derivacoes():
        for der_inseridas in bpy.context.scene.propriedades_derivacao_selecionada:
            yield der_inseridas.derivacao_selecionada

    def lista_kits_pf():
        for kits_inseridas in bpy.context.scene.propriedades_kits_pf_selecionados:
            yield kits_inseridas.kits_pf_selecionados

    pm_db.execute(
        tb_itens_insert,
        (
            int(codigo_objeto),
            str(nome_objeto),
            str(list(lista_derivacoes())[0]),
            str(list(lista_kits_pf())),
            str(list(lista_derivacoes())),
            float(peso_objeto),
            str(bpy.context.object.aqua.tipo_derivacao),
        ),
    )

    con.commit()
    con.close()


classes = ()


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
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
