import bpy
import os
from bpy.props import (
    StringProperty,
    IntProperty,
    CollectionProperty,
    BoolProperty,
    PointerProperty,
)
from bpy.types import Operator, PropertyGroup
from mathutils import Color
from funcoes.aqua_props import (
    coll_fixacao,
    excluir_coll,
    excluir_kitpf_coll,
    filtro_alvo,
    lista_funcoes_usuarios,
    lista_usuarios_pm,
    update_conectar,
)

from funcoes.aqua_obj_props import (
    atualizar_cor_metal,
    lista_derivacao,
    lista_derivacoes_items,
    preencher_dados,
    update_altura,
    update_ancoragem,
    update_cor_metal_personalizada,
    update_cor_personalizada,
    update_derivacao,
)

# TODO : CRIAR GRUPO DE PROPRIEDADES 'PLAYMAKER' PARA PROPS GENERICAS


class AQUA_PG_propriedades_cena(PropertyGroup):
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    meus_documentos = os.path.expanduser("~")
    codigo_senior: bpy.props.StringProperty(name="Codigo", update=preencher_dados)

    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    meus_documentos = os.path.expanduser("~")

    # estampa: bpy.props.StringProperty(name='estampa')
    caminho_pdf: bpy.props.StringProperty(
        name="Caminho PDF", default=desktop, subtype="FILE_PATH"
    )
    caminho_csv: bpy.props.StringProperty(
        name="Caminho CSV", default="*.csv*", subtype="FILE_PATH"
    )
    caminho_json: bpy.props.StringProperty(name="Caminho JSON", subtype="FILE_PATH")
    pedido: bpy.props.IntProperty(name="Active", min=1)  # numero inteiro
    modelo: bpy.props.StringProperty(name="Referência", default="")  # automatizar
    modelo_item: bpy.props.StringProperty(name="Modelo: ", default="")  # automatizar
    ref_csv_rev_lic: bpy.props.StringProperty(
        name="Sequência", default=""
    )  # automatizar
    # versao do arquivo .blend
    versao: bpy.props.IntProperty(name="Versao", min=1, max=10, default=1)
    # parte do parque se caso separado
    parte: bpy.props.IntProperty(name="Parte", min=1, max=10, default=1)
    projeto_exclusivo: bpy.props.BoolProperty(name="Projeto Exclusivo", default=False)
    nome_vistas: bpy.props.StringProperty(name="Modelo", default="")
    razao_social: bpy.props.StringProperty(name="Razao Social", default="")
    cnpj_cpf: bpy.props.StringProperty(
        name="CNPJ/CPF",
        default="",
        # update=buscar_cliente,
    )
    rua: bpy.props.StringProperty(name="Rua", default="")
    cep: bpy.props.StringProperty(
        name="CEP",
        default="Preencha o CEP",
        # update=buscar_cep,
    )
    num: bpy.props.StringProperty(name="Num", default="")
    bairro: bpy.props.StringProperty(name="Bairro", default="")
    cidade: bpy.props.StringProperty(name="CIDADE")
    uf: bpy.props.StringProperty(name="UF")
    complementos: bpy.props.StringProperty(name="Complementos", default="")
    telefone: bpy.props.StringProperty(name="Telefone", default="")
    email: bpy.props.StringProperty(name="E-mail", default="")
    # uf: bpy.props.EnumProperty(name="UF", items=(formatar_uf))
    # cidade: bpy.props.EnumProperty(name="CIDADE", items=(formatar_cidade))
    ancoragem: bpy.props.EnumProperty(
        name="Ancoragem",
        default="NENHUM",
        update=update_ancoragem,
        items=[
            ("NENHUM", "NENHUM", "", 0),
            ("PISO", "PISO", "", 1),
            ("TERRA", "TERRA", "", 2),
        ],
    )
    familia: bpy.props.EnumProperty(
        name="Familia",
        default="4020",
        items=[
            ("4010", "4010", "PARQUE", 0),
            ("4020", "4020", "PARQUE UNICO", 1),
            ("4030", "4030", "PROJETO MODULAR", 2),
            ("4040", "4040", "PARQUE LICITAÇAO", 3),
        ],
    )
    incremento: bpy.props.IntProperty(
        name="Código Incremental", soft_min=0, soft_max=999
    )
    qntd_torres: bpy.props.IntProperty(
        name="Qntd. Torres",
        default=1,
    )
    usuarios: bpy.props.EnumProperty(
        name="Função",
        default="PROJETOS",
        # update=update_workspace,
        items=[
            ("VENDEDOR", "VENDEDOR", "VENDEDOR", 0),
            ("SUP_VENDAS", "SUPERVISOR DE VENDAS", "SUP_VENDAS", 1),
            ("PROJETOS", "PROJETOS", "PROJETOS", 2),
            ("ADMIN", "ADMINISTRADOR", "ADMIN", 3),
            ("DESENVOLVEDOR", "DESENVOLVEDOR", "DESENVOLVEDOR", 4),
            ("PCP", "PCP", "PCP", 5),
            ("CATALOGO", "CATALOGO", "CATALOGO", 6),
            ("REVENDA", "REVENDA", "REVENDA", 7),
        ],
    )
    usuario_parque: bpy.props.EnumProperty(
        name="Usuarios parque",
        default="N",
        # update=update_nova_referencia,
        items=[
            ("N", "NENHUM", "NENHUM", 0),
            ("B", "BABY", "BABY", 1),
            ("T", "TEEN", "TEEN", 2),
            ("M", "MISTO", "MISTO", 3),
        ],
    )
    tipo_parque: bpy.props.EnumProperty(
        name="Tipos de parque",
        default="N",
        # update=update_nova_referencia,
        items=[
            ("N", "NENHUM", "NENHUM", 0),
            ("I", "INTERNO", "INTERNO", 1),
            ("L", "LITORAL", "LITORAL", 2),
            ("C", "CAMPO", "CAMPO", 3),
            ("R", "REVENDA", "REVENDA", 4),
            ("P", "PREFEITURA", "PREFEITURA", 5),
        ],
    )
    numero_torres: bpy.props.EnumProperty(
        name="Numero de Torres",
        # update=update_nova_referencia,
        default=0,
        items=[
            ("00", "00", "00", 0),
            ("01", "01", "01", 1),
            ("02", "02", "02", 2),
            ("03", "03", "03", 3),
            ("04", "04", "04", 4),
            ("05", "05", "05", 5),
            ("06", "06", "06", 6),
            ("07", "07", "07", 7),
            ("08", "08", "08", 8),
            ("09", "09", "09", 9),
            ("10", "10", "10", 10),
            ("11", "11", "11", 11),
            ("12", "12", "12", 12),
        ],
    )
    sequencia_senior: bpy.props.StringProperty(name="Sequência Senior", default="")
    gerar_metadados: bpy.props.BoolProperty(name="Gerar Metadados", default=False)
    funcoes_usuarios: bpy.props.EnumProperty(
        name="Funcoes Usuarios",
        items=lista_funcoes_usuarios,
    )
    usuarios_pm: bpy.props.EnumProperty(
        name="Usuario",
        # update=update_scene,
        items=lista_usuarios_pm,
    )
    largura: bpy.props.FloatProperty(
        name="Largura",
        default=10,
        min=1,
        max=100,
        step=50,
        unit="LENGTH",
        # update=update_largura,
    )
    comprimento: bpy.props.FloatProperty(
        name="Comprimento",
        default=10,
        min=1,
        max=100,
        step=50,
        unit="LENGTH",
        # update=update_comprimento,
    )
    peso: bpy.props.FloatProperty(name="Peso", soft_min=0, soft_max=1000000)
    total_itens: bpy.props.IntProperty(
        name="Total_Itens", soft_min=0, soft_max=100000000
    )
    mostrar_painel: bpy.props.BoolProperty(
        name="mostrar_painel",
    )
    vendedor: bpy.props.StringProperty(name="Vendedor", default="")
    observacoes: bpy.props.StringProperty(name="Observacoes", default="")
    validade_proposta_abilitar: bpy.props.BoolProperty(
        name="validade_proposta_abilitar", default=False
    )
    Validade_da_Proposta: bpy.props.StringProperty(
        name="Validade da Proposta", default="15 dias"
    )
    # -----------------------------
    # TAGS DOS PARQUES
    # -----------------------------
    parque_teen: bpy.props.BoolProperty(
        name="parque_teen",
    )
    parque_baby: bpy.props.BoolProperty(
        name="parque_baby",
    )
    parque_litoral: bpy.props.BoolProperty(
        name="parque_litoral",
    )
    parque_restrito: bpy.props.BoolProperty(
        name="parque_restrito",
    )
    parque_teen_baby: bpy.props.BoolProperty(
        name="parque_teen_baby",
    )
    travante: bpy.props.BoolProperty(
        name="travante",
    )
    # -----------------------------
    # PARAMETROS PRECO VENDA
    # -----------------------------
    distancia_km: bpy.props.IntProperty(
        name="Distancia KM", soft_min=0, soft_max=100000000, default=0
    )
    total_torres: bpy.props.IntProperty(
        name="Total Torres", soft_min=0, soft_max=1000, default=0
    )
    DESPESA_IND_TORRE: bpy.props.IntProperty(
        name="DESPESA TORRE", soft_min=0, soft_max=10000, default=0
    )
    MEDIA_HOSPEDAGEM: bpy.props.IntProperty(
        name="MÉDIA HOSPEDAGEM", soft_min=0, soft_max=1000, default=0
    )
    MEDIA_ALIMENTACAO: bpy.props.IntProperty(
        name="MÉDIA ALIMENTAÇÃO", soft_min=0, soft_max=1000, default=0
    )
    CUSTO_KM: bpy.props.FloatProperty(
        name="CUSTO KM", soft_min=0, soft_max=1000, default=0
    )
    ADITIVO: bpy.props.IntProperty(name="ADITIVO", soft_min=0, soft_max=1000, default=0)
    DESCONTO: bpy.props.IntProperty(name="DESCONTO", soft_min=0, soft_max=25, default=0)
    PRECO_VENDA: bpy.props.FloatProperty(name="PRECO VENDA", soft_min=0, default=0.0)
    # -----------------------------
    # LISTA DE LINKS
    # -----------------------------
    caminho_nome: bpy.props.StringProperty(
        name="Caminho",
    )
    caminho_url_nome: bpy.props.StringProperty(name="Caminho url", subtype="FILE_PATH")


