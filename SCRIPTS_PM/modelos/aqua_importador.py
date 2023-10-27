import contextlib
import glob
import os
import random

import bpy

# from pm_operadores import CONJUNTO_OT_confirmar_acao
from bpy.props import BoolProperty
from bpy.types import Operator, Panel

from funcoes.aqua_funcoes import (
    caminhos_pastas,
)
from funcoes.aqua_gerar_vistas import (
    Update_Ocultar_Colecoes,
)  # salvar_dados,; importado,; lista_peso,; update_nova_referencia,
from funcoes.aqua_importador import nao_importado
from funcoes.aqua_obj_props import ajustar_todas_torres, furos_colunas

############################
## ANTIGO PM_IMPORTAR_OBJ ##
############################


def obj_category_update(wm, context):
    with contextlib.suppress(Exception):
        cat = bpy.data.window_managers["WinMan"].obj_category
        bpy.data.window_managers["WinMan"].obj_preview_dir = (
            bpy.data.window_managers["WinMan"].caminho_modelo + cat
        )


def obj_preview_update(wm, context):
    pass


def obj_category_items(self, context):
    folder = bpy.data.window_managers["WinMan"].caminho_modelo

    if not os.path.exists(folder):
        return [("", "", "")]

    # list_ = [("SELECIONE", "SELECIONE", "SELECIONE")]
    list_ = []

    for entry in os.scandir(folder):
        if entry.is_dir() and not entry.name.startswith("."):
            id_ = entry.name
            name_ = f"{entry.name} "
            list_.append((id_, name_, ""))

    if not list_:
        list_ = [("", "", "")]

    lista = []
    return sorted(list_)


def obj_preview_items(self, context):
    # PASTA MODELOS

    bpy.context.window_manager.caminho_modelo = caminhos_pastas()[0]

    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.obj_preview_dir

    pcoll = preview_collections["main"]

    if directory == pcoll.obj_preview_dir:
        return pcoll.obj_preview

    diretorio = directory.split("\\")[-1]
    print(f"Abrindo o diretório: {diretorio}")

    if directory and os.path.exists(directory):
        image_paths = glob.glob(os.path.join(directory, "*.png"))
        for i, filepath in enumerate(image_paths):
            name = os.path.basename(filepath)
            icon = pcoll.get(name)
            thumb = pcoll[name] if icon else pcoll.load(name, filepath, "IMAGE")
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.obj_preview = sorted(enum_items)
    pcoll.obj_preview_dir = directory

    return pcoll.obj_preview


def objetos_cena():
    obj_cena = []
    obj_cena.clear()
    return [
        ob.name_full
        for ob in bpy.context.scene.objects
        if ob.show_bounds == True
        if ob.name_full not in obj_cena
    ]


# def objetos_cena():
#     for ob in bpy.context.scene.objects:
#         if ob.show_bounds == True:
#             if ob not in list(objetos_cena()):
#                 yield ob.name_full


def old_list():
    col_old_list = []
    obj_old_list = []

    for col in bpy.data.collections:
        col_old_list.append(col)
    for obj in bpy.data.objects:
        obj_old_list.append(obj)

    return col_old_list, obj_old_list


# def _old_list():
#     col_old_list = []
#     obj_old_list = []

#     for col in bpy.data.collections:
#         col_old_list.append(col)
#     for obj in bpy.data.objects:
#         obj_old_list.append(obj)

#     yield col_old_list
#     yield obj_old_list


# LISTA DE OBJETOS DA CENA APOS IMPORTAR NOVA COLEÇÃO
def cur_list():
    col_cur_list = list(bpy.data.collections)
    obj_cur_list = list(bpy.data.objects)
    return col_cur_list, obj_cur_list


# RESULTADO DA SUBTRAÇÃO DA LISTA ANTIGA DE DENTRO DA LISTA NOVA
def res(old_col, old_obj, cur_col, cur_obj):
    col_res = [a for a in cur_col if a not in old_col]
    obj_res = [a for a in cur_obj if a not in old_obj]
    return col_res, obj_res


