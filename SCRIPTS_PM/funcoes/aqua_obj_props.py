import ast
import contextlib
import fnmatch
import json
import os
import re
import sqlite3
from pathlib import Path
from icecream import ic
import bpy
import pandas as pd
from database.aqua_database import conexao_banco_local
from addons.install_modules import CaixaMensagemPM
from bpy_plus.file_system import Path
from classes.aqua_classes import Colecoes

from database.aqua_obj_props import select_codpro

from funcoes.aqua_funcoes import caminhos_pastas, painel_aviso, conexao_banco
from funcoes.aqua_database import conexao_banco_local

pm_produtos = conexao_banco_local()[0]


def lista_derivacoes_items(self, context):
    lista_derivacoes_items = []

    for produto in tuple(select_codpro()):
        print(produto)

        lista_derivacoes_items.append((produto[1], produto[1], produto[1]))

    return lista_derivacoes_items


def preencher_dados(self, context):
    bpy.context.scene.propriedades_derivacao.clear()
    for produto in tuple(select_codpro()):
        bpy.context.scene.propriedades_derivacao.add().derivacao = str(produto[1])
        bpy.context.object.aqua.nome = str(produto[0])
        bpy.context.object.aqua.peso = float(produto[4])

    bpy.context.scene.propriedades_derivacao_selecionada.clear()
    for der in bpy.context.object.aqua_cores.keys():
        bpy.context.scene.propriedades_derivacao_selecionada.add().derivacao_selecionada = (
            der
        )


def lista_derivacao(self, context):
    obj = bpy.context.object
    tipo = obj.aqua.tipo_derivacao
    lista_derivacao = []
    lista_derivacao.clear()

    return [
        ("05_unica", "05_unica", "")
        if tipo == "05_unica"
        else (item, item.split("_")[1], "")
        for item in obj.aqua_cores.keys()
        if item not in lista_derivacao and obj.type == "MESH"
    ]


def update_derivacao(self, context):
    obj = bpy.context.object
    tipo = obj.aqua.tipo_derivacao

    obj.aqua.leitura_derivacao = ""

    if tipo == "10_cores":
        if obj.aqua.derivacao != "98_sortida":
            obj.active_material = bpy.data.materials[obj.aqua.derivacao]

    elif tipo == "20_tam mad plast":
        val_derivacao = float(obj.aqua.derivacao.split("_")[1].split(" ")[0])
        obj.dimensions.z = val_derivacao / 100

    obj.aqua.leitura_derivacao = obj.aqua.derivacao
    # if (
    #     not (
    #         obj.aqua.nome.startswith(f"COLUNA {bpy.context.scene.cena.ancoragem}")
    #         or obj.aqua.nome.startswith("COLUNA MAD PLAST")
    #     )
    #     and obj.hide_viewport == False
    # ):
    #     ic(f"{str(obj.aqua.nome)} -:- {str(obj.aqua.derivacao)}")

    #     obj_importador = {obj.aqua.codigo: [obj.aqua.nome, obj.aqua.derivacao]}
    #     dataframe = pd.DataFrame.from_dict(
    #         obj_importador, orient="index", columns=["ITEM", "DERIVACAO"]
    #     )
    #     ic(dataframe)


def update_altura(self, context):
    bpy.context.object.location.z = bpy.context.object.aqua.altura


def update_cor_personalizada(self, context):
    material = bpy.data.materials["99_colorida"].node_tree


def update_cor_metal_personalizada(self, context):
    print("COR DO METAL PERSONALIZADO")


def atualizar_cor_metal(self, context):
    obj = bpy.context.object
    cor_nova = obj.aqua.cor_metal
    obj.active_material = bpy.data.materials[cor_nova]

    print(f"COR METAL ATUALIZADO: {cor_nova}")


def remove_mat_duplicados():
    material_names = set()

    for obj in bpy.data.objects:
        for slt in obj.material_slots:
            material_name = slt.name.split(".")[0]
            if material_name in bpy.data.materials:
                slt.material = bpy.data.materials.get(material_name)
                material_names.add(material_name)

    for m in bpy.data.materials:
        material_name = m.name.split(".")[0]
        if material_name.isnumeric() and material_name not in material_names:
            bpy.data.materials.remove(m)


