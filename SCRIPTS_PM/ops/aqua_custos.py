import bpy
from bpy.types import Context, Operator, Panel, PropertyGroup

from funcoes.aqua_custos import (
    atualizar_custo,
    calculo_soma_total_local,
    contagem_individual_lista_local,
    custo_producao,
)


class CUSTO_OT_atualizar(Operator):
    bl_idname = "custo.atualizar"
    bl_label = "Atualizar Custo"

    def execute(self, context):
        bpy.types.CUSTO_PT_dados_custos.preco_sugerido = atualizar_custo()[1]
        bpy.types.CUSTO_PT_custo_producao.custo_producao = calculo_soma_total_local()
        bpy.types.CUSTO_PT_custo_producao.obj_sem_custo = custo_producao()[1]
        bpy.types.CUSTO_PT_custo_producao.custo_obj = contagem_individual_lista_local()
        print("Custo Atualizado")

        return {"FINISHED"}


class CUSTO_OT_tabela_por_item(Operator):
    bl_idname = "custo.tabela_por_item"
    bl_label = "Exportar Tabela de Itens"

    def execute(self, context: Context):
        from funcoes.aqua_custos import gerar_tabela_custo_por_item

        gerar_tabela_custo_por_item(bpy.context.scene.nome_arquivo_custo_item)
        return {"FINISHED"}


classes = (
    CUSTO_OT_atualizar,
    CUSTO_OT_tabela_por_item,
)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.nome_arquivo_custo_item = bpy.props.StringProperty(
        name="Nome Arquivo  "
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
