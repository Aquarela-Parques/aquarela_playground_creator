import ast
import json
import os
import sqlite3
import bpy
from bpy.types import PropertyGroup, Operator
from bpy.props import EnumProperty
from bpy_plus.file_system import Path

from funcoes.aqua_funcoes import caminhos_pastas
from funcoes.aqua_obj_props import (
    carregar_dados_kit_pf_objeto,
    carregar_dados_objeto,
    remove_mat_duplicados,
)


class PLAYMAKER_OT_conectar_objetos(Operator):
    bl_idname = "object.conectar"
    bl_label = "Conectar"
    bl_description = "Conectar"
    bl_options = {"REGISTER", "UNDO"}

    action: EnumProperty(
        items=[
            ("CHECAR", "checar", "checar"),
            ("CONECTAR", "conectar", "conectar"),
            ("DESCONECTAR", "desconectar", "desconectar"),
            ("CONFLITO", "conflito", "conflito"),
        ]
    )

    def execute(self, context):
        if self.action == "checar":
            self.CHECAR(context=context, self=self)

        if self.action == "CONECTAR":
            self.CONECTAR(context=context, self=self)

        elif self.action == "DESCONECTAR":
            self.DESCONECTAR(context=context, self=self)

        elif self.action == "CONFLITO":
            self.CONFLITO(context=context, self=self)

        return {"FINISHED"}

    @staticmethod
    def CHECAR(self, context):
        obj = bpy.context.object

        location = obj.constraints.new("COPY_LOCATION")
        location.use_z = False

        obj.parent = obj.aqua.alvo
        obj.constraints["Copy Location"].target = obj.aqua.alvo
        obj.matrix_parent_inverse = obj.aqua.alvo.matrix_world.inverted()

        try:
            # MOVER PRO PRO TOPO
            con = obj.constraints["Copy Location"]

            ctx = bpy.context.copy()
            ctx["constraint"] = con

            bpy.ops.constraint.move_up(ctx, constraint=con.name, owner="OBJECT")

            self.report(
                {"INFO"}, f"{obj.name_full} conectado a {obj.aqua.alvo.name_full}"
            )
        except ValueError as ERROR:
            print(ERROR, obj.name_full, "->", obj.aqua.alvo.name_full)

    @staticmethod
    def CONECTAR(self, context):
        obj = bpy.context.object

        if obj.show_bounds == True:
            # CHECAR SE NOME É O MESMO
            if bpy.context.object.name_full == obj.aqua.alvo.name_full:
                self.report({"ERROR"}, "OBJETO NAO PODE CONECTAR A ELE MESMO!")
                bpy.types.MODELOS_PT_painel_modelos.erro = True

            elif bpy.context.object.aqua.fixo == False:
                self.CHECAR(self, context)

            elif round(bpy.context.object.location.z, 2) == round(
                bpy.context.object.aqua.alvo.location.z, 2
            ):
                self.CHECAR(self, context)

            else:
                self.report({"ERROR"}, "AJUSTE A ALTURA DA PLATAFORMA!")
                bpy.types.MODELOS_PT_painel_modelos.erro = True

        else:
            self.report({"ERROR"}, "ESCOLHA UM OBJETO PARA CONECTAR")
        bpy.ops.object.visual_transform_apply()

    @staticmethod
    def DESCONECTAR(self, context):
        print("desconectado")
        bpy.types.MODELOS_PT_painel_modelos.erro = False
        obj = bpy.context.object

        for c in obj.constraints:
            if "Copy Location" in c.name:
                obj.constraints.remove(c)
        obj.parent = None

    @staticmethod
    def CONFLITO(self, context):
        bpy.context.object.aqua.alvo = None
        bpy.types.MODELOS_PT_painel_modelos.erro = False