def query_colunas_furos_avulsas():
    pm_produtos = conexao_banco()[0]
    """
    Executes a SQL query to retrieve the product code and description from the 'tb_produtos' table in the database.
    The query selects the rows where the product code starts with '240' and orders them by the product code.

    Parameters:
    None

    Returns:
    query_colunas_dict_ (dict): A dictionary where the keys are product codes and the values are lists containing
    the product description, the size of the column, the type of lid, the anchoring, and the column hole.
    """

    pm_produtos.execute(
        """
        select
        produtos.codpro, produtos.despro
        from tb_produtos as produtos
        where produtos.codpro like ('240%')
        order by produtos.codpro
        """
    )

    query_colunas = pm_produtos.fetchall()
    query_colunas_avulsos = []
    query_colunas_avulsos.extend(query_colunas)
    query_colunas_dict_ = {}

    for coluna_ in query_colunas_avulsos:
        tam_col = coluna_[1].split(" ")[2]
        tampa = coluna_[1].split("- ")[-1]
        ancoragem = coluna_[1].split(" ")[1]
        furo_coluna = coluna_[1].split(" - ")[1]
        query_colunas_dict_.update(
            {coluna_[0]: [coluna_[1], tam_col, tampa, ancoragem, furo_coluna]}
        )

    return query_colunas_dict_


def selecionar_objetos_por_nome(obj_name):
    """
    Selects an object in Blender by its name.

    Parameters:
        obj_name (str): The name of the object to be selected.

    Returns:
        None
    """
    bpy.ops.object.select_all(action="DESELECT")  # Deselect all objects
    obj = bpy.data.objects[obj_name]  # Get the object
    obj.select_set(True)  # Select the object
    bpy.context.view_layer.objects.active = obj  # Set the object as active


def report_furos_coluna(torre):
    """Tamanho Madeira Plástica - Altura Plataforma - Aterramento + 5 = Altura Furo"""
    """Tamanho Madeira Plástica - Altura Furo - Aterramento + 5 = Altura Plataforma"""
    nome_coluna = ""
    fix = bpy.context.scene.cena.ancoragem
    alt_plat = 0
    tam_col = ""
    tampa = ""
    if bpy.context.scene.cena.ancoragem == "NENHUM":
        painel_aviso("Selecione uma fixação", "Erro", "ERROR")
    else:
        for obj in bpy.context.scene.objects:
            if (
                obj.name_full.find("COLUNA MAD PLAST") != -1
                and obj.hide_viewport == False
            ):
                # SELECIONAR E ATIVAR OBJETO
                selecionar_objetos_por_nome(obj.name_full)

        for objetos in bpy.data.collections[torre].objects:
            if (
                objetos.name_full.startswith("GUIA_PLATAFORMA")
                and round(objetos.location.z, 2) != 0.1
                and objetos.hide_viewport == False
            ):
                alt_plat = round(
                    bpy.context.scene.objects[objetos.name].location.z * 100
                )
                print(alt_plat)

                for coluna in bpy.data.collections[torre].objects:
                    if (
                        coluna.name_full.startswith("COLUNA MAD PLAST")
                        and coluna.hide_viewport == False
                    ):
                        tam_col = coluna.aqua.derivacao.split("_")[-1].split(" ")[0]

                        child_col = []
                        child_col.clear()

                        child_col = [
                            chld.name.split(".")[0]
                            for chld in coluna.children_recursive
                            if chld.name.split(".")[0]
                            not in ("L PEQUENO GALV", "COQUEIRO M1")
                        ]

                        tampa = "COM TAMPA" if len(child_col) > 1 else "SEM TAMPA"
                        anc = 0 if fix == "PISO" else 10

                        for codigo, colunas in query_colunas_furos_avulsas().items():
                            alt_furo = re.sub(r"[^0-9]", "", colunas[4])
                            if alt_furo.isdigit() == True:
                                alt_furo_ = (
                                    int(tam_col) - int(alt_furo) - int(anc) + 5
                                )  #
                                nome_coluna_ = f"{coluna.name.split(' MAD')[0]} {fix} {tam_col} CM - {alt_furo} CM - {tampa}"

                                if (
                                    int(colunas[1]) == int(tam_col)
                                    and tampa == colunas[2]
                                    and fix == colunas[3]
                                    and int(alt_furo_) == int(alt_plat)
                                    and objetos.hide_viewport == False
                                ):
                                    coluna.aqua.codigo = str(codigo)
                                    coluna.aqua.nome = nome_coluna_

                                    print(codigo, colunas[0], " -->", coluna.name)

        return nome_coluna


