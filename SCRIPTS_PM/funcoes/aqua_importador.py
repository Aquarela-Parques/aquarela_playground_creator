import contextlib
import json
import bpy
from more_itertools import unique_everseen
from funcoes.aqua_funcoes import (
    caminhos_pastas,
)


def caminho_arquivo():
    wm = bpy.context.window_manager
    return f"{caminhos_pastas()[0]}\\{wm.obj_preview.split('.')[0]}.tag"


def carregar_dados():
    score = []
    with open(caminho_arquivo(), "r") as arquivo:
        score.extend(str(line.strip()) for line in arquivo)
    return score


def nao_importado(self, context):
    layout = self.layout
    wm = context.window_manager
    rt = context.scene.cena

    layout.prop(wm, "obj_category", text="Categoria", expand=False)

    if bpy.context.scene.cena.usuarios == "VENDEDOR":
        if bpy.context.window_manager.obj_category.startswith(
            "CATALOGO"
        ) or bpy.context.window_manager.obj_category.startswith("LICITACAO"):
            row = layout.row()
            row.scale_y = 2
            row.template_icon_view(wm, "obj_preview", show_labels=True, scale_popup=6)

            row = layout.row()
            row.scale_y = 2
            row.operator(
                "modelos.obj_preview",
                text=f"IMPORTAR:        {wm.obj_preview.split('.')[0]}",
            )

            layout.separator()
            layout.separator()

            try:
                for i in carregar_dados():
                    layout.label(text=i)

                layout.separator()
                layout.separator()
                layout.label(text="PESO: --------------")
                layout.label(text="PRECO: -------------")

                layout.label(
                    text="Para visualizar PESO e PREÇO SUGERIDO, importe o Parque"
                )

            except FileNotFoundError:
                layout.label(text="LISTA NAO ENCONTRADA")

        else:
            layout.label(
                text="Selecione 'CATALOGO', 'CATALOGO LITORAL' ou 'CATALOGO PDF'"
            )


classes = ()


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