def importar_torre(self, context):
    lista = objetos_cena()
    category = "MODELOS_PM"
    object_name = "TORRE"
    file_path = (
        f"{bpy.data.window_managers['WinMan'].caminho_modelo}\\{object_name}.blend"
    )
    inner_path = "Collection"
    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name,
    )
    for ob in bpy.context.scene.objects:
        if ob.name_full not in lista and ob.show_bounds == True and ob.type != "EMPTY":
            ob.location.x = random.randint(-4, 4)
            ob.location.y = random.randint(-4, 4)


def UI_vendedor(self, context):
    # importar = None
    layout = self.layout

    wm = context.window_manager
    rt = context.scene.cena

    fucking_update = False
    if bpy.context.window_manager.obj_category == "1 - TORRES" and not fucking_update:
        bpy.context.window_manager.obj_category.startswith("CATALOGO")
        fucking_update = True

    if rt.ancoragem == "NENHUM":
        layout.label(text="SELECIONE UM TIPO DE FIXACAO")
        row = layout.row()
        row.scale_y = 2
        row.prop(rt, "ancoragem")
    else:
        if bpy.types.MODELOS_PT_painel_modelos.importar == False:
            nao_importado(self, context)

        if bpy.types.MODELOS_PT_painel_modelos.importar == True:
            rt = context.scene.cena
            # importado(self, context)
            row = layout.row()
            layout.separator()
            layout.separator()
            # row.label(text=f"PESO: {lista_peso()[0]}kg")
            row.label(
                text=f"CUSTO TOTAL: R${bpy.types.CUSTO_PT_custo_producao.custo_producao}"
            )
            row = layout.row()
            row.prop(rt, "pedido")
            row.operator(
                "admin.admin_op", text="Inserir no aplicativo"
            ).action = "INSERT_TABELA_APLICATIVO"
            row = layout.row()
            row.operator("operador.printar_lista", text="Criar Lista de Itens")
            row = layout.row()
            row.operator("object.operador_voltar")


