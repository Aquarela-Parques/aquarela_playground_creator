import bpy
from database.aqua_database import conexao_banco_local

pm_produtos = conexao_banco_local()[0]


def select_codpro():
    codigo_senior = bpy.context.object.aqua.codigo
    for produto in pm_produtos.execute(
        """select * from tb_produtos where codpro = ?""", (int(codigo_senior),)
    ).fetchall():
        if codigo_senior != "":
            yield produto[3], produto[2], produto[10], produto[11], produto[12]


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
