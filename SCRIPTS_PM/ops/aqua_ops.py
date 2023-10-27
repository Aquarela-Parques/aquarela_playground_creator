import os
import bpy
from bpy.types import PropertyGroup, Operator
from funcoes.aqua_funcoes import output_modelo_exportar, preparar_objetos
from funcoes.aqua_obj_props import pasta_cores

from modelos.aqua_importador import LimparAssetMateriais


class CONJUNTO_OT_confirmar_acao(Operator):
    """Você tem certeza?"""

    bl_idname = "conjunto_ot.confirmar_acao"
    bl_label = "VOCÊ TEM CERTEZA?"
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.admin.admin_op(action="OPEN")
        self.report({"INFO"}, "OBJETO ABERTO!")
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class PLAYMAKER_OT_girar_90_graus(Operator):  # GIRAR_OT_90graus
    bl_idname = "object.girar_90"
    bl_label = "Girar 90º"

    def execute(self, context):
        obj = bpy.context.object
        obj.rotation_euler.z = obj.rotation_euler.z + 1.5707963705062866
        print("Giro 90 graus")

        return {"FINISHED"}


class PLAYMAKER_OT_CarregarCores(Operator):
    """Carregar Pasta Cores"""

    bl_idname = "object.carregar_cores"
    bl_label = "Carregar Cores"

    def execute(self, context):
        pasta_cores()
        LimparAssetMateriais()
        return {"FINISHED"}


# define o caminho para a area de trabalho do usuario


# operador com EnumProperty para gerenciar as ações de cada exportador e suas respectivas necessidaes para cada arquivo
class PLAYMAKER_OT_exportador_modelos(Operator):
    """EXPORTADOR"""

    bl_idname = "object.obj_operator"
    bl_label = "Exportador Modelos 3D"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    action: bpy.props.EnumProperty(
        items=[
            ("DAE", "dae", "EXPORTAR EM .DAE"),
            ("DXF", "dxf", "EXPORTAR EM .DXF"),
            ("GLB", "glb", "EXPORTAR EM .GLB"),
        ]
    )

    def execute(self, context):
        preparar_objetos()

        if self.action == "DAE":
            bpy.context.view_layer.objects.active = bpy.data.objects["PLATAFORMA M1"]
            bpy.ops.object.join()
            bpy.ops.object.shade_flat()
            bpy.ops.wm.collada_export(
                filepath=output_modelo_exportar(".dae"),
                selected=True,
                apply_modifiers=True,
            )

        if self.action == "DXF":
            bpy.context.view_layer.objects.active = bpy.data.objects["PLATAFORMA M1"]
            bpy.ops.object.join()
            bpy.ops.export.dxf(filepath=output_modelo_exportar(".dxf"))

        if self.action == "GLB":
            bpy.ops.export_scene.gltf(
                filepath=output_modelo_exportar(".glb"),
                export_format="GLB",
                export_apply=True,
                use_selection=True,
            )

        return {"FINISHED"}


classes = (
    PLAYMAKER_OT_CarregarCores,
    CONJUNTO_OT_confirmar_acao,
    PLAYMAKER_OT_girar_90_graus,
    PLAYMAKER_OT_exportador_modelos,
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
