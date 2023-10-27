from collections import Counter
from decimal import Decimal

import bpy
from bpy.props import FloatProperty, IntProperty
from bpy.types import Context, Operator, Panel, PropertyGroup
from more_itertools import unique_everseen
from funcoes.aqua_custos import atualizar_custo, custo_producao

# from funcoes.aqua_custos import (
#     atualizar_custo,
#     calculo_soma_total_local,
#     contagem_individual_lista_local,
#     custo_producao,
#     calculo_soma_total,
#     contagem_individual_lista,
# )


class CUSTO_PT_variaveis(Panel):
    bl_label = "Variaveis Senior"
    bl_idname = "CUSTO_PT_variaveis"
    bl_space_type = "VIEW_3D"
    bl_options = {"DEFAULT_CLOSED"}
    bl_region_type = "UI"
    bl_category = "GESTAO DE VENDAS"
    bl_parent_id = "CUSTO_PT_custo_producao"
    mostrar = True

    @classmethod
    def poll(cls, context):
        if bpy.context.scene.cena.usuarios in [
            # "VENDEDOR",
            #            # "SUP_VENDAS",
            #            "PROJETOS",
            "ADMIN",
            "DESENVOLVEDOR",
            # "PCP",
            # "CATALOGO",
            #            "REVENDA",
        ]:
            return True

    def draw(self, context):
        sc = bpy.context.scene
        layout = self.layout

        layout.prop(sc.custo_preco, "TX_INSTALACAO_23")
        layout.prop(sc.custo_preco, "TX_TRANSPORTE_24")
        layout.prop(sc.custo_preco, "custo_coluna_mp")


class CUSTO_PT_dados_custos(Panel):
    bl_label = "Calculo Preço"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "CUSTO_PT_variaveis"
    bl_category = "GESTAO DE VENDAS"
    bl_options = {"DEFAULT_CLOSED"}

    preco_sugerido = 0
    mostrar = True

    @classmethod
    def poll(cls, context):
        if bpy.context.scene.cena.usuarios in [
            # "VENDEDOR",
            #            # "SUP_VENDAS",
            #            "PROJETOS",
            "ADMIN",
            "DESENVOLVEDOR",
            # "PCP",
            # "CATALOGO",
            #            "REVENDA",
        ]:
            return True

    def draw(self, context):
        layout = self.layout

        # if usuario_habilitado() == True:
        layout.separator()
        row = layout.row(align=True)
        row.label(text="DESCONTO:")
        row.prop(bpy.context.scene.custo_preco, "DESCONTO", text="%")
        row.label(text="ADITIVO:")
        row.prop(bpy.context.scene.custo_preco, "ADITIVO", text="%")
        layout.label(text=f"PRECO SUGERIDO: R${atualizar_custo()[1]}")

        # self.preco_sugerido = atualizar_custo()[1]

        layout.separator()
        if custo_producao()[1] != []:
            row2 = layout.row()
            row2.alert = True
            row2.label(text="Atenção! Os itens abaixo não possuem custo:".upper())
        layout.separator()


class CUSTO_PT_custo_producao(Panel):
    bl_label = "Custo Producao"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GESTAO DE CUSTOS"

    custo_producao = 0
    obj_sem_custo = None
    custo_obj = None
    mostrar = True

    @classmethod
    def poll(cls, context):
        return bpy.types.CUSTO_PT_custo_producao.mostrar != False

    def draw(self, context):
        layout = self.layout

        # if usuario_habilitado() == True:

        scl = 0.5
        if self.custo_obj != None:
            box = layout.box()
            row = box.row()
            col = row.column(align=True)
            col.scale_x = 0.45
            col.label(text="QTD")
            col = row.column(align=True)
            col.label(text="DESCRIÇÃO")
            col = row.column(align=True)
            col.label(text="DERIVAÇÃO")
            col = row.column(align=True)
            col.label(text="PRECO UNITÁRIO")
            col = row.column(align=True)

            contagem = Counter(bpy.types.CUSTO_PT_custo_producao.custo_obj)

            # for i in self.custo_obj:
            for desc, qtd in contagem.items():
                nome = desc.split(",")[1].replace("'", "")
                der = desc.split(",")[2].replace("'", "")
                #                preco_un = desc
                preco_un = round(float(desc.split(",")[3].replace(")", "")), 2)

                row = box.row()
                col = row.column(align=True)
                # row.label(text=str(qtd) + "   -   " + str(nome))
                col.label(text=f"{str(qtd)}")
                col.scale_x = 0.2
                col = row.column(align=True)
                col.label(text=f"{str(nome)}")
                col = row.column(align=True)
                col.label(text=f"{str(der)}")
                col = row.column(align=True)
                col.label(text=f"R$ {preco_un}")

            box = layout.box()
            row = box.row()
            if bpy.context.scene.cena.ancoragem == "NENHUM":
                row.label(text=f"CUSTO DE PRODUÇÃO: ESCOLHA UM PISO")
            else:
                row.label(text=f"CUSTO DE PRODUÇÃO: R${round(self.custo_producao,2)}")

            # if bpy.context.scene.cena.usuarios_pm in ["DANI", "IGOR"]:
            #     row = box.row()
            #     row.label(
            #         text=f"ACIMA DE 200MIL: R${round(self.custo_producao/0.33,2)}"
            #     )
            #     row = box.row()
            #     row.label(text=f"UNITÁRIO: R${round(self.custo_producao/0.25,2)}")
            #     row = box.row()
            #     row.label(
            #         text=f"FRETE E MONTAGEM (500KM): R${round(self.custo_producao/0.20,2)}"
            #     )
            layout.prop(bpy.context.scene, "nome_arquivo_custo_item")
            layout.operator("custo.tabela_por_item", icon="VIEW_ORTHO")
        layout.operator("custo.atualizar", icon="FILE_REFRESH")


classes = (
    CUSTO_PT_custo_producao,
    CUSTO_PT_variaveis,
    CUSTO_PT_dados_custos,
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
