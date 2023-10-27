import bpy
from bpy.types import Panel


class COMERCIAL_PT_criar_proposta(Panel):
    bl_label = "CRIAR PROPOSTA"
    bl_idname = "COMERCIAL_PT_criar_proposta"
    bl_category = "PROPOSTA COMERCIAL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {"DEFAULT_CLOSED"}
    mostrar = True

    @classmethod
    def poll(cls, context):
        return bpy.types.COMERCIAL_PT_criar_proposta.mostrar != False

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="TEXT")

    def draw(self, context):
        obj = context.object
        layout = self.layout
        scene = context.scene

        layout.separator(factor = .5)
        layout.prop(bpy.context.scene.orcamento, "titulo_proposta", text="Titulo da Proposta")
        layout.prop(bpy.context.scene.orcamento, "local_salvamento_orcamento", text="Salvar em")
        
        layout.separator(factor = 2)
        box = layout.box()
        row = box.row(align=True)

        row.label(text="Cliente:")
        row.label(text="Email:")
        row.label(text="Contato:")
        row = box.row()
        row.prop(bpy.context.scene.orcamento, "cliente", text="")
        row.prop(bpy.context.scene.orcamento, "email", text="")
        row.prop(bpy.context.scene.orcamento, "contato", text="")

        box.separator(factor = 2)
        row = box.row()
        



        # col.prop(bpy.context.scene.orcamento, "contato", text="Contato")
        row.label(text="Condição a vista:")
        row.label(text="Condição a prazo:")
        row = box.row()
        row.prop(bpy.context.scene.orcamento, "a_vista", text="")
        row.prop(bpy.context.scene.orcamento, "a_prazo", text="")
        row = box.row()
        row.label(text="Garantia:")
        row.label(text="Prazo de entrega:")
        row = box.row()
        row.prop(bpy.context.scene.orcamento, "garantia", text="")
        row.prop(bpy.context.scene.orcamento, "prazo_entrega", text="")
        row = box.row()

        # box = layout.box()
        # col = box.column(align=True)
        row.label(text="Proposta feita em:")

        row.prop(
            bpy.context.scene.orcamento,
            "data_proposta",
            text="",
        )
        row = box.row()
        row.label(text="Validade da Proposta:")
        row.prop(
            bpy.context.scene.orcamento,
            "validade_proposta",
            text="",
        )
        layout.separator(factor = 2)
        row = layout.row()
        row.label(text="Tamanho Fonte", icon="FILE_FONT")
        row.prop(bpy.context.scene.orcamento, "tamanho_fonte_proposta", text="")
        row = layout.row()
        row.scale_y = 2
        row.operator("orcamento.gerar_orcamento")



        # row.operator(
        #     "scene.subprocess", text="1º PREPARAR PROPOSTA", icon="CURRENT_FILE"
        # ).action = "CRIAR_PROPOSTA_COMERCIAL"


classes = (COMERCIAL_PT_criar_proposta,)


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