def ajustar_derivacao_colunas(torre):
    """
    This function adjusts the derivation of columns based on specific conditions.

    Parameters:
    - torre: The name of the tower.

    Returns:
    None
    """
    cobertura = False
    acesso = False
    alt_plat = 0
    col_der = "10_82 CM"  # INT APENAS PARA DAR ERRO -  "10_82 CM"
    fix = bpy.context.scene.cena.ancoragem

    lista_colunas = [
        col.name
        for col in bpy.data.collections[torre].objects
        if col.aqua.codigo  # TODO FAZER QUERY NAS COLUNAS PARA SEMPRE TER OS DADOS ATUALIZADOS
        in [
            "2402400001",
            "2402400002",
            "2402400003",
            "2402400004",
            "2402400005",
            "2402400006",
            "2402400007",
            "2402400008",
            "2402400009",
            "2402400010",
            "2402400011",
            "2402400012",
            "2402400013",
            "2402400014",
            "2402400015",
            "2402400016",
            "2402400017",
            "2402400018",
            "2402400019",
            "2402400020",
            "2402400021",
            "2402400022",
            "2402400023",
            "2402400024",
            "2402400025",
            "2402400026",
            "2402400027",
            "2402400028",
            "2402400029",
            "2402400030",
            "2402400031",
            "2402400032",
            "2402400033",
            "2402400034",
            "2402400035",
            "2402400036",
            "2402400037",
            "2402400038",
            "2402400039",
            "2402400040",
            "2402400041",
            "2402400042",
            "2402400043",
            "2402400044",
            "2402400045",
            "2402400046",
            "2402400047",
            "2402400048",
            "2402400049",
            "2402400050",
            "2402400051",
            "2402400052",
            "2402400053",
            "2402400054",
            "2402400055",
            "2402400056",
            "2402400057",
            "2402400058",
            "2402400059",
            "2402400060",
            "2402400061",
            "2402400062",
            "2402400063",
            "2402400064",
            "40410001",
        ]
        if not (col["COLUNA_CUSTOM"] == 1)
    ]

    for plataforma in bpy.data.collections[torre].objects:
        if (
            plataforma.name_full.startswith("GUIA_PLATAFORMA")
            and round(plataforma.location.z, 2) != 0.1
        ):
            alt_plat = round(bpy.context.scene.objects[plataforma.name].location.z, 2)

            # DETECTAR TOLDO E ACESSO
            for filhos in plataforma.children:
                if (filhos.aqua.nome.startswith("TOLDO")) == True:
                    cobertura = True
                if filhos.aqua.nome.startswith("ACESSO M1") == True:
                    acesso = True

    # ATUALIZAR "L"
    for obj in bpy.context.scene.objects:
        for prop in obj.keys():
            if prop == "AQUA_L":
                if fix == "PISO":
                    obj["AQUA_L"] = 1
                    obj.update_tag()

                elif fix == "TERRA":
                    obj["AQUA_L"] = 0
                    obj.update_tag()

    for coluna in lista_colunas:
        if cobertura == False:  # ESSA DEVE SER A PRIMEIRA CONDIÇÃO
            col_der = "80_230 CM"

        if alt_plat == 0.45:
            col_der = "80_230 CM"

        if alt_plat == 1.6:
            col_der = "120_300 CM"

        if alt_plat in [0.4, 0.8]:
            if acesso == False:
                col_der = "80_230 CM"

            elif acesso == True:
                col_der = "90_250 CM"

        if cobertura == True:
            # print("===========")
            # print(alt_plat)

            if alt_plat == 1.0:
                col_der = "90_250 CM"

                if acesso == True:
                    col_der = "100_270 CM"
                    if fix == "TERRA":
                        col_der = "110_280 CM"

            elif alt_plat == 1.2:
                col_der = "100_270 CM"
                if fix == "TERRA":
                    col_der = "110_280 CM"

                if acesso == True:
                    col_der = "120_300 CM"

        # AJUSTAR DERIVACAO

        bpy.context.view_layer.objects.active = bpy.data.objects[coluna]
        bpy.data.objects[coluna].aqua.derivacao = col_der
        bpy.data.objects[coluna].aqua.leitura_derivacao = col_der

        # AJUSTAR FIXACAO
        if fix == "PISO":
            bpy.data.objects[coluna].location.z = 0.0
        elif fix == "TERRA":
            bpy.data.objects[coluna].location.z = -0.1

    # print(
    #     f"{torre} FIXACAO:{fix} - PLATAFORMA:{alt_plat} - TOLDO:{cobertura} - ACESSO:{acesso}"
    # )


