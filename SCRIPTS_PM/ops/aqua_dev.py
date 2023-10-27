import bpy
from bpy.types import Operator, Panel
from funcoes.aqua_funcoes import painel_aviso
from funcoes.aqua_dev import (
    Upgrade_PIP,
    Install_Modules,
    Uninstall_Modules,
    Update_Modules,
)


class DESENVOLVEDOR_OT_ferramentas(Operator):
    bl_idname = "desenvolvedor.ferramentas"
    bl_label = "Ferramentas de Desenvolvedor"
    action: bpy.props.EnumProperty(
        items=[
            ("SALVAR_USUARIO", "SALVAR_USUARIO", "SALVAR_USUARIO"),
            ("upgrade_pip", "upgrade_pip", "upgrade_pip"),
            ("install_modules", "install_modules", "install_modules"),
            ("upgrade_modules", "upgrade_modules", "upgrade_modules"),
            ("uninstall_modules", "uninstall_modules", "uninstall_modules"),
        ]
    )

    def execute(self, context):
        if self.action == "upgrade_pip":
            Upgrade_PIP()
            painel_aviso("Pip Atualizado", "CONCLUIDO", "DOCUMENTS")
        if self.action == "install_modules":
            Install_Modules()
            painel_aviso(
                "Modulo Instalado, reinicialize o Playmaker", "CONCLUIDO", "DOCUMENTS"
            )
        if self.action == "upgrade_modules":
            Update_Modules()
            painel_aviso(
                "Modulo Atualizado, reinicialize o Playmaker", "CONCLUIDO", "DOCUMENTS"
            )
        if self.action == "uninstall_modules":
            Uninstall_Modules()
            painel_aviso(
                "Pacote Desinstalado, reinicialize o Playmaker",
                "CONCLUIDO",
                "DOCUMENTS",
            )
        return {"FINISHED"}


classes = (DESENVOLVEDOR_OT_ferramentas,)


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
