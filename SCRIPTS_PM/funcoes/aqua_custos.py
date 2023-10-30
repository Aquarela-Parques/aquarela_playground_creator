import ast
import csv
import os

# from icecream import ic
import bpy
from database.aqua_database import conexao_banco_local
import pandas as pd
from funcoes.aqua_database import conexao_banco_local

from funcoes.aqua_funcoes import (
    # caminhos_pastas,
    caminhos_pastas,
    lista_objetos,
    lista_parafuso,
    painel_aviso,
)

senior = conexao_banco_local()[0]


# SOMAR COMPRIMENTOS DAS COLUNAS
def comprimento_total_colunas():
    lista_comprimentos = []
    for ob in bpy.context.scene.objects:
        if (
            ob.aqua.codigo
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
                "2402400065",
                "2402400066",
                "2402400067",
                "2402400068",
                "2402400069",
                "2402400070",
                "2402400071",
                "2402400072",
                "2402400073",
                "2402400074",
                "2402400075",
                "2402400076",
                "2402400077",
                "2402400078",
                "2402400079",
                "2402400080",
            ]
            and ob.visible_get() == True
        ):
            dev = ob.aqua.leitura_derivacao
            lista_comprimentos.append(int(dev.split("_")[1].split(" ")[0]))

    return str(sum(lista_comprimentos) / 100)


def pesquisa_custo_local(codigo, der):
    """BUSCA NO BANCO LOCAL DO PLAYMAKER"""

    senior.execute(
        """
        SELECT

        tb_produtos.codpro,
        tb_produtos.despro,
        tb_produtos.codder,
        MAX(tb_produtos.precus) / 0.32

        FROM tb_produtos

        WHERE tb_produtos.codpro = ? and tb_produtos.codder = ?

        GROUP BY

        tb_produtos.codpro,
        tb_produtos.despro,
        tb_produtos.codder,
        tb_produtos.precus

        ORDER BY

        tb_produtos.codpro

    """,
        (codigo, der),
    )
    return senior.fetchall()


valores = []


def calculo_custo_parque():
    """CALCULO DE CUSTOS DO PARQUE EM CENA"""
    valores.clear()
    objetos = [
        pesquisa_custo_local(
            i.split("_")[0],
            "UNICA"
            if i.find(f"COLUNA {bpy.context.scene.cena.ancoragem}") != -1
            else i.split("_")[-1][:7],
        )
        for i in lista_objetos()
    ]
    parafusos = [
        pesquisa_custo_local(i.split("_")[0], "UNICA") for i in lista_parafuso()
    ]

    valores.extend(
        pesquisa_custo_local(
            i.split("_")[0],
            "UNICA"
            if i.find(f"COLUNA {bpy.context.scene.cena.ancoragem}") != -1
            else i.split("_")[-1][:7],
        )
        for i in lista_objetos()
    )
    valores.extend(
        pesquisa_custo_local(i.split("_")[0], "UNICA") for i in lista_parafuso()
    )
    return objetos + parafusos, valores


def calculo_custo_parque_local():
    """
    Calculates the cost of the park location.

    This function calculates the cost of the park location by performing the following steps:
    1. Clear the 'valores' list.
    2. Extend the 'valores' list by calling the 'pesquisa_custo_local' function for each element in the 'lista_objetos' list.
       - Split the element by underscore and take the first part as the parameter for 'pesquisa_custo_local' function.
       - If the element contains the value of 'bpy.context.scene.cena.ancoragem' preceded by 'COLUNA', use the value 'UNICA' as the second parameter for 'pesquisa_custo_local' function.
       - Otherwise, take the last part of the element (up to 7 characters) as the second parameter for 'pesquisa_custo_local' function.
    3. Extend the 'valores' list by calling the 'pesquisa_custo_local' function for each element in the 'lista_parafuso' list, using the first part of the element as the parameter and 'UNICA' as the second parameter.
    4. Remove any empty elements from the 'valores' list.
    5. Create a new list 'new_lista' by filtering out any elements in 'valores' that do not contain the string '2102199009'.
    6. Return the 'new_lista' as the result.

    Parameters:
    None

    Returns:
    list: The list of calculated costs for the park location.
    """

    valores.clear()

    valores.extend(
        pesquisa_custo_local(
            i.split("_")[0],
            "UNICA"
            if i.find(f"COLUNA {bpy.context.scene.cena.ancoragem}") != -1
            else i.split("_")[-1][:7],
        )
        for i in lista_objetos()
    )
    valores.extend(
        pesquisa_custo_local(i.split("_")[0], "UNICA") for i in lista_parafuso()
    )

    lista_tratada = []
    for index, i in enumerate(valores):
        if len(i) != 0 and "2102199009" not in str(i[0][0]):
            lista_tratada.append(i)

    return lista_tratada


valores_counter = []
valores_counter_local = []


def contagem_individual_lista():
    """LISTAGEM DE ITENS INDIVIDUAIS PARA EXIBIÇÃO NO PAINEL DE GESTÃO DE CUSTOS"""
    valores_counter.clear()  # SEMPRE LIMPAR LISTA
    for i in calculo_custo_parque():
        valores_counter.append(str(i[0]))
    return valores_counter