def furos_colunas():
    """
    Esta função itera sobre os objetos da cena e seleciona e ativa os objetos que têm o nome "COLUNA MAD PLAST"
    e não estão ocultos na viewport. Em seguida, cria uma lista dos objetos filhos do objeto selecionado, excluindo
    certos nomes. A função determina se o objeto selecionado tem mais de um filho e atribui o valor "COM TAMPA" à variável
    'tampa' se tiver, caso contrário, atribui o valor "SEM TAMPA". Também atribui o valor "SEM FURO" à variável 'alt_coluna'
    se a coordenada z da localização do objeto for menor que 1, caso contrário, atribui None. A variável 'anc' recebe o
    valor 0 se a variável 'fix' for igual a "PISO", caso contrário, recebe 10. A função então arredonda a dimensão z do objeto
    multiplicada por 100 e atribui o resultado à variável 'tam_col_scene'. Por fim, a função consulta um dicionário
    de códigos e descrições de colunas e, se uma descrição correspondente for encontrada com base nos valores de 'tam_col_scene',
    'tampa', 'fix' e 'alt_coluna', o atributo 'aqua.codigo' do objeto é atualizado com o código correspondente, o atributo 'aqua.nome'
    do objeto é atualizado com o nome correspondente e informações sobre o código, nome e nome do objeto são impressas.
    Após iterar sobre todos os objetos, a função chama a função 'report_furos_coluna' para cada torre em uma lista de torres.
    """
    fix = bpy.context.scene.cena.ancoragem
    print("COLUNAS:")
    for obj in bpy.context.scene.objects:
        if obj.name_full.find("COLUNA MAD PLAST") != -1 and obj.hide_viewport == False:
            # SELECIONAR E ATIVAR OBJETO
            selecionar_objetos_por_nome(obj.name_full)

            child_col = []
            child_col.clear()
            child_col = [
                chld.name.split(".")[0]
                for chld in obj.children_recursive
                if chld.name.split(".")[0]
                not in (
                    "L PEQUENO GALV",
                    "COQUEIRO M1",
                    "ADICIONAR NA LISTA DE SEPARACAO - SAPATA COQUEIRO E  4 KIT PF L",
                    "ADICIONAR NA LISTA DE SEPARACAO - SAPATA COQUEIRO E  4 KIT ",
                )
            ]

            tampa = "COM TAMPA" if len(child_col) > 1 else "SEM TAMPA"
            alt_coluna = "SEM FURO" if obj.location.z < 1 else None
            anc = 0 if fix == "PISO" else 10

            # SELECIONAR E ATIVAR OBJETO
            selecionar_objetos_por_nome(obj.name_full)

            tam_col_scene = round(obj.dimensions.z * 100)

            for codigo, descricao in query_colunas_furos_avulsas().items():
                nome_coluna_ = f"{obj.name.split(' MAD')[0]} {fix} {tam_col_scene} CM - {alt_coluna} - {tampa}"
                if (
                    int(descricao[1]) == int(tam_col_scene)
                    and tampa == descricao[2]
                    and fix == descricao[3]
                    and alt_coluna == descricao[4]
                ):
                    obj.aqua.codigo = str(codigo)
                    obj.aqua.nome = nome_coluna_
                    print(str(codigo), nome_coluna_, " -->", obj.name_full)

    for torre in list(Colecoes().lista_torre_colecoes_cena()):
        # for torre in lista_torres():
        report_furos_coluna(torre)


def ajustar_todas_torres():
    for i in list(Colecoes().lista_torre_colecoes_cena()):
        # for i in lista_torres():
        ajustar_derivacao_colunas(i)


