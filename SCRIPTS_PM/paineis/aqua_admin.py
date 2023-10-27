import bpy
from bpy.types import PropertyGroup, UIList, Operator, Panel


class ADMIN_UL_propriedades_cores(UIList):
    """UI LIST contendo os items dos catalogos"""

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # We could write some code to decide which icon to use here...
        custom_icon = "FILE_BLEND"

        # Make sure your code supports all 3 layout types
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=item.derivacao, icon=custom_icon)
            layout.prop(item, "adicionar", text="", toggle=True)

        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)


class ADMIN_UL_propriedades_cores_selecionada(UIList):
    """UI LIST contendo os items dos catalogos"""

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # We could write some code to decide which icon to use here...
        custom_icon = "FILE_BLEND"

        # Make sure your code supports all 3 layout types
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=item.derivacao_selecionada, icon=custom_icon)

        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)


class ADMIN_UL_propriedades_kits_pf(UIList):
    """UI LIST contendo os kits pf"""

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # We could write some code to decide which icon to use here...
        custom_icon = "FILE_BLEND"

        # Make sure your code supports all 3 layout types
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=item.kits_pf, icon=custom_icon)
            layout.prop(item, "quantidade", text="", toggle=True)
            layout.prop(item, "adicionar", text="", toggle=True)

        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)


class ADMIN_UL_propriedades_kits_pf_selecionados(UIList):
    """UI LIST contendo os kits pf do item"""

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # We could write some code to decide which icon to use here...
        custom_icon = "FILE_BLEND"

        # Make sure your code supports all 3 layout types
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.label(text=item.kits_pf_selecionados, icon=custom_icon)

        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)


class ADMIN_PT_cadastro_objetos(bpy.types.Panel):
    bl_label = "PM_ADMIN: Cadastro de Objetos"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    # @classmethod
    # def poll(cls, context):
    #     if bpy.context.scene.cena.usuarios in [
    #         # "VENDEDOR",
    #         # "SUP_VENDAS",
    #         # "PROJETOS",
    #         "ADMIN",
    #         "DESENVOLVEDOR",
    #         "PCP",
    #         # "CATALOGO",
    #         # "REVENDA",
    #     ]:
    #         return True

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="MOD_HUE_SATURATION")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        object = bpy.context.object
        aqua = bpy.context.object.aqua
        cena = bpy.context.scene.cena
        scene = context.scene
        layout.label(text="DADOS DO OBJETO:")
        layout.prop(aqua, "codigo")
        row = layout.row().split(factor=0.1)
        #        row.prop(aqua, "nome", text="Descrição")
        row.label(text="Descrição:")
        row.label(text=f"{bpy.context.object.aqua.nome}")
        row.prop(aqua, "aqua")
        row.prop(object, "show_bounds", text="CONTORNO")
        row = layout.row().split(factor=0.1)
        row.label(text="Peso:")
        row.label(text=f"{bpy.context.object.aqua.peso}")

        #        row.prop(aqua, "peso", text="Em kg")

        #        layout.separator(factor=2)

        #        row = layout.row()
        #        row = layout.row()
        row.prop(aqua, "atualizar_cores", text="Cor Aleatoria")
        row.prop(aqua, "fixo", text="ALTURA FIXA")
        layout.separator(factor=2)
        row = layout.row().split(factor=0.5)
        row.prop(aqua, "tipo_derivacao", text="Tipo Der")
        row.prop(object, "display_bounds_type", text="")
        layout.separator(factor=2)
        row = layout.row().split(factor=0.7)
        # TODO : AJUSTAR INTERFACE QUANDO FOR != 10_cores e RETORNAR E APLICAR
        # DERIVAÇÕES DE ITENS DO BANCO NO PAINEL DE CONFIGURAÇAÕ DE DERIVAÇÕES
        if bpy.context.object.aqua.tipo_derivacao == "10_cores":
            box = row.box()

            split = box.split(factor=0.5)

            split.operator(
                "admin.adicionar_derivacoes_selecionados", text="Adicionar Derivação"
            )
            split.alert = True
            split.operator("admin.deletar_derivacao", icon="CANCEL")

            split = box.split(factor=1)

            split.template_list(
                "ADMIN_UL_propriedades_cores",
                "Propriedades_Derivacao",
                scene,
                "propriedades_derivacao",
                scene,
                "propriedades_derivacao_index",
            )

            box = row.box()

            split = box.split(factor=0.5)
            split.operator(
                "admin.mover_derivacao", text="", icon="TRIA_UP"
            ).direcao = "UP"
            split.operator(
                "admin.mover_derivacao", text="", icon="TRIA_DOWN"
            ).direcao = "DOWN"

            split = box.split(factor=1)

            split.template_list(
                "ADMIN_UL_propriedades_cores_selecionada",
                "Lista_Derivacao_Item",
                scene,
                "propriedades_derivacao_selecionada",
                scene,
                "propriedades_derivacao_selecionada_index",
            )

            row = layout.row()
        box = row.box()
        split = box.split(factor=0.5)
        split.operator("admin.listar_kits_pf", text="LISTAR KITS PF")
        split.operator("admin.adicionar_kits_pf_selecionados", text="ADICIONAR KITS PF")
        split.scale_y = 1.5
        split.alert = True
        split.operator("admin.deletar_kit_pf", text="REMOVER KITS PF", icon="CANCEL")
        split = box.split(factor=0.5)
        split.template_list(
            "ADMIN_UL_propriedades_kits_pf",
            "Propriedades_Kits_PF",
            scene,
            "propriedades_kits_pf",
            scene,
            "propriedades_kits_pf_index",
        )

        split.template_list(
            "ADMIN_UL_propriedades_kits_pf_selecionados",
            "",
            scene,
            "propriedades_kits_pf_selecionados",
            scene,
            "propriedades_kits_pf_selecionados_index",
        )

        row = layout.row()
        row.scale_y = 2
        row.operator(
            "admin.salvar_dados", text="SALVAR DADOS DO OBJETO", icon="GREASEPENCIL"
        )
        
        # enquadrar item (refinar processo[automatizar mudança do ponto de origem com base nas plataformas para item que forem fixados na mesma])


classes = (
    ADMIN_UL_propriedades_cores,
    ADMIN_UL_propriedades_cores_selecionada,
    ADMIN_UL_propriedades_kits_pf,
    ADMIN_UL_propriedades_kits_pf_selecionados,
    ADMIN_PT_cadastro_objetos,
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
