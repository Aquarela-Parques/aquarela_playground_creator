import bpy

# from pm_funcoes import (
#     atualizar_custo,
#     calculo_soma_total_local,
#     contagem_individual_lista_local,
#     custo_producao,
#     calculo_soma_total,
#     contagem_individual_lista,
# )
# from collections import Counter
from bpy.types import Context, Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, IntProperty

# from decimal import Decimal
# from more_itertools import unique_everseen


class CUSTO_PG_propriedades_custos(PropertyGroup):
    TX_FIN_1: FloatProperty(name="1-TAXA FINANCEIRA", soft_min=0, default=0.0)
    DIA_MEDIO_2: FloatProperty(
        name="2-DIA MEDIO DE FORMACAO DE PRECO", soft_min=0, default=0.0
    )
    DIA_COMPRA_3: FloatProperty(name="3-DIA MEDIO DE COMPRA", soft_min=0, default=0.0)
    DIA_PROD_4: FloatProperty(name="4-DIA MEDIO DE PRODUCAO", soft_min=0, default=0.0)
    DIA_VENDA_5: FloatProperty(name="5-DIA MEDIO DE VENDA", soft_min=0, default=0.0)
    PRAZO_ICMS_6: FloatProperty(
        name="6-PRAZO DE RECUPERACAO ICMS", soft_min=0, default=0.0
    )
    PRAZO_PIS_7: FloatProperty(
        name="7-PRAZO DE RECUPERACAO DE PIS", soft_min=0, default=0.0
    )
    PRAZO_COFI_8: FloatProperty(
        name="8-PRAZO DE RECUPERACAO DE COFINS", soft_min=0, default=0.0
    )
    IMP_RENDA_9: FloatProperty(name="9-IMPOSTO DE RENDA", soft_min=0, default=0.0012)
    CIF_10: FloatProperty(
        name="10-CUSTO INDIRETO DE FABRICACAO", soft_min=0, default=0.0
    )
    DF_11: FloatProperty(name="11-DESPESA FIXA", soft_min=0, default=0.0)
    SALDO_IMP_12: FloatProperty(
        name="12-SALDO DOS IMPERFEITOS", soft_min=0, default=0.3
    )
    P_LUC_LIQ_13: FloatProperty(
        name="13-PERCENTUAL DE LUCRO LIQUIDO", soft_min=0, default=0.0
    )
    V_LUC_LIQ_14: FloatProperty(
        name="14-VALOR DE LUCRO LIQUIDO", soft_min=0, default=0.0
    )
    P_MARG_CON_15: FloatProperty(
        name="15-PERCENTUAL DE MARGEM DE CONTRIBUICAO", soft_min=0, default=0.0
    )
    V_MARG_CON_16: FloatProperty(
        name="16-VALOR DE MARGEM DE CONTRIBUICAO", soft_min=0, default=0.0
    )
    PERC_ICMS_17: FloatProperty(name="17-PERCENTUAL DE ICMS", soft_min=0, default=0.18)
    PERC_IPI_18: FloatProperty(name="18-PERCENTUAL DE IPI", soft_min=0, default=0.0)
    PERC_PIS_19: FloatProperty(name="19-PERCENTUAL DE PIS", soft_min=0, default=0.0065)
    PERC_COFINS_20: FloatProperty(
        name="20-PERCENTUAL DE COFINS", soft_min=0, default=0.03
    )

    PERC_CSLL_21: FloatProperty(name="21-PERCENTUAL CSLL", soft_min=0, default=0.0082)
    PERC_COMISSAO_22: FloatProperty(
        name="22-PERCENTUAL COMISSAO", soft_min=0, default=0.015
    )
    TX_INSTALACAO_23: FloatProperty(name="23-TAXA INSTALACAO", soft_min=0, default=0.03)
    TX_TRANSPORTE_24: FloatProperty(name="24-TAXA TRANSPORTE", soft_min=0, default=0.07)
    TX_DESP_FIXA_25: FloatProperty(name="25-TAXA DESP. FIXA", soft_min=0, default=0.175)

    ADITIVO: IntProperty(name="ADITIVO", soft_min=0, soft_max=1000, default=0)
    DESCONTO: IntProperty(name="DESCONTO", soft_min=0, soft_max=25, default=0)

    custo_coluna_mp: FloatProperty(name="CUSTO COL MP", soft_min=0, default=37.73)


classes = (CUSTO_PG_propriedades_custos,)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    bpy.types.Scene.custo_preco = bpy.props.PointerProperty(
        type=CUSTO_PG_propriedades_custos
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
