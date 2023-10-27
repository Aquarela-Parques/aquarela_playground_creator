import bpy
from bpy.types import Panel


class DEV_PT_ferramentas(Panel):
    """Painel para instalação de modulos e atualizacao do PIP."""

    bl_label = "DEV: INSTALAR MODULOS"
    bl_idname = "DEV_PT_ferramentas"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "PM - DESENVOLVEDOR"
    mostrar = True

    @classmethod
    def poll(cls, context):
        return bpy.types.DEV_PT_ferramentas.mostrar != False

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        # put a column layout into the box
        col = box.column()
        row = col.row(align=True)
        col.scale_y = 4
        col.separator(factor=1)
        row.prop(bpy.context.scene, "modulos", text="", icon="SYSTEM")
        col.scale_y = 3
        row = col.row(align=True)
        row.operator(
            "desenvolvedor.ferramentas", text="Instalar Modulo", icon="MODIFIER_ON"
        ).action = "install_modules"
        row = col.row(align=True)
        row.operator(
            "desenvolvedor.ferramentas", text="Desinstalar Modulo", icon="TRASH"
        ).action = "uninstall_modules"
        row = col.row(align=True)
        row.operator(
            "desenvolvedor.ferramentas", text="Update PIP", icon="SORT_DESC"
        ).action = "upgrade_pip"

        row.operator(
            "desenvolvedor.ferramentas", text="Update Modulo", icon="SORT_DESC"
        ).action = "upgrade_modules"


classes = (DEV_PT_ferramentas,)


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
