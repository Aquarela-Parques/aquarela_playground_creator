import contextlib
import os
import random

import bpy
from bpy.app.handlers import persistent
from bpy.props import CollectionProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import Header, Menu, Operator, Panel, PropertyGroup, UIList

# from pm_criar_parques import panel_poll_is_upper_region
# from pm_funcoes import caminhos_pastas, salvar_dados
# from pm_importar_modelos import cur_list, layer_collection, objetos_cena, old_list, res


class FileBrowserPanel:
    bl_space_type = "FILE_BROWSER"

    @classmethod
    def poll(cls, context):
        space_data = context.space_data

        # can be None when save/reload with a file selector open
        if space_data.params is None:
            return False

        return (
            space_data
            and space_data.type == "FILE_BROWSER"
            and space_data.browse_mode == "FILES"
        )


def panel_poll_is_upper_region(region):
    # The upper region is left-aligned, the lower is split into it then.
    # Note that after "Flip Regions" it's right-aligned.
    return region.alignment in {"LEFT", "RIGHT"}


def panel_poll_is_asset_browsing(context):
    from bpy_extras.asset_utils import SpaceAssetInfo

    return SpaceAssetInfo.is_asset_browser_poll(context)


# class IMPORTADOR_OT_funcoes_importador(Operator):
#     bl_idname = "importador.funcoes"
#     bl_label = "Funcoes do Importador"
#     bl_options = {"REGISTER", "UNDO"}

#     funcao: EnumProperty(
#         items=[
#             ("atualizar_tag_parque", "atualizar_tag_parque", "atualizar_tag_parque"),
#         ]
#     )

#     def execute(self, context):
#         if self.funcao == "atualizar_tag_parque":
#             self.atualizar_tag_parque(context=context, self=self)
#         return {"FINISHED"}

#     # @staticmethod
#     # def atualizar_tag_parque(self, context):
#     #     bpy.context.scene.tags_parques.clear()
#     #     for area in screen.areas:
#     #         if area.type == "FILE_BROWSER":
#     #             params = area.spaces[0].params
#     #             singleFileName = params.filename
#     #             filename = singleFileName.split(".")[0]
#     #             with os.scandir(caminhos_pastas()[0]) as scan_modelos:
#     #                 for tag in scan_modelos:
#     #                     if tag.is_file() and tag.name.split(".")[0] == filename:
#     #                         #                            print(tag.path)
#     #                         with open(tag.path, "r") as leitura_tag:
#     #                             for i in leitura_tag:
#     #                                 bpy.context.scene.tags_parques.add().tags = i.split(
#     #                                     "\n"
#     #                                 )[0]