class AQUA_PG_propriedades_revenda(PropertyGroup):
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    meus_documentos = os.path.expanduser("~")


class AQUA_PG_propriedades_objeto(PropertyGroup):
    """PROPRIEDADES DE OBJETOS"""

    aqua: bpy.props.BoolProperty(
        name="Objeto AQUA", default=True, description="Objetos cadastrados na Senior"
    )
    codigo: bpy.props.StringProperty(name="Codigo", update=preencher_dados)
    nome: bpy.props.StringProperty(name="Nome")
    peso: bpy.props.FloatProperty(name="Peso", soft_min=0, soft_max=100)
    preco: bpy.props.FloatProperty(name="Preco", soft_min=0, soft_max=10000000)
    leitura_derivacao: bpy.props.StringProperty(name="Leitura Derivacao")
    tipo_derivacao: bpy.props.EnumProperty(
        name="Tipo Derivacao",
        items=[
            ("10_cores", "Cores", "derivacao", 0),
            ("20_tam mad plast", "Madeira Plastica", "mad_plast", 1),
            ("05_unica", "Unica", "unica", 2),
        ],
    )
    derivacao: bpy.props.EnumProperty(items=lista_derivacao, update=update_derivacao)
    altura: bpy.props.FloatProperty(
        name="Altura", default=1.2, min=-2, max=10.000, step=20, update=update_altura
    )
    cor_personalizada: BoolProperty(
        name="Cor Personalizada", default=False, update=update_cor_personalizada
    )
    atualizar_cores: BoolProperty(
        name="Cor Aleatoria",
        default=False,
    )
    ordem: bpy.props.IntProperty(name="Ordem", default=0)
    alvo: PointerProperty(
        name="Ligar", type=bpy.types.Object, update=update_conectar, poll=filtro_alvo
    )
    altura: bpy.props.FloatProperty(
        name="Altura da Fixação",
        default=1.2,
        min=0,
        max=10,
        step=20,
        update=update_altura,
    )
    fixo: BoolProperty(name="fixo", default=False)
    cor_metal_personalizada: BoolProperty(
        name="Cor Personalizada", default=False, update=update_cor_metal_personalizada
    )
    cor_metal: bpy.props.EnumProperty(
        name="Cor Metal",
        update=atualizar_cor_metal,
        default="verde limao pint",
        items=[
            ("verde limao pint", "VERDE LIMAO", "", 0),
            ("amarelo pint", "AMARELO", "", 1),
            ("verde pint", "VERDE", "", 2),
            ("azul pint", "AZUL", "", 3),
        ],
    )
    excluir: BoolProperty(name="Excluir", default=False, update=excluir_coll)
    leitura_kitpf: bpy.props.StringProperty(name="Nome Kit PF")
    # excluir_kitpf_obj: BoolProperty(
    #     name="Excluir", default=False, update=excluir_kitpf_obj
    # )


