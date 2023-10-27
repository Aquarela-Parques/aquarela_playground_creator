import bpy
from bpy.types import PropertyGroup, UIList, Operator, Panel

from funcoes.aqua_database import (
    create_database_tb_itens,
    salvar_dados_itens_obj,
    select_kits_pf,
)


class ADMIN_OT_propriedades_derivacao(Operator):
    """Adiciona a lista de DERIVACOES do Item em Contexto"""

    bl_idname = "admin.propriedades_derivacao"
    bl_label = "Adiciona a lista de DERIVACOES do Item em Contexto"

    def execute(self, context):
        for derivacao in bpy.context.scene.propriedades_derivacao:
            if derivacao.adicionar == True:
                print(derivacao)

        return {"FINISHED"}


class ADMIN_OT_propriedades_adicionar_derivacoes(Operator):
    bl_idname = "admin.adicionar_derivacoes_selecionados"
    bl_label = "adicionar Derivacoes"

    def execute(self, context):
        # TODO ADICIONAR FUNCIONALIDADE DE REORGANIZAR O INDEX DA LISTA E EXCLUIR ITEMS
        for _d in bpy.context.scene.propriedades_derivacao:
            if _d.adicionar == True:
                bpy.context.scene.propriedades_derivacao_selecionada.add().derivacao_selecionada = (
                    _d.derivacao
                )

        for _n in bpy.context.scene.propriedades_derivacao:
            if _n.adicionar == True:
                _n.adicionar = False

        print("operador funcionando")

        return {"FINISHED"}


class ADMIN_OT_mover_prioridade_derivacao(Operator):

    """Move an item in the list."""

    bl_idname = "admin.mover_derivacao"
    bl_label = "Move an item in the list"

    direcao: bpy.props.EnumProperty(
        items=(
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
        )
    )

    @classmethod
    def poll(cls, context):
        return context.scene.propriedades_derivacao_selecionada

    def move_index(self):
        """Move index of an item render queue while clamping it."""

        index = bpy.context.scene.propriedades_derivacao_selecionada_index
        list_length = (
            len(bpy.context.scene.propriedades_derivacao_selecionada) - 1
        )  # (index starts at 0)
        new_index = index + (-1 if self.direcao == "UP" else 1)

        bpy.context.scene.propriedades_derivacao_selecionada_index = max(
            0, min(new_index, list_length)
        )

    def execute(self, context):
        my_list = context.scene.propriedades_derivacao_selecionada
        index = context.scene.propriedades_derivacao_selecionada_index

        neighbor = index + (-1 if self.direcao == "UP" else 1)
        my_list.move(neighbor, index)
        self.move_index()

        return {"FINISHED"}


class ADMIN_OT_propriedades_listar_kits_pf(Operator):
    bl_idname = "admin.listar_kits_pf"
    bl_label = "Listar Kits PF"
    bl_description = "Listar Kits PF"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.context.scene.propriedades_kits_pf.clear()
        for kit in tuple(select_kits_pf()):
            bpy.context.scene.propriedades_kits_pf.add().kits_pf = str(
                f"{kit[0]} {kit[1]}"
            )
        return {"FINISHED"}


class ADMIN_OT_propriedades_adicionar_kits_pf(Operator):
    bl_idname = "admin.adicionar_kits_pf_selecionados"
    bl_label = "adicionar Kits PF"

    @classmethod
    def poll(cls, context):
        return context.scene.propriedades_kits_pf

    def execute(self, context):
        def quantidade_kits():
            for _n in bpy.context.scene.propriedades_kits_pf:
                if _n.adicionar == True:
                    yield _n.kits_pf, _n.quantidade

        for _ in list(quantidade_kits()):
            for _n in range(_[1]):
                bpy.context.scene.propriedades_kits_pf_selecionados.add().kits_pf_selecionados = _[
                    0
                ]

        for _n in bpy.context.scene.propriedades_kits_pf:
            if _n.adicionar == True:
                _n.adicionar = False
                _n.quantidade = 1

        return {"FINISHED"}


class ADMIN_OT_deletar_derivacoes(Operator):
    """Delete the selected item from the list."""

    bl_idname = "admin.deletar_derivacao"
    bl_label = "Remove a derivacao inserida"

    @classmethod
    def poll(cls, context):
        return context.scene.propriedades_derivacao_selecionada

    def execute(self, context):
        my_list = context.scene.propriedades_derivacao_selecionada
        index = context.scene.propriedades_derivacao_selecionada_index

        my_list.remove(index)
        context.scene.propriedades_derivacao_selecionada_index = min(
            max(0, index - 1), len(my_list) - 1
        )

        return {"FINISHED"}


class ADMIN_OT_deletar_kit_pf(Operator):
    """Delete the selected item from the list."""

    bl_idname = "admin.deletar_kit_pf"
    bl_label = "Remove um kit pf"

    @classmethod
    def poll(cls, context):
        return context.scene.propriedades_kits_pf_selecionados

    def execute(self, context):
        my_list = context.scene.propriedades_kits_pf_selecionados
        index = context.scene.propriedades_kits_pf_selecionados_index

        my_list.remove(index)
        context.scene.propriedades_kits_pf_selecionados_index = min(
            max(0, index - 1), len(my_list) - 1
        )

        return {"FINISHED"}


class ADMIN_OT_salvar_dados(Operator):
    bl_idname = "admin.salvar_dados"
    bl_label = "Salvar dados do Objeto"
    bl_description = "Salva os dados do Objeto no banco de dados"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        salvar_dados_itens_obj()
        self.report({"INFO"}, "Dados salvos com sucesso!")
        return {"FINISHED"}


# TODO CRIAR FUNÇÃO EXTERNA PARA SALVAR OS DADOS DO PAINEL DE CADASTRO DE ITEM NO BANCO DE DADOS tb_itens
# TODO CRIAR METODO PARA EXIBIR AS INFORMAÇÕES JÁ SALVAS DOS ITEMS CADASTRADOS

classes = (
    ADMIN_OT_mover_prioridade_derivacao,
    ADMIN_OT_propriedades_derivacao,
    ADMIN_OT_deletar_derivacoes,
    ADMIN_OT_propriedades_adicionar_derivacoes,
    ADMIN_OT_propriedades_listar_kits_pf,
    ADMIN_OT_propriedades_adicionar_kits_pf,
    ADMIN_OT_deletar_kit_pf,
    ADMIN_OT_salvar_dados,
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