def ImportadorFileBrowser(self, context, _event):
    screen = bpy.context.window.screen
    for area in screen.areas:  # PASSA POR TODAS AS AREAS
        # from bpy_plus.collections import Collections

        if area.type == "FILE_BROWSER":
            colecao_parque = []
            params = area.spaces[0].params
            singleFileName = params.filename
            singleDirectory = params.directory
            inner_path = "Collection"
            dir_base_selec = str(singleDirectory).split("'")[1]
            caminho_arquivo_selecionado = os.path.join(dir_base_selec, singleFileName)
            nome_arquivo_selecionado = os.path.splitext(
                os.path.basename(caminho_arquivo_selecionado)
            )[0]

            bpy.ops.wm.append(
                filepath=os.path.join(
                    caminho_arquivo_selecionado,
                    inner_path,
                    nome_arquivo_selecionado,
                ),
                directory=os.path.join(caminho_arquivo_selecionado, inner_path),
                filename=nome_arquivo_selecionado,
            )

            # for i in os.scandir(os.path.join(f"{caminhos_pastas()[0]}\\CATALOGO")):
            #     for j in Collections.all():
            #         if i.name.split(".")[0] == j.name:
            #             colecao_parque = i.name.split(".")[0]

            # layer_collection(str(colecao_parque), _layer_collection=None)
            # col = layer_collection(name=str(colecao_parque))
            # if col:
            #     bpy.context.view_layer.active_layer_collection = col

            # # CARREGAR LISTA ANTES DE IMPORTAR
            # old_col, old_obj = old_list()

            # obj = nome_arquivo_selecionado

            # ----------------------------------------------------------
            # DEFINE TIPO DE FIXACAO E IMPORTAR OBJETOS
            # ancoragem_dict = {
            #     "TERRA": "TERRA",
            #     "PISO": "PISO",
            # }
            # ancoragem = ancoragem_dict.get(obj, "NENHUM")

            # if ancoragem in [bpy.context.scene.cena.ancoragem, "NENHUM"]:
            #     inner_path = "Collection"

            # lista = list(objetos_cena())

            # bpy.ops.wm.append(
            #     filepath=os.path.join(
            #         caminho_arquivo_selecionado,
            #         inner_path,
            #         nome_arquivo_selecionado,
            #     ),
            #     directory=os.path.join(caminho_arquivo_selecionado, inner_path),
            #     filename=nome_arquivo_selecionado,
            # )

            # # LISTA OBJETOS DEPOIS DE IMPORTAR
            # cur_col, cur_obj = cur_list()

            # # RESULTADO
            # res_col, res_obj = res(old_col, old_obj, cur_col, cur_obj)

            # # ASSOCIAR AS PORRAS DOS OBJS IMPORTADOS A PORRA DA LISTA DE RESULTADO
            # bpy.types.MODELOS_OT_obj_preview.res_obj = res_obj
            # colecao = str(res_col)[1:-1]
            # bpy.types.MODELOS_OT_obj_preview.res_col = res_col

            # # salvar_dados()
            # if bpy.context.scene.cena.usuarios == "VENDEDOR":
            #     # salvar dados, caso não tenham sido salvos ou atualizar
            #     salvar_dados()

            #     # ajustar area
            #     bpy.ops.scene.criar_vistas(action="criar_circulacao")

            #     # ocultar limites
            #     bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True

            # # Check if bpy.context.window_manager.obj_category is not "CATALOGO" or "LICIT"
            # if not any(
            #     bpy.context.window_manager.obj_category.startswith(prefix)
            #     for prefix in ["CATAL", "LICIT"]
            # ):
            #     filtered_objects = [
            #         ob
            #         for ob in bpy.context.scene.objects
            #         if ob.name_full not in lista
            #     ]

            #     for ob in filtered_objects:
            #         if ob.show_bounds == True and ob.type != "EMPTY":
            #             ob.location.x = random.randint(-3, 3)
            #             ob.location.y = random.randint(-3, 3)
            #     if bpy.context.scene.auto_atualizar == True:
            #         bpy.ops.object.carregar_dados()

            # LimparAssetMateriais()
            # mudar estado do painel
            # pra alterar visualização dos usuarios
            # bpy.types.MODELOS_PT_painel_modelos.comecar = True
            # bpy.types.MODELOS_PT_painel_modelos.importar = True

            # colecao_cena = bpy.context.view_layer.layer_collection.children.keys()

            # catalogo = f"{caminhos_pastas()[0]}\\catalogo"

            # file_names = [entry.name for entry in os.scandir(catalogo)]

            # listagem_catalogo = set(
            #     os.path.splitext(file_name)[0] for file_name in file_names
            # )

            # for i in colecao_cena:
            #     if (i != "GERAR_VISTAS" or i.isdigit()) and i in listagem_catalogo:
            #         with contextlib.suppress(Exception):
            #             bpy.context.scene.cena.modelo = str(i)
            #             bpy.context.scene.cena.modelo_item = str(i)
            #             bpy.context.scene.cena.nome_vistas = str(i)

            #         self.report({"INFO"}, f"Modelo: {str(i)} importado!")

            # bpy.ops.scene.recarregar_dados(action="carregar_dados_kit_pf_objeto")
            # bpy.ops.scene.recarregar_dados(action="carregar_dados_objeto")
            # bpy.ops.object.carregar_cores()

            # for obj in bpy.data.objects:
            #     if obj.name.startswith("ESCORREGADOR M") or obj.name.startswith(
            #         "ACESSO M1"
            #     ):
            #         if obj.hide_viewport == False:
            #             obj["TIPO_PE"] = 2

            #     if (
            #         obj.name.startswith("PE CARACOL M1 78")
            #         and obj.name.endswith("PINT")
            #         and obj.aqua.nome.startswith("PE CARACOL")
            #     ):
            #         obj.aqua.nome = "PE CARACOL M1 78CM GALV FOGO"
            #         obj.aqua.codigo = "2232235010"
            #         for i in bpy.data.materials:
            #             if i.name.startswith("GALVANI"):
            #                 if i.name.startswith(obj.name):
            #                     bpy.data.objects[obj.name].active_material = i

            #     elif (
            #         obj.name.startswith("PE CARACOL M1 116")
            #         and obj.name.endswith("PINT")
            #         and obj.aqua.nome.startswith("PE CARACOL")
            #     ):
            #         obj.aqua.nome = "PE CARACOL M1 116 CM GALV FOGO"
            #         obj.aqua.codigo = "2232235011"
            #         for i in bpy.data.materials:
            #             if i.name.startswith("GALVANI"):
            #                 if i.name.startswith(obj.name):
            #                     bpy.data.objects[obj.name].active_material = i

    return {"FINISHED"}