def update_ancoragem(self, context):
    ajustar_todas_torres()
    furos_colunas()
    pf_novo = "3003020142_KIT PF TORRE L PEQUENO GALV FOGO PISO"
    pf_novo_acop = "3003020143_KIT PF TORRE ACOP L PEQUENO GALV FOGO PISO"

    for obj in bpy.data.objects:
        for pf in obj.kit_pf.keys():
            if pf.split("_")[0] == "3003020140":
                for obj in bpy.data.objects[obj.name_full].kit_pf:
                    obj.name = pf_novo

            elif pf.split("_")[0] == "3003020141":
                for obj in bpy.data.objects[obj.name_full].kit_pf:
                    obj.name = pf_novo_acop

    print(f"Ancoragem alterada para: {bpy.context.scene.cena.ancoragem}")


def carregar_dados_json(obj):
    import ast

    aqua = obj.aqua
    nome_aqua = obj.aqua.nome
    codigo_aqua = obj.aqua.codigo
    nome_gen = os.path.splitext(os.path.basename(nome_aqua))[0]

    pm_db = conexao_banco_local()[0]

    select_props = """
        SELECT
            codigo,
            nome,
            derivacao_ativa,
            kits_pf,
            lista_derivacao,
            peso,
            tipo_derivacao

        FROM
            tb_itens
        WHERE
            codigo = ?
            and parametro = 'OBJETO';
    """

    pm_db.execute(select_props, (codigo_aqua,))
    from icecream import ic

    for info_item in pm_db.fetchall():
        aqua.peso = float(info_item[5])
        aqua.codigo = str(info_item[0])
        aqua.derivaco = info_item[4]
        aqua.preco = float(info_item[0])

        # ic(aqua.codigo, aqua.peso, aqua.derivacao, f"R$ {round(float(aqua.preco), 2)}")

        if aqua.nome != "COLUNA MAD PLAST 9 X 9CM":
            obj.kit_pf.clear()
            with contextlib.suppress(Exception):
                for i in ast.literal_eval(info_item[3]):
                    obj.kit_pf.add().name = i

        tipo = aqua.tipo_derivacao
        obj.aqua_cores.clear()  # Clear the previous list

        for i in ast.literal_eval(info_item[4]):
            obj.aqua_cores.add().name = i

        if aqua.tipo_derivacao == "05_unica":
            aqua.derivacao = "05_unica"

        if aqua.tipo_derivacao == "10_cores":
            aqua.derivacao = info_item[2]

        if aqua.tipo_derivacao == "20_tam mad plast":
            aqua.derivacao = (
                "100_270 CM"
                if bpy.context.scene.cena.ancoragem == "PISO"
                else "110_280 CM"
            )
            val_derivacao = float(aqua.derivacao.split("_")[1].split(" ")[0])
            obj.dimensions.z = val_derivacao / 100

        aqua.leitura_derivacao = aqua.derivacao

        print(
            f"------------------------------------------------- ATUALIZADO - {obj.aqua.nome}"
        )


def carregar_dados_kit_pf_json(obj):
    nome_aqua = obj.aqua.nome
    nome_gen = os.path.splitext(os.path.basename(nome_aqua))[0]

    # -------------------------------------------------------
    # CAMINHO: PEGAR DA OUTRA FUNCAO
    data = caminhos_pastas()[1]
    # -------------------------------------------------------

    # file = Path(data + nome_aqua + ".txt")
    file = Path(f"{data}{nome_aqua}.txt")

    # checar se o arquivo existe
    if not os.path.exists(file):
        print(f"caminho arquivo {str(file)} nao existe")
        bpy.ops.object.aviso_prop("INVOKE_DEFAULT")

    else:
        with open(file) as json_data:
            dados_kit_pf = json.load(json_data)

        for item, key in dados_kit_pf.items():
            if item == "kits_pf" and obj.aqua.nome != "COLUNA MAD PLAST 9 X 9CM":
                obj.kit_pf.clear()  # LIMPAR LISTA ANTERIOR
                for i in dados_kit_pf[item]:
                    obj.kit_pf.add().name = i
                    ##
                    for col in bpy.data.collections:
                        if (
                            not col.name.isdigit()
                            and not col.name.startswith("GERAR_VISTAS")
                            and col.kit_pf.keys() != []
                        ):
                            col.kit_pf.add().name = i

        print(
            f"------------------------------------------------- ATUALIZADO KIT PF - {obj.aqua.nome}"
        )