class AQUA_PG_propriedades_colecao(PropertyGroup):
    ancoragem: bpy.props.EnumProperty(
        name="Fixacao",
        update=coll_fixacao,
        default="NENHUM",
        items=[
            ("NENHUM", "NENHUM", "", 0),
            ("PISO", "PISO", "", 1),
            ("TERRA", "TERRA", "", 2),
        ],
    )

    excluir: BoolProperty(name="Excluir", default=False, update=excluir_coll)
    excluir_kitpf_col: BoolProperty(
        name="Excluir", default=False, update=excluir_kitpf_coll
    )

    nome: bpy.props.StringProperty(name="Nome")
    codigo: bpy.props.StringProperty(name="Codigo")
    categoria: bpy.props.EnumProperty(
        name="Categoria",
        # update=coll_fixacao,
        default="NENHUM",
        items=[
            ("NENHUM", "NENHUM", "", 0),
            ("SUBIDAS", "SUBIDAS", "", 1),
            ("DESCIDAS", "DESCIDAS", "", 2),
            ("PASSAGEMS", "PASSAGEMS", "", 3),
            ("COBERTURAS", "COBERTURAS", "", 4),
            ("FECHAMENTOS", "FECHAMENTOS", "", 5),
            ("AVULSOS", "AVULSOS", "", 6),
            ("OBSOLETOS", "FECHAMENTOS", "", 7),
        ],
    )


