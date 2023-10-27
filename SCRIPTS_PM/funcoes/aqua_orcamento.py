import os

import bpy
from fpdf import FPDF
from classes.aqua_classes import Colecoes

from funcoes.aqua_funcoes import caminhos_pastas


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_text_color(r=2, g=88, b=42)
        self.set_font("Helvetica", "B", 160)
        # Move to the right
        #        self.cell(2)
        # Title
        self.cell(0, 30, bpy.context.scene.orcamento.titulo_proposta, 0, 0, "L")

        # Line brea
        self.ln(70)

    # Page footer
    def footer(self):
        if self.page_no() not in [1, 2]:
            # Position at 1.5 cm from bottom
            self.set_y(-30)
            # Arial italic 8
            self.set_font("Helvetica", "", 50)
            # Page number

            self.cell(0, 10, f"Página {str(self.page_no())}" + "/{nb}", 0, 0, "C")
            # self.image(
            #     f"{caminhos_pastas()[1]}logo.png",
            #     1090,
            #     630,
            #     140,
            # )

    def imagens(self):
        entrelinhas = 3
        self.cell(3, entrelinhas, " ", 0, 1)
        self.image(bpy.context.scene.orcamento.img_topo, 1000, 40, 220)
        self.image(bpy.context.scene.orcamento.img_iso, 600, 220, 450)


def gerar_pdf(topo, frontal):
    pdf = PDF(orientation="landscape", format=(720, 1280))
    pdf.set_left_margin(100)
    pdf.set_top_margin(60)

    pdf.center_window = True
    pdf.fit_window = True

    pdf.add_page("L")
    #    pdf.header()
    pdf.ln(150)
    pdf.set_font("Helvetica", "B", 120)
    pdf.cell(
        00,
        00,
        bpy.context.scene.orcamento.cliente,
    )
    pdf.set_font("Helvetica", "", 80)
    pdf.ln(10)
    pdf.cell(100, 240, "Email:")
    pdf.cell(
        100,
        240,
        bpy.context.scene.orcamento.email,
    )
    pdf.ln(10)
    pdf.cell(150, 280, "Contato:")
    pdf.cell(
        150,
        280,
        bpy.context.scene.orcamento.contato,
    )

    bpy.context.scene.orcamento.img_iso = frontal
    bpy.context.scene.orcamento.img_topo = topo

    # preparar pagina
    pdf.add_page("L")
    pdf.set_auto_page_break(auto=True, margin=-300)

    # pdf.set_font('Times', '', 12)
    pdf.set_font("Helvetica", "B", 120)
    # pdf.set_text_color(r=0, g=62, b=46)
    pdf.imagens()
    pdf.ln(20)
    # pdf.set_text_color(r=00, g=152, b=88)
    pdf.set_font("Helvetica", "B", 120)
    pdf.cell(
        10,
        00,
        bpy.context.scene.orcamento.valor_item,
    )
    pdf.ln(60)
    # pdf.set_text_color(r=00, g=115, b=75)
    pdf.set_font("Helvetica", "B", 70)
    pdf.cell(0, 10, "FICHA TÉCNICA:")
    # pdf.set_text_color(r=0, g=62, b=46)
    pdf.set_font("Helvetica", "", bpy.context.scene.orcamento.tamanho_fonte_proposta)
    pdf.ln(30)

    for colecoes in list(Colecoes().listar_colecoes_recursivas_cena()):
        pdf.multi_cell(200, 10, colecoes.name, 0)
        pdf.ln(10)

    pdf.add_page("L")
    pdf.ln(100)
    # pdf.set_text_color(r=255, g=255, b=255)
    pdf.set_font("Helvetica", "B", 70)
    pdf.cell(100, 00, "A vista:")
    pdf.set_font("Helvetica", "", 70)
    pdf.cell(110, 00, bpy.context.scene.orcamento.a_vista)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 70)
    pdf.cell(110, 60, "A prazo:")
    pdf.set_font("Helvetica", "", 70)
    pdf.cell(40, 60, bpy.context.scene.orcamento.a_prazo)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 70)
    pdf.cell(130, 120, "Garantia:")
    pdf.set_font("Helvetica", "", 70)
    pdf.cell(150, 120, bpy.context.scene.orcamento.garantia)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 70)
    pdf.cell(230, 180, "Prazo de entrega:")
    pdf.set_font("Helvetica", "", 70)
    pdf.cell(130, 180, bpy.context.scene.orcamento.prazo_entrega)
    pdf.ln(10)
    pdf.cell(1, 240, "Frete e Instalação já inclusos.")
    pdf.ln(250)
    pdf.set_font("Helvetica", "", 40)
    pdf.cell(180, 240, "Proposta feita em:")
    pdf.cell(13, 240, bpy.context.scene.orcamento.data_proposta)
    pdf.ln(20)
    pdf.cell(180, 240, "Validade da Proposta:")
    pdf.cell(13, 240, bpy.context.scene.orcamento.validade_proposta)

    DESKTOP = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

    output_pdf = os.path.join(
        DESKTOP, bpy.context.scene.orcamento.titulo_proposta + ".pdf"
    )
    local_salvamento_orcamento = os.path.join(
        bpy.context.scene.orcamento.local_salvamento_orcamento,
        bpy.context.scene.orcamento.titulo_proposta + ".pdf",
    )

    if bpy.context.scene.orcamento.local_salvamento_orcamento != "":
        pdf.output(
            local_salvamento_orcamento,
            "F",
        )
    else:
        pdf.output(
            output_pdf,
            "F",
        )

    return {"FINISHED"}


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