class PLAYMAKER_OT_recarregar_dados(Operator):  # RECARREGAR_OT_dados
    bl_idname = "scene.recarregar_dados"
    bl_label = "Recarregar Dados"
    action: bpy.props.EnumProperty(
        items=[
            ("carregar_dados_objeto", "carregar_dados_objeto", "carregar_dados_objeto"),
            (
                "carregar_dados_kit_pf_objeto",
                "carregar_dados_kit_pf_objeto",
                "carregar_dados_kit_pf_objeto",
            ),
        ]
    )

    def execute(self, context):
        # CARREGA OS DADOS DO PARQUE NOVAMENTE PARA PUXAR DERIVAÇÃO E KIT
        if self.action == "carregar_dados_objeto":
            # ATUALIZAR DADOS DE OBJETO
            # carregar_dados_objeto(bpy.context.scene.objects)
            # carregar_dados_objeto(bpy.context.scene.objects)
            carregar_dados_objeto(bpy.types.MODELOS_OT_obj_preview.res_obj)
            print("cores")

            for col in bpy.data.collections:
                nome_colecao = col.name_full.split(".")[0]
                if col.kit_pf.keys() != []:
                    col.kit_pf.clear()

                    caminho_db = os.path.join(Path.blender(), "database")

                    conect = sqlite3.connect(os.path.join(caminho_db, "playmaker.db"))
                    pm_db = conect.cursor()

                    select_props = """
                        SELECT
                            kits_pf
                        FROM
                            tb_itens
                        WHERE
                            nome = ?
                            and nome not like ('COLUNA MAD PLAST%')
                            and parametro = 'COLECAO';
                    """

                    pm_db.execute(select_props, (nome_colecao,))

                    for info_item in pm_db.fetchall():
                        for i in ast.literal_eval(info_item[0]):
                            col.kit_pf.add().name = i

            # # ATUALIZAR DADOS DE COLECAO
            # for col in bpy.data.collections:
            #     if col.kit_pf.keys() != []:
            #         col.kit_pf.clear()

            #         file = f"{caminhos_pastas()[0]}\\{col.name_full.split('.')[0]}.txt"

            #         with open(file) as json_data:
            #             p = json.load(json_data)
            #             for o in p["kits_pf"]:
            #                 col.kit_pf.add().name = o

        if self.action == "carregar_dados_kit_pf_objeto":
            # ATUALIZAR DADOS DE OBJETO
            carregar_dados_kit_pf_objeto(self, bpy.context.scene.objects)

            # ATUALIZAR DADOS DE COLECAO
            for col in bpy.data.collections:
                if col.kit_pf.keys() != []:
                    col.kit_pf.clear()

                    file = f"{caminhos_pastas()[0]}\\{col.name_full.split('.')[0]}.txt"

                    with open(file) as json_data:
                        p = json.load(json_data)
                        for o in p["kits_pf"]:
                            col.kit_pf.add().name = o

                            json_data.close()

        return {"FINISHED"}


class PLAYMAKER_OT_carregar_dados(Operator):  # CARREGAR_OT_dados
    bl_idname = "object.carregar_dados"
    bl_label = "Carregar Dados"

    def execute(self, context):
        # ATUALIZAR DADOS DA COLECAO

        # for col in bpy.types.MODELOS_OT_obj_preview.res_col:
        #     nome = col.name_full.split(".")[0]
        #     file = caminhos_pastas()[0] + nome + ".txt"

        #     # checar se o arquivo existe
        #     if os.path.exists(file):
        #         # LIMPAR COLECAO POR VIA DAS DUVIDAS
        #         col.kit_pf.clear()

        #         with open(file) as json_data:
        #             p = json.load(json_data)

        #             for o in p["kits_pf"]:
        #                 col.kit_pf.add().name = o

        #     else:
        #         print(f"{file} NAO ENCONTRADO - PLAYMAKER_OT_carregar_dados(Operator)")

        # ATUALIZAR DADOS DE OBJETO
        carregar_dados_objeto(bpy.types.MODELOS_OT_obj_preview.res_obj)

        # ------------------------------------------------------------
        # REMOVER MATERIAIS DUPLICADOS
        remove_mat_duplicados()

        return {"FINISHED"}


classes = (
    PLAYMAKER_OT_conectar_objetos,
    PLAYMAKER_OT_carregar_dados,
    PLAYMAKER_OT_recarregar_dados,
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