# class IMPORTADOR_PG_propriedaes(PropertyGroup):
#     """PROPRIEDADES USUADAS DA UI LIST DE USUARIOS"""

#     nomes_categorias: StringProperty(
#         name="Categorias",
#         description="Nome das Categorias",
#         default="",
#     )

#     tags: StringProperty(
#         name="Tags",
#         description="Composição do parque",
#         default="",
#     )


# class IMPORTADOR_UL_uilist(UIList):
#     """UI LIST contendo os items dos catalogos"""

#     def draw_item(
#         self, context, layout, data, item, icon, active_data, active_propname, index
#     ):
#         # We could write some code to decide which icon to use here...
#         custom_icon = "COMMUNITY"

#         # Make sure your code supports all 3 layout types
#         if self.layout_type in {"DEFAULT", "COMPACT"}:
#             layout.label(text=item.nomes_categorias, icon=custom_icon)

#         elif self.layout_type in {"GRID"}:
#             layout.alignment = "CENTER"
#             layout.label(text="", icon=custom_icon)


# class IMPORTADOR_UL_tagsparqes(UIList):
#     """UI LIST contendo os items dos catalogos"""

#     def draw_item(
#         self, context, layout, data, item, icon, active_data, active_propname, index
#     ):
#         # We could write some code to decide which icon to use here...
#         custom_icon = "TRIA_RIGHT"

#         # Make sure your code supports all 3 layout types
#         if self.layout_type in {"DEFAULT", "COMPACT"}:
#             layout.label(text=item.tags, icon=custom_icon)

#         elif self.layout_type in {"GRID"}:
#             layout.alignment = "CENTER"
#             layout.label(text="", icon=custom_icon)


# def AdicionarCategorias():
#     modelos = caminhos_pastas()[0]

#     with os.scandir(modelos) as modelos_scan:
#         for i in modelos_scan:
#             if i.is_dir():
#                 bpy.context.scene.categorias_pm.add().nomes_categorias = i.name
#         return {"FINISHED"}

for area in bpy.context.window.screen.areas:
    if area.type == "FILE_BROWSER":
        area.spaces.active.params.use_filter = True
        area.spaces.active.params.use_filter_blender = True

# bpy.context.scene.tags_parques.clear()
# bpy.context.scene.categorias_pm.clear()
# AdicionarCategorias()