class PLAYMAKER_PG_derivacao_e_cor(PropertyGroup):
    name: StringProperty(name="Nenhum", default="Nenhum")


classes = (
    AQUA_PG_propriedades_cena,
    AQUA_PG_propriedades_revenda,
    AQUA_PG_propriedades_objeto,
    AQUA_PG_propriedades_colecao,
    PLAYMAKER_PG_derivacao_e_cor,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.cena = PointerProperty(type=AQUA_PG_propriedades_cena)
    bpy.types.Scene.revenda = PointerProperty(type=AQUA_PG_propriedades_revenda)

    bpy.types.Object.kit_pf = CollectionProperty(type=AQUA_PG_propriedades_objeto)
    bpy.types.Object.aqua = bpy.props.PointerProperty(type=AQUA_PG_propriedades_objeto)
    bpy.types.Object.aqua_cores = CollectionProperty(type=PLAYMAKER_PG_derivacao_e_cor)

    bpy.types.Collection.aqua = bpy.props.PointerProperty(
        type=AQUA_PG_propriedades_colecao
    )
    bpy.types.Collection.kit_pf = CollectionProperty(type=AQUA_PG_propriedades_colecao)

    bpy.types.Scene.nome_arquivo_exportado = bpy.props.StringProperty(
        name="nome",
        default="NOME DO ARQUIVO",
        description="ARQUIVO EXPORTADO PARA ÁREA DE TRABALHO",
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Object.aqua_cores
    del bpy.types.Object.kit_pf
    del bpy.types.Collection.kit_pf

    del bpy.types.Scene.nome_arquivo_exportado


if __name__ == "__main__":
    register()
