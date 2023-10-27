import bpy
import contextlib
from bpy.types import Panel


class ADMIN_PT_area_custom_1(Panel):
    bl_label = "PM: AREA CUSTOM"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FERRAMENTAS"
    mostrar = True

    @classmethod
    def poll(cls, context):
        return bpy.context.selected_objects != []

    def draw_header(self, context):
        self.layout.label(text="", icon="SURFACE_NCIRCLE")

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object

        with contextlib.suppress(AttributeError):
            if obj.name_full.startswith("PM_AREA_CUSTOM"):
                layout.prop(obj.data, '["Dim X"]')
                layout.prop(obj.data, '["Dim Y"]')
                layout.prop(obj.data, '["Formato"]')
            else:
                layout.label(text="Nenhum Piso Selecionado")


class ADMIN_PT_medir_produto(Panel):
    bl_label = "PM: MEDIR PRODUTO"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FERRAMENTAS"
    mostrar = True

    @classmethod
    def poll(cls, context):
        return bpy.context.object != False

    def draw_header(self, context):
        self.layout.label(text="", icon="ORIENTATION_GLOBAL")

    def draw(self, context):
        layout = self.layout

        un = ""
        with contextlib.suppress(AttributeError):
            if bpy.context.scene.unit_settings.length_unit == "CENTIMETERS":
                x_largura = round(bpy.context.object.dimensions.x * 100, 2)
                y_largura = round(bpy.context.object.dimensions.y * 100, 2)
                z_largura = round(bpy.context.object.dimensions.z * 100, 2)
                un = "cm"
            elif bpy.context.scene.unit_settings.length_unit == "METERS":
                x_largura = round(bpy.context.object.dimensions.x, 2)
                y_largura = round(bpy.context.object.dimensions.y, 2)
                z_largura = round(bpy.context.object.dimensions.z, 2)
                un = "m"
            elif bpy.context.scene.unit_settings.length_unit == "MILLIMETERS":
                x_largura = round(bpy.context.object.dimensions.x * 1000, 2)
                y_largura = round(bpy.context.object.dimensions.y * 1000, 2)
                z_largura = round(bpy.context.object.dimensions.z * 1000, 2)
                un = "mm"

            layout.prop(context.scene.unit_settings, "length_unit", text="Unidade")

            if bpy.context.scene.unit_settings.length_unit in [
                "METERS",
                "CENTIMETERS",
                "MILLIMETERS",
            ]:
                box = layout.box()
                box.label(text=f"Largura: {x_largura} {un}")
                box.label(text=f"Comprimento: {y_largura} {un}")
                box.label(text=f"Altura: {z_largura} {un}")
            else:
                layout.label(text="Selecione uma das seguintes unidades:", icon="ERROR")
                layout.label(text="MILIMETROS, CENTIMETROS ou METROS")


class ADMIN_PT_preferencias(Panel):
    bl_label = "PAINEL DE PREFERENCIAS"
    bl_idname = "PANEL_PT_preferencias"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FERRAMENTAS"
    bl_options = {"DEFAULT_CLOSED"}
    mostrar = True

    def draw_header(self, context):
        self.layout.label(text="", icon="USER")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        wm = context.window_manager
        prefs = context.preferences
        view = prefs.view
        row.label(text="Cor Fundo")
        row = layout.row()
        row.prop(
            bpy.context.preferences.themes["Default"].view_3d.space.gradients,
            "high_gradient",
            text="",
        )
        layout.menu("USERPREF_MT_interface_theme_presets", text="Tema")
        layout.prop(
            bpy.context.preferences.themes["Default"].view_3d.space.gradients,
            "background_type",
            text="Gradiente Fundo",
        )
        # layout.prop(bpy.context.preferences.view, "language", text="Idioma") # DESATIVADO POIS INTERFERE NO FUNCIONAMENTO DO PROGRAMA
        layout.prop(view, "ui_scale", text="Escala da interface")


# painel com a UI do exportador
class PLAYMAKER_PT_painel_exportador_modelos(Panel):
    """PAINEL DO EXPORTADOR DE MODELOS 3D"""

    bl_label = "EXPORTADOR"
    bl_idname = "PLAYMAKER_PT_painel_exportador_modelos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FERRAMENTAS"
    #    bl_options = {"DEFAULT_CLOSED"}

    # @classmethod
    # def poll(cls, context):
    #     return bpy.types.PLAYMAKER_PT_painel_exportador_modelos.mostrar != False

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(bpy.context.scene, "nome_arquivo_exportado", text="Nome")
        row = layout.row()
        row.operator("object.obj_operator", text=".DAE").action = "DAE"
        row.operator("object.obj_operator", text=".DXF").action = "DXF"
        row.operator("object.obj_operator", text=".GLB").action = "GLB"


classes = (
    ADMIN_PT_area_custom_1,
    ADMIN_PT_medir_produto,
    ADMIN_PT_preferencias,
    PLAYMAKER_PT_painel_exportador_modelos,
)


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