def UI_Modelos(self, context):
    erro = False
    layout = self.layout
    wm = context.window_manager
    scene = context.scene
    rt = context.scene.cena
    row = layout.row()
    row.scale_y = 1

    layout.prop(wm, "obj_category", text="Categoria", expand=False)
    layout.template_icon_view(
        wm, "obj_preview", show_labels=True, scale=6, scale_popup=6
    )
    row = layout.row()
    cf = layout.column_flow(columns=2, align=False)
    cf.scale_y = 1.8
    cf.operator(
        "modelos.obj_preview",
        text=f"IMPORTAR: {wm.obj_preview.split('.')[0]}",
        icon="PLUS",
    )

    cf.operator(
        "modelos.ferramentas", text="ADICIONAR TORRE", icon="SNAP_VERTEX"
    ).action = "importar_torre"
    if bpy.context.scene.cena.usuarios in ["ADMIN", "DESENVOLVEDOR"]:
        row2 = layout.row(align=True)
        row2.scale_y = 1.5
        row2.operator(
            "modelos.substituir_objetos",
            text="SUBSTITUIR OBJETOS SELECIONADO",
            icon="CON_ACTION",
        )
        row2 = layout.row(align=True)
        row2.alert = True
        row2.scale_y = 1.5
        # row2.operator(
        #     CONJUNTO_OT_confirmar_acao.bl_idname,
        #     text="DESEJA ABRIR O OBJETO?",
        #     icon="QUESTION",
        # )

    # layout.label(text=f"Peso Total: {lista_peso()[0]}kg")
    layout.separator()
    if not bpy.context.selected_objects:
        pass
    else:
        try:
            # EXIBINDO NOME DA COLECAO SELECIONADA
            # MAIS BOTAO EXCLUIR
            act_obj = bpy.context.active_object.name_full
            scale = 0.4
            for col in bpy.data.objects[act_obj].users_collection:
                if (
                    not col.name.isdigit()
                    and col.hide_viewport == False
                    and col.name_full != "GERAR_VISTAS"
                ):
                    fix = bpy.context.scene.cena.ancoragem
                    filtro = ["TERRA", "PISO"]
                    box = layout.box()
                    row1 = box.row()
                    row1.alert = True
                    row1.label(text=col.name_full)  # .split(".")[0])
                    row1.label(text=bpy.context.object.aqua.codigo)  # .split(".")[0])
                    if col.kit_pf.keys() != []:
                        for k in col.kit_pf.keys():
                            if fix in k:
                                row1 = box.row()
                                row1.label(text=k.split("_")[0], icon="TOOL_SETTINGS")
                                row1.label(text=k.split("_")[1])

                            else:
                                if not any(word in k for word in filtro):
                                    row = box.row()
                                    row.scale_y = scale
                                    row.label(
                                        text=k.split("_")[0], icon="TOOL_SETTINGS"
                                    )
                                    row.label(text=k.split("_")[1])
                    else:
                        for obj in col.objects:
                            if obj.hide_viewport == False and obj.kit_pf.keys() != []:
                                for k in obj.kit_pf.keys():
                                    if fix in k:
                                        row1 = box.row()
                                        row1.label(
                                            text=k.split("_")[0], icon="TOOL_SETTINGS"
                                        )
                                        row1.label(text=k.split("_")[1])
                                    else:
                                        if not any(word in k for word in filtro):
                                            row1 = box.row()
                                            row1.label(
                                                text=k.split("_")[0],
                                                icon="TOOL_SETTINGS",
                                            )
                                            row1.label(text=k.split("_")[1])
                    row1 = box.row()
                    row1.alert = True
                    row1.scale_y = 1.4
                    row1.prop(
                        col.aqua,
                        "excluir",
                        toggle=True,
                        icon="CANCEL",
                        text="EXCLUIR ITEM",
                    )

            layout = self.layout
            row = layout.row()

            row1 = layout.row()
            icon = "TRIA_DOWN" if context.scene.subpanel_status else "TRIA_RIGHT"
            row1.prop(context.scene, "subpanel_status", icon=icon, icon_only=True)
            row1.label(text="Mais opções")
            row1 = layout.row()

            if bpy.context.scene.subpanel_status:
                if bpy.context.scene.cena.usuarios != "VENDEDOR":
                    row1.scale_y = 1.5
                    #                row1.prop(rt, "familia", expand=True)
                    #                row1.scale_y = 1.2
                    #            row1.prop(rt, "pedido")
                    #            row1.operator(
                    #                "admin.admin_op", text="Inserir no aplicativo"
                    #            ).action = "INSERT_TABELA_APLICATIVO"
                    row1 = layout.row()
                    #                row1.prop(rt, "projeto_exclusivo")
                    row1 = layout.row()

                    if bpy.context.scene.cena.familia == "4040":
                        row1.prop(
                            bpy.context.scene, "caminho_csv_catalogo", text="Caminho"
                        )
                        row1 = layout.row()
                        row1.prop(
                            context.scene.cena,
                            "ref_csv_rev_lic",
                            text="Sequência Senior",
                            icon="SORTSIZE",
                        )
                        row1 = layout.row()
                        row1.scale_y = 1.8
                        row1.operator(
                            "senior.ferramentas", text="Exportar CSV 4040"
                        ).action = "export_csv_4040"
                    if bpy.context.scene.cena.familia in ["4010", "4030"]:
                        row1.scale_y = 1.8
                        row1.operator(
                            "senior.ferramentas", text="Exportar CSV"
                        ).action = "export_csv"
                if bpy.data.is_saved:
                    layout.operator(
                        "admin.admin_op", text="Inserir no Aplicativo", icon="URL"
                    ).action = "INSERT_TABELA_APLICATIVO"

                # layout.separator()
                # layout.separator()

                # LISTA COLECAO DA CENA
                # ------------------------
                # EXIBIR KITS PF DAS COLEÇÕES
                # ------------------------

                box = layout.box()

                #            layout.label(text="OS ITEMS ABAIXO NÃO POSSUEM KIT PF:")
                row.alert = True

                # lista_objetos = []
                # lista_objetos_ = []
                # row4 = box.row()
                # row4.alert = True

                for col in bpy.data.collections:
                    if (
                        col.hide_viewport == False
                        and col.name_full != "GERAR_VISTAS"
                        and not col.name_full.startswith("SAPATAS")
                    ) and not col.kit_pf.keys() != []:
                        if any(
                            obj.aqua.nome
                            for obj in col.objects
                            if obj.aqua.nome != "" and obj.kit_pf.keys() != []
                        ):
                            pass
                        else:
                            row4 = box.row()
                            row4.scale_y = 1.5
                            row4.alert = True
                            row4.label(text=col.name_full)

        except AttributeError as ATT:
            layout.label(text="SELECIONE UM OBJETO")
            box = layout.box()
            print(ATT)

        return {"FINISHED"}


