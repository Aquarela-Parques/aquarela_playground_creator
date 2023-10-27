import contextlib
import json
import bpy
from more_itertools import unique_everseen

from funcoes.aqua_funcoes import caminhos_pastas


def lista_funcoes_usuarios(self, context):
    """
    USADO PARA MONTAR DINAMICAMENTE A FUNCAO DOS USUARIOS COM BASE NOS VALORES DO ARQUIVO 'USUARIOS_PM.JSON'
    """
    lista_funcoes_usuarios = []
    lista_funcoes_usuarios_result = []

    with open(
        f"{caminhos_pastas()[9]}\\usuarios_pm.json", "r"
    ) as json_funcoes_usuarios:
        lista_funcoes_pm_json = json.load(json_funcoes_usuarios)

    lista_funcoes_usuarios = [
        (values, values, values) for values in lista_funcoes_pm_json.values()
    ]

    return unique_everseen(lista_funcoes_usuarios)


def lista_usuarios_pm(self, context):
    """
    USADA PARA CRIAR A ENUMPROPERY COM OS USUARIOS DE FORMA DINAMICA BASEADO NAS CHAVES DO ARQUIVO 'USUARIOS_PM.JSON'
    SE AS CHAVES (USUARIOS) FOREM IGUAL A SELECIONADA, bpy.context.scene.cena.funcoes_usuarios, A LISTA É MONTADA COM
    AS DETERMINADAS CHAVES
    """
    lista_usuarios_pm = []
    lista_usuarios_pm_result = []

    with open(f"{caminhos_pastas()[9]}\\usuarios_pm.json", "r") as json_usuarios:
        lista_usuarios_json = json.load(json_usuarios)

        lista_usuarios_pm = [
            (keys, keys, keys)
            for keys, values in lista_usuarios_json.items()
            if values == bpy.context.scene.cena.funcoes_usuarios
        ]
    return unique_everseen(lista_usuarios_pm)


def excluir_coll(self, context):
    with contextlib.suppress(AttributeError):
        with contextlib.suppress(RecursionError):
            for coll in bpy.data.collections:
                if coll.aqua.excluir == True:
                    print(f"{str(coll.name_full)} Excluido")
                    for col in coll.children:
                        col.aqua.excluir = True

            for col in bpy.data.collections:
                if col.aqua.excluir == True:
                    bpy.data.collections.remove(col)

            for objects in bpy.data.objects:
                if objects.users == 0:
                    bpy.data.objects.remove(objects)

            for meshes in bpy.data.meshes:
                if meshes.users == 0:
                    bpy.data.meshes.remove(meshes)


def coll_fixacao(self, context):
    print(bpy.context.collection.aqua.ancoragem)


def excluir_kitpf_coll(self, context):
    bpy.context.collection.kit_pf.clear()


def update_conectar(self, context):
    obj = bpy.context.object

    if obj.aqua.alvo is None:
        bpy.ops.object.conectar(action="DESCONECTAR")

    elif bpy.context.object.constraints.find("Copy Location"):
        bpy.ops.object.conectar(action="CONECTAR")


def filtro_alvo(self, object):
    return object.show_bounds == True


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
