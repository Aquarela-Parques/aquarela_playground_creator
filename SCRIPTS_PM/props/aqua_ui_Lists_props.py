import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty, BoolProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel


class ADMIN_PG_propriedades_derivacoes(PropertyGroup):
    """Lista dos .blends presentes nas pastas de items dos projetos das prefeituras"""

    derivacao: StringProperty(
        name="Derivacao", description="Derivação do item em questão"
    )
    adicionar: BoolProperty(default=False)


class ADMIN_PG_derivacoes_selecionadas(PropertyGroup):
    """Lista dos .blends presentes nas pastas de items dos projetos das prefeituras"""

    derivacao_selecionada: StringProperty(
        name="Derivacao Selecionada", description="Derivação selecionada"
    )


class ADMIN_PG_propriedades_kits_pf(PropertyGroup):
    """Lista dos Kits PF para adição nos items"""

    kits_pf: StringProperty(name="Kits PF", description="Kit PF", default="Untitled")
    quantidade: IntProperty(
        name="quantidade",
        description="Quantidade de kits Adicionados",
        min=1,
        max=10,
        default=1,
    )
    adicionar: BoolProperty(default=False)


class ADMIN_PG_propriedades_kits_pf_selecionados(PropertyGroup):
    """Lista dos Kits PF adicionados no item"""

    kits_pf_selecionados: StringProperty(name="Kits PF", description="Kit PF")


class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def execute(self, context):
        bpy.context.object.aqua.codigo = bpy.context.object.aqua.codigo

        return {"FINISHED"}

    def modal(self, context, event):
        if event.type == "LEFTMOUSE":  # Confirm
            self.execute(context)
            return {"FINISHED"}

        return {"RUNNING_MODAL"}


classes = (
    ADMIN_PG_propriedades_derivacoes,
    ADMIN_PG_derivacoes_selecionadas,
    ADMIN_PG_propriedades_kits_pf,
    ADMIN_PG_propriedades_kits_pf_selecionados,
    ModalOperator,
)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    # ui list derivacoes
    bpy.types.Scene.propriedades_derivacao = CollectionProperty(
        type=ADMIN_PG_propriedades_derivacoes
    )
    bpy.types.Scene.propriedades_derivacao_index = IntProperty(
        name="Index para propriedades_derivacao", default=0
    )

    # ui list derivacoes selecionadas
    bpy.types.Scene.propriedades_derivacao_selecionada = CollectionProperty(
        type=ADMIN_PG_derivacoes_selecionadas
    )
    bpy.types.Scene.propriedades_derivacao_selecionada_index = IntProperty(
        name="Index para propriedades_derivacao", default=0
    )

    # ui list kits pf
    bpy.types.Scene.propriedades_kits_pf = CollectionProperty(
        type=ADMIN_PG_propriedades_kits_pf
    )
    bpy.types.Scene.propriedades_kits_pf_index = IntProperty(
        name="Index para propriedades_kits_pf", default=0
    )

    # ui list kits pf selecionados
    bpy.types.Scene.propriedades_kits_pf_selecionados = CollectionProperty(
        type=ADMIN_PG_propriedades_kits_pf_selecionados
    )
    bpy.types.Scene.propriedades_kits_pf_selecionados_index = IntProperty(
        name="Index para propriedades_kits_pf_selecionados", default=0
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.propriedades_derivacao
    del bpy.types.Scene.propriedades_derivacao_index

    del bpy.types.Scene.propriedades_derivacao_selecionada
    del bpy.types.Scene.propriedades_derivacao_selecionada_index

    del bpy.types.Scene.propriedades_kits_pf
    del bpy.types.Scene.propriedades_kits_pf_index

    del bpy.types.Scene.propriedades_kits_pf_selecionados
    del bpy.types.Scene.propriedades_kits_pf_selecionados_index


if __name__ == "__main__":
    register()