# def TrocarCategoria(self, context):
#     screen = bpy.context.window.screen
#     for area in screen.areas:
#         if area.type == "FILE_BROWSER":
#             area.spaces.active.params.directory = f"{caminhos_pastas()[0]}\\{bpy.context.scene.categorias_pm[bpy.context.scene.categorias_pm_index].nomes_categorias}".encode()
#             area.spaces.active.params.use_filter = True


# bpy.context.scene.categorias_pm.clear()
# AdicionarCategorias()


# class IMPORTADOR_PT_menu_categorias(Panel):
#     bl_space_type = "FILE_BROWSER"
#     bl_region_type = "TOOLS"
#     bl_category = "CATEGORIAS"
#     bl_label = "Categorias"

#     #    @classmethod
#     #    def poll(cls, context):
#     #        if len(context.area.spaces) > 1:
#     #            return False
#     #        return not context.preferences.filepaths.hide_recent_locations and panel_poll_is_upper_region(context.region)

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         row = layout.row()
#         row.scale_y = 1.5
#         rt = context.scene.cena
#         wm = context.window_manager

#         if bpy.types.MODELOS_PT_painel_modelos.comecar == False:
#             row.scale_y = 2
#             row.operator(
#                 "modelos.ferramentas", text="Iniciar Playmaker", icon="PLAY"
#             ).action = "iniciar"
#             row = layout.row()
#         else:
#             if rt.usuarios == "VENDEDOR":
#                 pass

#             if rt.usuarios != "VENDEDOR":
#                 row.operator(
#                     "modelos.ferramentas", text="ADICIONAR TORRE", icon="SNAP_VERTEX"
#                 ).action = "importar_torre"

#                 row = layout.row()
#                 row.template_list(
#                     "IMPORTADOR_UL_uilist",
#                     "Categorias_PM",
#                     scene,
#                     "categorias_pm",
#                     scene,
#                     "categorias_pm_index",
#                 )
#                 row = layout.row()
#                 row.separator(factor=2)
#                 row = layout.row()
#                 row.label(text="COMPOSIÇÃO DO MODELO")
#                 row.operator(
#                     "importador.funcoes", text="LISTAR", icon="ALIGN_LEFT"
#                 ).funcao = "atualizar_tag_parque"
#                 row = layout.row()
#                 row.template_list(
#                     "IMPORTADOR_UL_tagsparqes",
#                     "Tags_PM",
#                     scene,
#                     "tags_parques",
#                     scene,
#                     "tags_pm_index",
#                 )


# class FileBrowserPanel:
#     bl_space_type = "FILE_BROWSER"

#     @classmethod
#     def poll(cls, context):
#         space_data = context.space_data

#         # can be None when save/reload with a file selector open
#         if space_data.params is None:
#             return False

#         return (
#             space_data
#             and space_data.type == "FILE_BROWSER"
#             and space_data.browse_mode == "FILES"
#         )


# class FileBrowserMenu:
#     @classmethod
#     def poll(cls, context):
#         space_data = context.space_data
#         return (
#             space_data
#             and space_data.type == "FILE_BROWSER"
#             and space_data.browse_mode == "FILES"
#         )


# class FILEBROWSER_PT_bookmarks_recents(Panel):
#     bl_space_type = "FILE_BROWSER"
#     bl_region_type = "TOOLS"
#     bl_category = "Bookmarks"
#     bl_label = "Recent"

#     @classmethod
#     def poll(cls, context):
#         if len(context.area.spaces) > 1:
#             return False
#         return (
#             not context.preferences.filepaths.hide_recent_locations
#             and panel_poll_is_upper_region(context.region)
#         )

#     def draw(self, context):
#         layout = self.layout
#         space = context.space_data

#         if space.recent_folders:
#             row = layout.row()
#             row.template_list(
#                 "FILEBROWSER_UL_dir",
#                 "recent_folders",
#                 space,
#                 "recent_folders",
#                 space,
#                 "recent_folders_active",
#                 item_dyntip_propname="path",
#                 rows=1,
#                 maxrows=10,
#             )
#             col = row.column(align=True)
#             col.operator("file.reset_recent", icon="X", text="")