class MODELOS_OT_substituir_objetos(Operator):
    bl_idname = "modelos.substituir_objetos"
    bl_label = "Substituir Objetos"
    bl_description = (
        "Troca o objeto selecionado pelo objeto em contexto no painel de modelos"
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        pass
        # from pm_funcoes import substituir_objetos

        # # Store frequently accessed data in variables
        # win_man = bpy.data.window_managers["WinMan"]
        # obj = win_man.obj_preview.split(".")[0]
        # category = win_man.obj_category

        # file_path = f"{win_man.caminho_modelo}{category}/{obj}.blend"

        # inner_path = "Collection"

        # substituir_objetos(file_path, obj, file_path.split("/")[-1])

        return {"FINISHED"}


class MODELOS_OT_ferramentas(bpy.types.Operator):
    bl_idname = "modelos.ferramentas"
    bl_label = "Ferramentas de Importar"
    action: bpy.props.EnumProperty(
        items=[
            ("importar_torre", "importar_torre", "importar_torre"),
            ("iniciar", "iniciar", "iniciar"),
            ("ocultar_colecoes", "ocultar_colecoes", "ocultar_colecoes"),
            ("3", "3", "3"),
            ("4", "4", "4"),
        ]
    )

    def execute(self, context):
        if self.action == "importar_torre":
            print("importar_torre")
            importar_torre(self, context)

        if self.action == "iniciar":
            print("")
            print("Playmaker Iniciado!")
            print("")

            # update_nova_referencia(self, context)

            bpy.types.MODELOS_PT_painel_modelos.comecar = True
            obj_category_update(bpy.context.window_manager, "obj_category")
            bpy.context.window_manager.obj_category = "01 - SUBIDAS"

        if self.action == "ocultar_colecoes":
            bpy.context.scene.ocultar = True

        if self.action == "3":
            print("3")

        if self.action == "4":
            print("4")

        return {"FINISHED"}


def LimparAssetMateriais():
    for material in bpy.data.materials:
        material.asset_clear()


def layer_collection(name, _layer_collection=None):
    if _layer_collection is None:
        _layer_collection = bpy.context.view_layer.layer_collection
    if _layer_collection.name == name:
        return _layer_collection
    else:
        for l_col in _layer_collection.children:
            if rez := layer_collection(name=name, _layer_collection=l_col):
                return rez


# CRIAÇAO DA LISTA BASE DE OBJETOS NA CENA
def _old_list():
    col_old_list = []
    obj_old_list = []

    for col in bpy.data.collections:
        col_old_list.append(col)
    for obj in bpy.data.objects:
        obj_old_list.append(obj)

    yield col_old_list
    yield obj_old_list


# APPEND DO OBJETO
def AppendObjeto(caminho_arquivo, nome_arquivo, inner_path="Collection"):
    bpy.ops.wm.append(
        filepath=os.path.join(caminho_arquivo, inner_path, nome_arquivo),
        directory=os.path.join(caminho_arquivo, inner_path),
        filename=nome_arquivo,
    )


# LISTA ATUALIZAD CRIADA
def _cur_list():
    col_cur_list = list(bpy.data.collections)
    obj_cur_list = list(bpy.data.objects)
    yield col_cur_list
    yield obj_cur_list


# LISTA ATUALIZAD CRIADA
def _cur_list():
    col_cur_list = list(bpy.data.collections)
    obj_cur_list = list(bpy.data.objects)
    yield col_cur_list
    yield obj_cur_list


class MODELOS_OT_obj_preview(bpy.types.Operator):
    bl_label = "Import obj_preview"
    bl_idname = "modelos.obj_preview"

    res_obj = ""
    res_col = ""

    def execute(self, context):
        from bpy_plus.collections import Collections

        colecao_parque = []
        for i in os.scandir(os.path.join(f"{caminhos_pastas()[0]}\\CATALOGO")):
            for j in Collections.all():
                if i.name.split(".")[0] == j.name:
                    colecao_parque = i.name.split(".")[0]

        layer_collection(str(colecao_parque), _layer_collection=None)
        col = layer_collection(name=str(colecao_parque))
        if col:
            bpy.context.view_layer.active_layer_collection = col

        # Store frequently accessed data in variables
        win_man = bpy.data.window_managers["WinMan"]
        obj = win_man.obj_preview.split(".")[0]
        category = win_man.obj_category
        file_path = f"{win_man.caminho_modelo}{category}/{obj}"

        # CARREGAR LISTA ANTES DE IMPORTAR
        old_col, old_obj = old_list()

        # ----------------------------------------------------------
        # DEFINE TIPO DE FIXACAO E IMPORTAR OBJETOS
        ancoragem_dict = {
            "TERRA": "TERRA",
            "PISO": "PISO",
        }
        ancoragem = ancoragem_dict.get(obj, "NENHUM")

        if ancoragem in [bpy.context.scene.cena.ancoragem, "NENHUM"]:
            # file_path = f"{win_man.caminho_modelo}{category}/{obj}.blend"
            file_path = os.path.join(win_man.caminho_modelo, category, f"{obj}.blend")
            inner_path = "Collection"

            lista = list(objetos_cena())

            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, obj),
                directory=os.path.join(file_path, inner_path),
                filename=obj,
            )

            # LISTA OBJETOS DEPOIS DE IMPORTAR
            cur_col, cur_obj = cur_list()

            # RESULTADO
            res_col, res_obj = res(old_col, old_obj, cur_col, cur_obj)

            # ASSOCIAR AS PORRAS DOS OBJS IMPORTADOS A PORRA DA LISTA DE RESULTADO
            bpy.types.MODELOS_OT_obj_preview.res_obj = res_obj
            colecao = str(res_col)[1:-1]
            bpy.types.MODELOS_OT_obj_preview.res_col = res_col

            # salvar_dados()
            if bpy.context.scene.cena.usuarios == "VENDEDOR":
                # salvar dados, caso não tenham sido salvos ou atualizar
                # salvar_dados()

                # ajustar area
                bpy.ops.scene.criar_vistas(action="criar_circulacao")

                # ocultar limites
                bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True

            # Check if bpy.context.window_manager.obj_category is not "CATALOGO" or "LICIT"
            if not any(
                bpy.context.window_manager.obj_category.startswith(prefix)
                for prefix in ["CATAL", "LICIT"]
            ):
                filtered_objects = [
                    ob for ob in bpy.context.scene.objects if ob.name_full not in lista
                ]

                for ob in filtered_objects:
                    if ob.show_bounds == True and ob.type != "EMPTY":
                        ob.location.x = random.randint(-3, 3)
                        ob.location.y = random.randint(-3, 3)
                if bpy.context.scene.auto_atualizar == True:
                    pass
                    bpy.ops.object.carregar_dados()

        bpy.ops.scene.recarregar_dados(action="carregar_dados_objeto")

        # LimparAssetMateriais()
        # mudar estado do painel
        # pra alterar visualização dos usuarios
        bpy.types.MODELOS_PT_painel_modelos.comecar = True
        bpy.types.MODELOS_PT_painel_modelos.importar = True
        colecao_cena = bpy.context.view_layer.layer_collection.children.keys()
        catalogo = os.path.join(caminhos_pastas()[0], "catalogo")
        # catalogo = f"{caminhos_pastas()[0]}\\catalogo"
        file_names = [entry.name for entry in os.scandir(catalogo)]
        listagem_catalogo = set(
            os.path.splitext(file_name)[0] for file_name in file_names
        )

        for i in colecao_cena:
            if (i != "GERAR_VISTAS" or i.isdigit()) and i in listagem_catalogo:
                with contextlib.suppress(Exception):
                    bpy.context.scene.cena.modelo = str(i)
                    bpy.context.scene.cena.modelo_item = str(i)
                    bpy.context.scene.cena.nome_vistas = str(i)

                self.report({"INFO"}, f"Modelo: {str(i)} importado!")

        # bpy.ops.scene.recarregar_dados(action="carregar_dados_kit_pf_objeto")

        bpy.ops.object.carregar_cores()

        for obj in bpy.data.objects:
            if obj.name.startswith("ESCORREGADOR M") or obj.name.startswith(
                "ACESSO M1"
            ):
                if obj.hide_viewport == False:
                    obj["TIPO_PE"] = 2

            if (
                obj.name.startswith("PE CARACOL M1 78")
                and obj.name.endswith("PINT")
                and obj.aqua.nome.startswith("PE CARACOL")
            ):
                obj.aqua.nome = "PE CARACOL M1 78CM GALV FOGO"
                obj.aqua.codigo = "2232235010"
                for i in bpy.data.materials:
                    if i.name.startswith("GALVANI"):
                        if i.name.startswith(obj.name):
                            bpy.data.objects[obj.name].active_material = i

            elif (
                obj.name.startswith("PE CARACOL M1 116")
                and obj.name.endswith("PINT")
                and obj.aqua.nome.startswith("PE CARACOL")
            ):
                obj.aqua.nome = "PE CARACOL M1 116 CM GALV FOGO"
                obj.aqua.codigo = "2232235011"
                for i in bpy.data.materials:
                    if i.name.startswith("GALVANI"):
                        if i.name.startswith(obj.name):
                            bpy.data.objects[obj.name].active_material = i

        return {"FINISHED"}