def contagem_individual_lista_local():
    """LISTAGEM DE ITENS INDIVIDUAIS PARA EXIBIÇÃO NO PAINEL DE GESTÃO DE CUSTOS"""
    valores_counter_local = [str(i[0]) for i in calculo_custo_parque_local() if i]

    return valores_counter_local


def calculo_soma_total():
    soma_total = 0
    for i in calculo_custo_parque():
        soma_total = round(float(soma_total) + float(i[0][3]), 2)

    return soma_total


def calculo_soma_total_local():
    """
    Calculates the total sum of a local.

    Returns:
        float: The total sum of the local, multiplied by 1.05.
    """
    soma_total = 0
    for i in calculo_custo_parque_local():
        # tabela_custos = {i[0][0]: [i[0][1], i[0][2], i[0][3]]}
        # # print(i, len(i))
        # dataframe = pd.DataFrame.from_dict(
        #     tabela_custos, orient="index", columns=["ITEM", "DERIVACAO", "CUSTO"]
        # )
        # print(dataframe)
        if len(i) == 0:
            soma_total = 9999999999999999999.9999999
            painel_aviso(
                message="ITEM SEM CADASTRO",
                title="CUSTO INVÁLIDO - CONSULTE UM ADMINISTRADOR",
                icon="ERROR",
            )

        else:
            soma_total += float(i[0][3])

    return soma_total


def gerar_tabela_custo_por_item(nome_arquivo):
    """
    Generates a table with the cost per item.

    This function imports the necessary libraries, retrieves the desktop path,
    extracts the cost object list, and defines a generator function to process
    each item. It then creates a pandas DataFrame with the processed data and
    prints it. Finally, it exports the DataFrame to an Excel file on the
    desktop.

    Parameters:
    None

    Returns:
    None
    """
    import pandas as pd

    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

    custo_obj_list = list(bpy.types.CUSTO_PT_custo_producao.custo_obj)

    def lista_tratada():
        for i in custo_obj_list:
            yield ast.literal_eval(i)

    df = pd.DataFrame(
        list(lista_tratada()),
        columns=["CODIGO", "DESCRIÇÃO", "DERIVACAO", "PRECO DE CUSTO"],
    )
    print(df)
    caminho_arquivo = os.path.join(desktop, f"{nome_arquivo} - CUSTO POR ITEM.xlsx")
    df.to_excel(
        caminho_arquivo,
        sheet_name="CUSTO",
    )


def csv_custos():
    with open(f"{caminhos_pastas()[1]}custos.csv", encoding="cp1252", newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    lista_base = [(",".join(i)).split(";") for i in data]

    # DEFINIR INDICES ATRAVES DO CABEÇALHO
    idx_cod = lista_base[0].index("Produto")
    idx_der = lista_base[0].index("Derivação")
    idx_des = lista_base[0].index("Descrição")
    idx_cst = lista_base[0].index("Custo Total")

    # REMOVER CABEÇALHO
    lista_base.remove(lista_base[0])

    lista_custo = []
    lista_obj = []
    for i in lista_base:
        cod = i[idx_cod]
        des = i[idx_des].split(" - ")[0]
        der = i[idx_der]
        cus_l = i[idx_cst]
        try:
            cus = round(float(cus_l.replace(",", ".")), 2)
        except ValueError:
            cus = 0
        lista_custo.append(f"{cod}_{des}_{der}_{cus}")
        lista_obj.append(f"{cod}_{des}_{der}")

    return sorted(lista_custo), sorted(lista_obj)


def custo_producao():
    item_csv = list(csv_custos()[0])
    lst_csv = {"_".join(ic.split("_")[:-1]): ic.split("_")[-1] for ic in item_csv}

    objetos_e_parafusos = [
        f"{obj_sem_derivacao}_{obj.split('_')[-1][:7]}"
        for obj in lista_objetos()
        for obj_sem_derivacao in [obj.rsplit("_", 1)[0]]
    ]
    objetos_e_parafusos.extend(f"{pf}_UNICA" for pf in lista_parafuso())

    lista_custo_obj = [
        f"{oc}_{lst_csv[oc]}" for oc in objetos_e_parafusos if oc in lst_csv
    ]
    lista_obj_sem_custo = [oc for oc in objetos_e_parafusos if oc not in lst_csv]

    return lista_custo_obj, lista_obj_sem_custo


def atualizar_custo():
    cprod = sum(float(i.split("_")[3]) for i in custo_producao()[0])

    cp = cprod + (
        float(comprimento_total_colunas())
        * float(bpy.context.scene.custo_preco.custo_coluna_mp)
    )
    cp = cp * 1.05
    PRECO_VENDA = 0
    PRECO_VENDA = cp / (1 - sum(bpy.context.scene.custo_preco.values()))

    preco_sugerido = round(
        PRECO_VENDA
        * (
            1
            + (bpy.context.scene.custo_preco.ADITIVO / 100)
            - (bpy.context.scene.custo_preco.DESCONTO / 100)
        ),
        2,
    )

    return cp, preco_sugerido


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