# class FILEBROWSER_PT_bookmarks_favorites(FileBrowserPanel, Panel):
#     bl_space_type = "FILE_BROWSER"
#     bl_region_type = "TOOLS"
#     bl_category = "Bookmarks"
#     bl_label = "Bookmarks"

#     @classmethod
#     def poll(cls, context):
#         if len(context.area.spaces) > 1:
#             return False
#         return (
#             not context.preferences.filepaths.hide_recent_locations
#             and panel_poll_is_upper_region(context.region)
#         )

#     def draw(self, context):
#         layout = self.layout
#         space = context.space_data

#         if space.bookmarks:
#             row = layout.row()
#             num_rows = len(space.bookmarks)
#             row.template_list(
#                 "FILEBROWSER_UL_dir",
#                 "bookmarks",
#                 space,
#                 "bookmarks",
#                 space,
#                 "bookmarks_active",
#                 item_dyntip_propname="path",
#                 rows=(2 if num_rows < 2 else 4),
#                 maxrows=10,
#             )

#             col = row.column(align=True)
#             col.operator("file.bookmark_add", icon="ADD", text="")
#             col.operator("file.bookmark_delete", icon="REMOVE", text="")
#             col.menu(
#                 "FILEBROWSER_MT_bookmarks_context_menu", icon="DOWNARROW_HLT", text=""
#             )

#             if num_rows > 1:
#                 col.separator()
#                 col.operator(
#                     "file.bookmark_move", icon="TRIA_UP", text=""
#                 ).direction = "UP"
#                 col.operator(
#                     "file.bookmark_move", icon="TRIA_DOWN", text=""
#                 ).direction = "DOWN"
#         else:
#             layout.operator("file.bookmark_add", icon="ADD")


# class FILEBROWSER_PT_bookmarks_system(Panel):
#     bl_space_type = "FILE_BROWSER"
#     bl_region_type = "TOOLS"
#     bl_category = "Bookmarks"
#     bl_label = "System"

#     @classmethod
#     def poll(cls, context):
#         if len(context.area.spaces) > 1:
#             return False
#         return (
#             not context.preferences.filepaths.hide_recent_locations
#             and panel_poll_is_upper_region(context.region)
#         )

#     def draw(self, context):
#         layout = self.layout
#         space = context.space_data

#         if space.system_bookmarks:
#             row = layout.row()
#             row.template_list(
#                 "FILEBROWSER_UL_dir",
#                 "system_bookmarks",
#                 space,
#                 "system_bookmarks",
#                 space,
#                 "system_bookmarks_active",
#                 item_dyntip_propname="path",
#                 rows=1,
#                 maxrows=10,
#             )


# class FILEBROWSER_PT_bookmarks_volumes(Panel):
#     bl_space_type = "FILE_BROWSER"
#     bl_region_type = "TOOLS"
#     bl_category = "Bookmarks"
#     bl_label = "Volumes"

#     @classmethod
#     def poll(cls, context):
#         if len(context.area.spaces) > 1:
#             return False
#         return (
#             not context.preferences.filepaths.hide_recent_locations
#             and panel_poll_is_upper_region(context.region)
#         )

#     def draw(self, context):
#         layout = self.layout
#         space = context.space_data

#         if space.system_folders:
#             row = layout.row()
#             row.template_list(
#                 "FILEBROWSER_UL_dir",
#                 "system_folders",
#                 space,
#                 "system_folders",
#                 space,
#                 "system_folders_active",
#                 item_dyntip_propname="path",
#                 rows=1,
#                 maxrows=10,
#             )


# class FILEBROWSER_PT_directory_path(Panel):
#     bl_space_type = "FILE_BROWSER"
#     bl_region_type = "UI"
#     bl_label = "Directory Path"
#     bl_category = "Attributes"
#     bl_options = {"HIDE_HEADER"}