preview_collections = {}
############################
## ANTIGO PM_IMPORTAR_OBJ ##
############################


# OPERADOR PARA AJUSTAR TODAS AS TORRES
class PLAYMAKER_OT_ajustar_colunas(Operator):
    bl_idname = "objects.ajustar_colunas"
    bl_label = "Ajustar Colunas"

    def execute(self, context):
        furos_colunas()
        ajustar_todas_torres()
        return {"FINISHED"}


class MODELOS_PT_painel_modelos_colecoes(Panel):
    bl_label = "MODELOS IMPORTADOS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "MODELOS_PT_painel_modelos"
    bl_order = 0
    bl_category = "CRIAR PARQUES"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        for col in bpy.context.scene.collection.children:
            if (
                col.name_full != "GERAR_VISTAS"
                and bpy.types.MODELOS_PT_painel_modelos.comecar != False
            ):
                box = layout.box()
                row2 = box.row()
                row2.alert = True
                row2.label(text=f"{col.name}")  # .split(".")[0])
                row2.prop(col.aqua, "excluir", toggle=True, icon="CANCEL")
                row2.alert = True


class MODELOS_PT_painel_modelos(Panel):
    bl_label = "MODELOS"
    bl_space_type = "VIEW_3D"
    bl_idname = "MODELOS_PT_painel_modelos"
    bl_region_type = "UI"
    bl_order = 0
    bl_category = "CRIAR PARQUES"
    mostrar = True

    importar = False
    erro = False
    comecar = False
    caminho = ""
    mostrar = True
    # gerar_vistas = False

    @classmethod
    def poll(cls, context):
        return bpy.types.MODELOS_PT_painel_modelos.mostrar != False

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="MOD_LINEART")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        # scene = context.scene
        rt = context.scene.cena
        wm = context.window_manager
        # col = row.column(align=True)

        if bpy.types.MODELOS_PT_painel_modelos.comecar == False:
            row.scale_y = 2
            row.operator(
                "modelos.ferramentas", text="Iniciar AQUA CREATOR", icon="PLAY"
            ).action = "iniciar"
            row = layout.row()
            row.template_icon_view(wm, "obj_preview", scale=0.1, scale_popup=1)
        else:
            if rt.usuarios != "VENDEDOR":
                UI_Modelos(self, context)

            if rt.usuarios == "VENDEDOR":
                UI_vendedor(self, context)