def carregar_dados_objeto(conjunto_objetos):
    for obj in conjunto_objetos:
        if obj.aqua.nome != "":
            selecionar_objetos_por_nome(obj.name_full)

            # bpy.ops.object.select_all(
            #     action="DESELECT"
            # )  # DESLECIONAR QUALQUER OBJETO SELECIONADO

            nome = obj.name_full  # NOME OBJETO NO BLENDER

            # SELECIONAR E ATIVAR OBJETO
            bpy.context.view_layer.objects.active = bpy.data.objects[nome]
            bpy.data.objects[nome].select_set(True)

            if bpy.context.object.name_full.startswith("COLUNA MAD PLAST"):
                bpy.ops.objects.ajustar_colunas()
            else:
                # CARREGAR DADOS DO JSON
                carregar_dados_json(obj)


def nomes_colunas():
    pm_produtos.execute(
        """
    select
    produtos.codpro, produtos.despro
    from tb_produtos as produtos
    where produtos.codpro like ('240%')
    order by produtos.codpro
    """
    )
    return [colunas[1] for colunas in pm_produtos.fetchall()]


def carregar_dados_kit_pf_objeto(self, conjunto_objetos):
    """
    Carrega os dados do kit PF de um conjunto de objetos.

    Parameters:
        self (objeto): O objeto atual.
        conjunto_objetos (lista): Uma lista de objetos.

    Returns:
        None
    """
    try:
        for obj in conjunto_objetos:
            if obj.aqua.nome != "" and obj.aqua.nome not in nomes_colunas():
                selecionar_objetos_por_nome(obj.name_full)
                nome_aqua = obj.aqua.nome
                nome_gen = os.path.splitext(os.path.basename(nome_aqua))[0]

                # -------------------------------------------------------
                # CAMINHO: PEGAR DA OUTRA FUNCAO
                data = caminhos_pastas()[1]
                # -------------------------------------------------------

                pm_db = conexao_banco_local()[0]

                select_props = """
                    SELECT
                        kits_pf
                    FROM
                        tb_itens
                    WHERE
                        nome = ?
                        and nome not like ('COLUNA MAD PLAST%')
                        and parametro = 'OBJETO';
                """

                pm_db.execute(select_props, (obj.aqua.nome,))

                for info_item in pm_db.fetchall():
                    obj.kit_pf.clear()  # LIMPAR LISTA ANTERIOR
                    try:
                        for kit in ast.literal_eval(info_item[0]):
                            if not obj.name.startswith("COLUNA MAD PLAST"):
                                obj.kit_pf.add().name = kit
                                print(f"ATUALIZADO KIT PF: {obj.aqua.nome}")
                    except TypeError as error1:
                        print(obj.aqua.nome, error1)

        for col in bpy.data.collections:
            nome_colecao = col.name_full.split(".")[0]
            if col.kit_pf.keys() != []:
                col.kit_pf.clear()

                pm_db = conexao_banco_local()[0]

                select_props = """
                    SELECT
                        kits_pf
                    FROM
                        tb_itens
                    WHERE
                        nome = ?
                        and parametro = 'COLECAO';
                """

                pm_db.execute(select_props, (nome_colecao,))

                for info_item in pm_db.fetchall():
                    try:
                        for kit_pf in ast.literal_eval(info_item[0]):
                            col.kit_pf.add().name = kit_pf
                    except TypeError as error:
                        print(obj.aqua.nome, error)
    except ReferenceError as E:
        print(E)


def pasta_cores():
    pasta_cores = caminhos_pastas()[2]
    padrao = "*.blend"

    for path, subdirs, files in os.walk(pasta_cores):
        for name in files:
            if fnmatch.fnmatch(
                name, padrao
            ):  # Use fnmatch.fnmatch to check the pattern
                cor = os.path.splitext(name)[0]
                caminho = os.path.join(
                    pasta_cores, cor + ".blend", "Material"
                )  # Use os.path.join for path manipulation
                bpy.ops.wm.append(filename=cor, directory=caminho)


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