#     def is_header_visible(self, context):
#         for region in context.area.regions:
#             if region.type == "HEADER" and region.height <= 1:
#                 return False

#         return True

#     # @classmethod
#     # def poll(cls, context):
#     #     if len(context.area.spaces) > 1:
#     #         return False
#     #     return (
#     #         not context.preferences.filepaths.hide_recent_locations
#     #         and panel_poll_is_upper_region(context.region)
#     #     )

#     def draw(self, context):
#         layout = self.layout
#         space = context.space_data
#         params = space.params

#         layout.scale_x = 1.3
#         layout.scale_y = 1.3

#         row = layout.row()
#         flow = row.grid_flow(
#             row_major=True, columns=0, even_columns=False, even_rows=False, align=False
#         )

#         subrow = flow.row()

#         subsubrow = subrow.row(align=True)
#         subsubrow.operator("file.previous", text="", icon="BACK")
#         subsubrow.operator("file.next", text="", icon="FORWARD")
#         subsubrow.operator("file.parent", text="", icon="FILE_PARENT")
#         subsubrow.operator("file.refresh", text="", icon="FILE_REFRESH")

#         subsubrow = subrow.row()
#         #        subsubrow.operator_context = 'EXEC_DEFAULT'
#         #        subsubrow.operator("file.directory_new", icon='NEWFOLDER', text="")

#         subrow.template_file_select_path(params)

#         subrow = flow.row()

#         #        subsubrow = subrow.row()
#         subsubrow.scale_x = 1
#         subsubrow.prop(params, "filter_search", text="", icon="VIEWZOOM")

#         subsubrow = subrow.row(align=True)
#         subsubrow.prop(params, "display_type", expand=True, icon_only=True)
#         subsubrow.popover("FILEBROWSER_PT_display", text="")

#         subsubrow = subrow.row(align=True)
#         subsubrow.prop(params, "use_filter", toggle=True, icon="FILTER", icon_only=True)
#         subsubrow.popover("FILEBROWSER_PT_filter", text="")

#         if space.active_operator:
#             subrow.operator(
#                 "screen.region_toggle",
#                 text="",
#                 icon="PREFERENCES",
#                 depress=is_option_region_visible(context, space),
#             ).region_type = "TOOL_PROPS"


# screen = bpy.context.window.screen
# for area in screen.areas: # CONTROLA O CAMINHO DO FILEBROWSER
#    if area.type == 'FILE_BROWSER':
#        area.spaces.active.params.directory = b"C:\Users\Aquarela\\"


# def ExibirTags():
#     for area in screen.areas:
#         if area.type == "FILE_BROWSER":
#             params = area.spaces[0].params
#             singleFileName = params.filename
#             filename = singleFileName.split(".")[0]
#             area.spaces.active.params.directory = f"{caminhos_pastas()[0]}\\{bpy.context.scene.categorias_pm[bpy.context.scene.categorias_pm_index].nomes_categorias}".encode()
#             area.spaces.active.params.use_filter = True

#             with os.scandir(caminhos_pastas()[0]) as scan_modelos:
#                 for tag in scan_modelos:
#                     if tag.is_file() and tag.name.split(".")[0] == filename:
#                         with open(tag.path, "r") as leitura_tag:
#                             tag_conteudo = leitura_tag.read()
#                             return tag_conteudo


def scan_filebrowser():
    for area in bpy.context.window.screen.areas:  # PASSA POR TODAS AS AREAS
        if area.type == "FILE_BROWSER":
            params = area.spaces[0].params
            singleFileName = params.filename
            retorno_modelo = f"Nome do Modelo: {singleFileName.split('.')[0]}"
            return retorno_modelo


# class FILEBROWSER_MT_editor_menus(FileBrowserMenu, Menu):
#     bl_idname = "FILEBROWSER_MT_editor_menus"
#     bl_label = ""