def header_PM(self, context):
    layout = self.layout
    row = layout.row(align=True)
    # Retrieve necessary attributes
    view = context.space_data.shading
    overlay = context.space_data.overlay
    tool_settings = context.tool_settings

    # View shading
    layout.prop(view, "type", text="", expand=True)

    # Overlay toggle & popover
    layout.prop(overlay, "show_overlays", icon="OVERLAY", text="")
    if overlay.show_overlays:
        layout.popover(panel="VIEW3D_PT_overlay", text="")

    # Snap elements
    snap_elements = tool_settings.snap_elements
    if len(snap_elements) == 1:
        for elem in snap_elements:
            icon = (
                bpy.types.ToolSettings.bl_rna.properties["snap_elements"]
                .enum_items[elem]
                .icon
            )
            break
    else:
        icon = "NONE"

    # Snapping
    layout.prop(tool_settings, "use_snap", text="")
    layout.popover(
        panel="VIEW3D_PT_snapping",
        icon=icon,
        text="Mix" if len(snap_elements) > 1 else "",
    )

    row.prop(context.scene.cena, "ancoragem", expand=True)

    row.separator(factor=1)
    row.operator(
        "scene.recarregar_dados", icon="FILE_REFRESH"
    ).action = "carregar_dados_objeto"
    row.operator(
        "admin.admin_op", text="Distribuir Cores", icon="SHADING_RENDERED"
    ).action = "DISTRIBUIR_CORES"
    #        col = box.column(align = True)
    row.operator(
        "scene.recarregar_dados", text="Recarregar KIT PF", icon="FILE_REFRESH"
    ).action = "carregar_dados_kit_pf_objeto"
    row.operator("objects.ajustar_colunas", icon="EMPTY_SINGLE_ARROW")
    # split.scale_y = 1.5
    if bpy.types.MODELOS_PT_painel_modelos.comecar != False:
        row.operator(
            "scene.criar_vistas",
            text="Ajustar Area Circulacao",
            icon="CON_LOCLIMIT",
        ).action = "criar_circulacao"
    row.prop(
        bpy.context.scene,
        "ocultar",
        text="Ocultar Gerar Vistas",
        toggle=True,
        icon="HIDE_OFF",
    )

    if bpy.context.scene.notificacao_banco == True:
        row.label(
            text="SEM CONEXAO COM BANCO DE DADOS. PRECOS PODEM ESTAR DESATUALIZADOS"
        )


