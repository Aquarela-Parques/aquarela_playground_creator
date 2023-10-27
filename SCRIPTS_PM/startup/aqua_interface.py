import bpy
from bpy.types import Operator
from bpy.utils import unregister_class
from bl_ui.space_view3d import *
from bl_ui.space_toolsystem_common import *
from bl_ui.properties_workspace import *
from bpy.types import Operator, Panel, Menu
from bpy.app.handlers import persistent

# ARMAZENAR PAINEIS ORIGINAIS

from bpy.props import BoolProperty
from bl_ui.space_view3d import VIEW3D_HT_header as HEADER
from bl_ui.space_view3d import VIEW3D_HT_tool_header as TOOL_HEADER
from bl_ui.space_topbar import TOPBAR_HT_upper_bar as TOPBAR

# import blf

self = 0
context = 1

ORIGINAL_HEADER = HEADER.draw
ORIGINAL_TOOL_HEADER = TOOL_HEADER.draw
ORIGINAL_RIGHT_TOPBAR = TOPBAR.draw_right
ORIGINAL_LEFT_TOPBAR = TOPBAR.draw_left


def ui_clean(self, context):
    layout = self.layout
    layout.label(text="")


def top_bar(self, context):
    # self.atualizacao = True
    scn = bpy.context.scene
    layout = self.layout
    # cena = bpy.context.scene.cena
    # if scn.cena.usuarios != "VENDEDOR":
    layout.menu("TOPBAR_MT_file")
    layout.menu("TOPBAR_MT_window")
    #     layout.separator(factor=2)

    # layout.label(text=scn.cena.usuarios, icon="WORKSPACE")
    # layout.label(text=scn.cena.usuarios_pm, icon="COMMUNITY")
    # if (
    #     scn.cena.usuarios == "DESENVOLVEDOR"
    #     or scn.cena.usuarios == "ADMIN"
    #     or scn.cena.usuarios == "PCP"
    #     or scn.cena.funcoes_usuarios == "DESENVOLVEDOR"
    # ):
    #     layout.separator(factor=1)
    #     layout.prop(cena, "usuarios", text="", icon="WORKSPACE")
    #     layout.separator(factor=1)
    #     layout.prop(cena, "funcoes_usuarios", text="", icon="COPY_ID")
    #     layout.separator(factor=1)
    #     layout.prop(cena, "usuarios_pm", text="", icon="COMMUNITY")


def top_bar_right(self, context):
    layout = self.layout
    window = bpy.context.window

    # Active workspace view-layer is retrieved through window, not through workspace.
    layout.operator(
        "wm.url_open", text="Normas Internas", icon="DOCUMENTS"
    ).url = "https://aquarelaparquescombr.sharepoint.com/:b:/s/playmaker2/EWjt3r5FHaxAqR49pVH6nYYB3gEyTk6vifv7wCqmODiLcg?e=FTXd8H"
    # if bpy.context.window.workspace.name != "CATALOGO":
    #     layout.operator(
    #         "fluxo.trocarworkspace", text="Catalogo", icon="ASSET_MANAGER"
    #     ).action = "CATALOGO"
    # if bpy.context.window.workspace.name == "CATALOGO":
    #     layout.operator("fluxo.trocarworkspace", text="Voltar").action = "VOLTAR"
    # # layout.operator(
    # #     "wm.read_homefile", text="Blender", icon="BLENDER"
    # # ).app_template = "Blender"
    layout.operator("outliner.orphans_purge", text="Purge", icon="BRUSH_DATA")
    layout.operator("wm.console_toggle", text="Console", icon="CONSOLE")

    # if bpy.context.scene.cena.usuarios in ["ADMIN", "DESENVOLVEDOR"]:
    #     layout.template_ID(window, "scene", new="scene.new", unlink="scene.delete")


def text_mode_header(self, context):
    layout = self.layout

    st = context.space_data
    text = st.text
    is_syntax_highlight_supported = st.is_syntax_highlight_supported()
    # if bpy.context.scene.cena.usuarios != "VENDEDOR":
    layout.template_header()
    layout.menu("TEXT_MT_templates")
    layout.separator_spacer()

    if text and text.is_modified:
        row = layout.row(align=True)
        row.alert = True
        row.operator("text.resolve_conflict", text="", icon="QUESTION")

    row = layout.row(align=True)
    row.template_ID(st, "text", new="text.new", unlink="text.unlink", open="text.open")

    if text:
        if text.name.endswith((".osl", ".osl")):
            row.operator("node.shader_script_update", text="", icon="FILE_REFRESH")
        else:
            row = layout.row()
            row.active = is_syntax_highlight_supported
            row.operator("text.run_script", text="", icon="PLAY")

    layout.separator_spacer()

    row = layout.row(align=True)
    row.prop(st, "show_line_numbers", text="")
    row.prop(st, "show_word_wrap", text="")

    syntax = row.row(align=True)
    syntax.active = is_syntax_highlight_supported
    syntax.prop(st, "show_syntax_highlight", text="")


