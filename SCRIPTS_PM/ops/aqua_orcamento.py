import os
import bpy
from bpy.types import Operator

from funcoes.aqua_orcamento import gerar_pdf


class ORCAMENTO_OT_gerar_orcamento(Operator):  # OPERADOR_OT_orcamento
    bl_idname = "orcamento.gerar_orcamento"
    bl_label = "Gerar Orçamento"

    def execute(self, context):
        # TODO : CRIAR ENTRADAS NA FUNCAO GERAR_PDF COM O CAMINHO DO PDF E COM O NOME
        bpy.ops.scene.criar_vistas(action="criar_circulacao")

        bpy.context.scene.cena.nome_vistas = bpy.context.scene.orcamento.titulo_proposta

        bpy.ops.scene.criar_vistas(action="vista_topo")
        bpy.ops.scene.criar_vistas(action="iso_frontal")

        pasta_imagem = os.path.join(
            bpy.context.scene.cena.desktop, bpy.context.scene.cena.nome_vistas
        )

        def scan_img():
            topo = None
            frontal = None

            with os.scandir(pasta_imagem) as SCAN_IMG_DIR:
                for file in SCAN_IMG_DIR:
                    if file.name.endswith("topo.png"):
                        topo = file.path
                    if file.name.endswith("frontal.png"):
                        frontal = file.path

            return topo, frontal

        bpy.ops.custo.atualizar()  # ATUALIZAR CUSTOS

        gerar_pdf(scan_img()[0], scan_img()[1])  # GERAR PDF
        self.report({"INFO"}, "Proposta Comercial Gerada!")

        return {"FINISHED"}


classes = (ORCAMENTO_OT_gerar_orcamento,)


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
