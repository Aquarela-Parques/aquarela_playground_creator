import bpy
from bpy.types import PropertyGroup


class ORCAMENTO_PG_propriedades_orcamento(PropertyGroup):
    titulo_proposta: bpy.props.StringProperty(name="Titulo", default="")
    valor_item: bpy.props.StringProperty(name="Valor Proposto", default="")

    cliente: bpy.props.StringProperty(name="Cliente", default="")
    email: bpy.props.StringProperty(name="Email", default="")
    contato: bpy.props.StringProperty(name="Contato", default="")
    local_salvamento_orcamento: bpy.props.StringProperty(
        name="Caminho", default="", subtype="FILE_PATH"
    )

    fundo_proposta: bpy.props.StringProperty(name="Fundo", default="")
    capa_proposta: bpy.props.StringProperty(name="Capa", default="")
    indice_proposta: bpy.props.StringProperty(name="Indice", default="")

    a_vista: bpy.props.StringProperty(name="A vista", default="")
    a_prazo: bpy.props.StringProperty(name="A prazo", default="")
    garantia: bpy.props.StringProperty(name="Garantia", default="")
    prazo_entrega: bpy.props.StringProperty(name="Prazo de entrega", default="")
    frete_instalacao: bpy.props.BoolProperty(name="Frete e instalação")
    data_proposta: bpy.props.StringProperty(name="Data da Proposta", default="")
    validade_proposta: bpy.props.StringProperty(name="Validade da Proposta", default="")

    img_iso: bpy.props.StringProperty(name="Img Iso", default="")
    img_topo: bpy.props.StringProperty(name="Img Top", default="")
    txt_proposta: bpy.props.StringProperty(name="Txt", default="")

    tamanho_fonte_proposta: bpy.props.IntProperty(
        name="Tamanho Fonte", default=50, min=10, max=60
    )


classes = (ORCAMENTO_PG_propriedades_orcamento,)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.orcamento = bpy.props.PointerProperty(
        type=ORCAMENTO_PG_propriedades_orcamento
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.orcamento


if __name__ == "__main__":
    register()