def image_mode_header(self, context):
    layout = self.layout

    sima = context.space_data
    overlay = sima.overlay
    ima = sima.image
    iuser = sima.image_user
    tool_settings = context.tool_settings

    show_render = sima.show_render
    show_uvedit = sima.show_uvedit
    show_maskedit = sima.show_maskedit

    if bpy.context.scene.cena.usuarios != "VENDEDOR":
        layout.template_header()

    if ima and ima.is_dirty:
        layout.menu("IMAGE_MT_image", text="Image*")
    else:
        layout.menu("IMAGE_MT_image", text="Image")

    layout.separator_spacer()

    layout.template_ID(sima, "image", new="image.new", open="image.open")

    if show_maskedit:
        row = layout.row()
        row.template_ID(sima, "mask", new="mask.new")

    if not show_render:
        layout.prop(sima, "use_image_pin", text="", emboss=False)

    layout.separator_spacer()


def header_PM(self, context):
    layout = self.layout
    row = layout.row(align=True)

    row.prop(context.scene.cena, "ancoragem", expand=True)

    row.separator(factor=1)
    row = layout.row(align=True)
    row.operator(
        "scene.recarregar_dados", icon="FILE_REFRESH"
    ).action = "carregar_dados_objeto"
    # row.operator(
    #     "admin.admin_op", text="Distribuir Cores", icon="SHADING_RENDERED"
    # ).action = "DISTRIBUIR_CORES"
    row.operator(
        "scene.recarregar_dados", text="Recarregar KIT PF", icon="FILE_REFRESH"
    ).action = "carregar_dados_kit_pf_objeto"
    
    if bpy.types.PLAYMAKER_PT_gerar_vistas.estado == 0:

        row.alert = True    
        row.operator(
            "scene.criar_vistas", text="Ajustar Area Circulacao"
        ).action = "criar_circulacao"

    else:
        row.alert = False
        row.operator(
            "scene.criar_vistas", text="Ajustar Area Circulacao"
        ).action = "criar_circulacao"        
    row.alert = False
    row.operator("objects.ajustar_colunas", icon="EMPTY_SINGLE_ARROW")
    row.separator(factor=1)
    # split.scale_y = 1.5
    # if bpy.types.MODELOS_PT_painel_modelos.comecar != False:
    #     row.operator(
    #         "scene.criar_vistas",
    #         text="Ajustar Area Circulacao",
    #         icon="CON_LOCLIMIT",
    #     ).action = "criar_circulacao"
    # row.prop(
    #     bpy.context.scene,
    #     "ocultar",
    #     text="Ocultar Gerar Vistas",
    #     toggle=True,
    #     icon="HIDE_OFF",
    # )

    # if bpy.context.scene.notificacao_banco == True:
    #     row.label(
    #         text="SEM CONEXAO COM BANCO DE DADOS. PRECOS PODEM ESTAR DESATUALIZADOS"
    #     )
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
    # if bpy.context.scene.notificacao_banco == True:
    #     row.label(
    #         text="SEM CONEXAO COM BANCO DE DADOS. PRECOS PODEM ESTAR DESATUALIZADOS"
    #     )


def tool_header(self, context):
    layout = self.layout
    obj = context.object
    aqua = obj.aqua if hasattr(obj, "aqua") else None
    row = layout.row()

    # Object selection and attributes
    if not bpy.context.selected_objects:
        layout.label(text="Selecione um Objeto")
    else:
        if (
            len(bpy.context.selected_objects) == 1
            and aqua
            and (not aqua.nome == "" or obj.name_full.startswith("GUIA_PLATAFORMA"))
        ):
            if obj.aqua.nome.startswith(f"COLUNA {bpy.context.scene.cena.ancoragem}"):
                if obj.aqua.nome.startswith(
                    f"COLUNA {bpy.context.scene.cena.ancoragem}"
                ) or obj.aqua.nome.startswith(f"COLUNA MAD PLAST"):
                    layout.prop(obj, '["COLUNA_CUSTOM"]')
                if obj["COLUNA_CUSTOM"] == 1:
                    layout.prop(aqua, "derivacao", text="DER")
            else:
                layout.prop(aqua, "derivacao", text="DER")

            if obj.aqua.fixo:
                layout.label(text=f"Altura Fixa em {round(obj.location.z, 2)} Mts")

            if obj.aqua.derivacao == "99_colorida":
                layout.prop(aqua, "cor_personalizada", text="Personalizar")
                if obj.aqua.cor_personalizada:
                    layout.prop(obj, "color", text="")

            # COR PEÇAS METALICAS ("226")
            if (
                obj.aqua.codigo.startswith("226") == True
                or obj.aqua.codigo.startswith("300")
            ) and not obj.aqua.nome.startswith("TUNEL"):
                layout.label(text="          ")
                layout.prop(obj.aqua, "cor_metal_personalizada")

            if obj.aqua.cor_metal_personalizada == True:
                layout.prop(obj.aqua, "cor_metal", text="")
                layout.label(text="CONSULTE DISPONILIDADE")

            # layout.separator(factor=3)
            layout.prop(aqua, "altura", text="Altura")
            layout.label(text=aqua.nome)
            layout.label(text=str(aqua.codigo))
            layout.label(text=f"{aqua.peso} kg")  # TODO: PESO DIRETO DA SENIOR

            if obj.show_bounds and not bpy.types.MODELOS_PT_painel_modelos.erro:
                layout.separator()
                row = layout.row()
                # row.label(text="Ligar")
                row.prop_search(aqua, "alvo", context.scene, "objects", text="")

            if obj.aqua.alvo:
                row = layout.row()
                # row.scale_y = 1
                row.alert = True

                if obj.name_full == obj.aqua.alvo.name_full:
                    row.operator(
                        "object.conectar",
                        text="ERRO! OBJETO NAO PODE CONECTAR A ELE MESMO",
                        icon="ERROR",
                    ).action = "CONFLITO"

                if (
                    round(obj.location.z, 2) != round(obj.aqua.alvo.location.z, 2)
                    and obj.aqua.fixo
                ):
                    row.operator(
                        "object.conectar", text="ERRO! ALTURA INCOPATIVEL", icon="ERROR"
                    ).action = "CONFLITO"

            if obj.show_bounds or obj.name_full.startswith("GUIA_PLATAFORMA"):
                layout.operator("object.girar_90", icon="ORIENTATION_GIMBAL")

                props = [
                    "AQUA_INVERTER",
                    "AQUA_VOLVER",
                    "AQUA_DUPLO",
                    "AQUA_ACOP",
                    "AQUA_L",
                    "TIPO_PE",
                    "AQUA_INCLINAR",
                    "AQUA_ALTURA",
                ]
                for prop in obj.keys():
                    if prop in props:
                        row = layout.row()
                        row.prop(obj, '["' + prop + '"]')

            if obj.aqua.alvo and obj.constraints:
                layout.separator()
                row = layout.row(heading="Eixo", align=True)
                row.prop(
                    obj.constraints["Copy Location"], "use_x", text="X", toggle=True
                )
                row.prop(
                    obj.constraints["Copy Location"], "use_y", text="Y", toggle=True
                )
                row.prop(
                    obj.constraints["Copy Location"], "use_z", text="Z", toggle=True
                )