#     @classmethod
#     def poll(cls, context):
#         if len(context.area.spaces) > 1:
#             return False
#         return (
#             not context.preferences.filepaths.hide_recent_locations
#             and panel_poll_is_upper_region(context.region)
#         )

#     def draw(self, _context):
#         layout = self.layout
#         layout.label(text=scan_filebrowser())


#        layout.menu("FILEBROWSER_MT_view")
#        layout.menu("FILEBROWSER_MT_select")


# class FILEBROWSER_HT_header(Header):
#     bl_space_type = "FILE_BROWSER"

#     def draw_asset_browser_buttons(self, context):
#         layout = self.layout

#         space_data = context.space_data
#         params = space_data.params

#         layout.separator_spacer()

#         if params.asset_library_ref != "LOCAL":
#             layout.prop(params, "import_type", text="")

#         layout.separator_spacer()

#         # Uses prop_with_popover() as popover() only adds the triangle icon in headers.
#         layout.prop_with_popover(
#             params,
#             "display_type",
#             panel="ASSETBROWSER_PT_display",
#             text="",
#             icon_only=True,
#         )

#         sub = layout.row()
#         sub.ui_units_x = 8
#         sub.prop(params, "filter_search", text="", icon="VIEWZOOM")

#         layout.popover(panel="ASSETBROWSER_PT_filter", text="", icon="FILTER")

#         layout.operator(
#             "screen.region_toggle",
#             text="",
#             icon="PREFERENCES",
#             depress=is_option_region_visible(context, space_data),
#         ).region_type = "TOOL_PROPS"

#     def draw(self, context):
#         from bpy_extras.asset_utils import SpaceAssetInfo

#         layout = self.layout

#         space_data = context.space_data

#         if SpaceAssetInfo.is_asset_browser(space_data):
#             ASSETBROWSER_MT_editor_menus.draw_collapsible(context, layout)
#             layout.separator()
#             self.draw_asset_browser_buttons(context)
#         else:
#             FILEBROWSER_MT_editor_menus.draw_collapsible(context, layout)
#             layout.separator_spacer()

#         if not context.screen.show_statusbar:
#             layout.template_running_jobs()


classes = (
    # IMPORTADOR_PG_propriedaes,
    # IMPORTADOR_UL_uilist,
    # IMPORTADOR_UL_tagsparqes,
    # IMPORTADOR_PT_menu_categorias,
    # FILEBROWSER_PT_bookmarks_recents,
    # FILEBROWSER_PT_bookmarks_favorites,
    # FILEBROWSER_PT_bookmarks_system,
    # FILEBROWSER_PT_bookmarks_volumes,
    # FILEBROWSER_PT_directory_path,
    # FILEBROWSER_MT_editor_menus,
    # IMPORTADOR_OT_funcoes_importador,
    # FILEBROWSER_HT_header,
)


@persistent
def ApontarNovoDrag(dummy):
    bpy.context.scene.auto_atualizar = True
    bpy.types.WM_OT_drop_blend_file.invoke = ImportadorFileBrowser


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.app.handlers.load_post.append(ApontarNovoDrag)

    # bpy.types.Scene.categorias_pm = CollectionProperty(type=IMPORTADOR_PG_propriedaes)
    # bpy.types.Scene.tags_parques = CollectionProperty(type=IMPORTADOR_PG_propriedaes)
    # bpy.types.Scene.categorias_pm_index = IntProperty(
    #     name="indiceDasCategorias", default=0, update=TrocarCategoria
    # )
    # bpy.types.Scene.tags_pm_index = IntProperty(name="IndicedasTags", default=0)


def unregister():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    del bpy.types.Scene.categorias_pm
    del bpy.types.Scene.categorias_pm_index

    del bpy.types.Scene.tags_parques
    del bpy.types.Scene.tags_pm_index


if __name__ == "__main__":
    register()