classes = (
    MODELOS_PT_painel_modelos,
    MODELOS_OT_ferramentas,
    MODELOS_OT_obj_preview,
    MODELOS_PT_painel_modelos_colecoes,
    MODELOS_OT_substituir_objetos,
    PLAYMAKER_OT_ajustar_colunas,
)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    from bpy.props import EnumProperty, StringProperty
    from bpy.types import WindowManager

    WindowManager.obj_preview_dir = StringProperty(
        name="Folder Path", subtype="DIR_PATH", default=""
    )

    WindowManager.obj_category = EnumProperty(
        name="obj_category",
        items=obj_category_items,
        update=obj_category_update,
        # default="SELECIONE",
    )

    WindowManager.obj_preview = EnumProperty(
        items=obj_preview_items,
        update=obj_preview_update,
    )

    WindowManager.caminho_modelo = StringProperty(
        name="Caminho Modelos", default="", subtype="FILE_PATH"
    )

    import bpy.utils.previews

    pcoll = bpy.utils.previews.new()
    pcoll.obj_preview_dir = ""
    pcoll.obj_preview = ()

    preview_collections["main"] = pcoll

    bpy.types.Scene.subpanel_status = BoolProperty(default=False)
    # bpy.types.Scene.colecoes_importadas = CollectionProperty(
    #     type=PM_PG_colecoes_importadas_ui
    # )
    # bpy.types.Scene.colecoes_importadas_pm_ui_list = IntProperty(
    #     name="indice das colecoes importadas", default=0
    # )
    # AUTO ATUALIZAR AS DERIVACOES
    bpy.types.Scene.auto_atualizar = BoolProperty(
        name="Atualizar Automaticamente", default=True
    )
    bpy.types.Scene.ocultar = BoolProperty(
        name="Ocultar Coleções",
        default=False,
        update=Update_Ocultar_Colecoes,
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    from bpy.types import WindowManager

    del WindowManager.obj_preview

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    # del bpy.types.Scene.colecoes_importadas
    # del bpy.types.Scene.colecoes_importadas_pm_ui_list


if __name__ == "__main__":
    register()