# BOTAO


def change_header(self, context):
    if not self.change_header:
        bpy.types.VIEW3D_HT_header.draw = ui_clean
        bpy.types.VIEW3D_HT_tool_header.draw = ui_clean
        bpy.types.TEXT_HT_header.draw = ui_clean
        bpy.types.IMAGE_HT_header.draw = ui_clean

        bpy.types.TOPBAR_HT_upper_bar.draw_right = top_bar_right
        bpy.types.VIEW3D_HT_tool_header.draw = tool_header
        bpy.types.TOPBAR_HT_upper_bar.draw_left = top_bar
        bpy.types.TEXT_HT_header.draw = text_mode_header
        bpy.types.IMAGE_HT_header.draw = image_mode_header
        bpy.types.VIEW3D_HT_header.draw = header_PM
    else:
        bpy.types.VIEW3D_HT_header.draw = ORIGINAL_HEADER
        bpy.types.VIEW3D_HT_tool_header.draw = ORIGINAL_TOOL_HEADER
        bpy.types.TOPBAR_HT_upper_bar.draw_right = ORIGINAL_RIGHT_TOPBAR
        bpy.types.TOPBAR_HT_upper_bar.draw_left = ORIGINAL_LEFT_TOPBAR


bpy.types.WindowManager.change_header = BoolProperty(update=change_header)


def clear_interface():
    gpclasses = [
        c
        for c in dir(bpy.types)
        if c.startswith("VIEW3D_PT_collections")
        or c.startswith("VIEW3D_PT_view3d_lock")
        or c.startswith("VIEW3D_PT_view3d_cursor")
        or c.startswith("VIEW3D_PT_transform_orientations")
        or c.startswith("WORKSPACE_PT_main")
        or c.startswith("WORKSPACE_PT_custom_props")
        or c.startswith("WORKSPACE_PT_addons")
        or c.startswith("VIEW3D_PT_tools_object_options")
        or c.startswith("VIEW3D_PT_active_tool")
        or c.startswith("VIEW3D_PT_tools_meshedit_options")
        or c.startswith("VIEW3D_PT_grease_pencil")
        or c.startswith("VIEW3D_PT_context_properties")
        or c.startswith("VIEW3D_PT_view3d_properties")
        or c.startswith("CURVE_PT_assign_shape_keys")
    ]

    for c in gpclasses:
        cls = getattr(bpy.types, c)
        unregister_class(cls)


def EsconderPaineis():
    bpy.ops.object.hide_panels()


# HIDE_OT_panels
class Hide_Panels(Operator):
    bl_idname = "object.hide_panels"
    bl_label = "Hide Panels"

    def execute(self, context):
        bpy.data.window_managers["WinMan"].change_header = False
        clear_interface()

        return {"FINISHED"}


classes = (Hide_Panels,)


@persistent
def post_init_handler(dummy):
    bpy.data.window_managers["WinMan"].change_header = False
    clear_interface()
    print("@Paineis_Originais_Escondidos")


def register():
    from bpy.utils import register_class

    bpy.app.handlers.load_post.append(post_init_handler)

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
