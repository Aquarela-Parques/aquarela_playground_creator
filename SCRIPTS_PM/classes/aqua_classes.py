import bpy


# SELECIONAR COLECOES DA CENA
class Colecoes:
    def __init__(self):
        self.cena = bpy.context.scene.collection

    def listar_colecoes_cena(self):
        for col in self.cena.children:
            if col.name != "GERAR_VISTAS":
                yield col

    def listar_colecoes_recursivas_cena(self):
        for col in self.cena.children_recursive:
            if col.name != "GERAR_VISTAS":
                yield col

    def nome_colecoes_cena(self):
        for col in self.cena.children_recursive:
            if col.name != "GERAR_VISTAS":
                yield col.name

    def lista_torre_colecoes_cena(self):
        return [
            col.name
            for col in self.listar_colecoes_recursivas_cena()
            if col.name.startswith("TORRE") == True and col.hide_viewport == False
        ]


class Objetos:
    def __init__(self):
        self.objeto = bpy.data.objects

    def lista_objetos_aqua(self):
        for obj in self.objeto:
            if obj.aqua.nome != "" and obj.visible_get() == True:
                yield obj, obj.aqua.codigo, obj.aqua.nome, obj.aqua.leitura_derivacao.split(
                    "_"
                )[
                    1
                ].upper()[
                    :7
                ]

    def NomeEDerivacaoDict(self):
        for obj in self.objeto:
            if obj.aqua.leitura_derivacao != "":
                yield obj.aqua.nome, obj.aqua.leitura_derivacao


classes = ()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


if __name__ == "__main__":
    register()
