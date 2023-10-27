import contextlib
import os
import shutil
import sqlite3

import bpy
import pyodbc

from bpy_plus.file_system import Path


def caminho_base():
    with contextlib.suppress(Exception):
        wm = bpy.data.window_managers["WinMan"]
    return f"{wm.caminho_modelo}\\{wm.obj_category}\\"


def caminhos_pastas():
    """
    This function returns the paths to various folders in the project.

    Returns:
    - modelos_pm (str): The path to the MODELOS_PM folder. caminhos_pastas()[0])
    - dados (str): The path to the DADOS_PM folder. caminhos_pastas()[1])
    - cores (str): The path to the CORES_PM folder. caminhos_pastas()[2])
    - scripts_pm (str): The path to the scripts folder. caminhos_pastas()[3])"""

    scripts_pm = bpy.utils.script_paths_pref()[0]

    root = os.path.dirname(scripts_pm)

    modelos_pm = os.path.join(root, f"MODELOS\\")
    dados = os.path.join(root, f"DADOS\\")
    cores = os.path.join(root, f"CORES\\")

    return (
        modelos_pm,  # caminhos_pastas()[0])
        dados,  # caminhos_pastas()[1])
        cores,  # caminhos_pastas()[2])
        scripts_pm,  # caminhos_pastas()[3])
    )


def painel_aviso(message="", title="Message Box", icon="INFO"):
    """
    Creates a message box with a specified message, title, and icon.

    Parameters:
        message (str): The message to display in the message box. Default is an empty string.
        title (str): The title of the message box. Default is "Message Box".
        icon (str): The icon to display in the message box. Default is "INFO".

    Returns:
        None
    """

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def conexao_banco(database_name="playmaker.db", database_folder="database"):
    """
    Connects to a SQLite database and returns a database cursor and connection object.

    Args:
        database_name (str): The name of the database. Defaults to "playmaker.db".
        database_folder (str): The folder where the database is located. Defaults to "database".

    Returns:
        pm_db (object): The database cursor object.
        conect (object): The database connection object.
    """
    blender_path = os.path.join(
        Path.blender(), database_folder
    )  # > CAMINHO DO PLAYMAKER
    if not os.path.exists(blender_path):
        os.mkdir(blender_path)  # > ASSEGURAR QUE A PASTA É CRIADA CASO NÃO EXISTA

    conect = sqlite3.connect(
        os.path.join(blender_path, database_name)
    )  # > CONNECT DO SQLITE3

    pm_db = conect.cursor()
    return pm_db, conect


def conexao_senior():
    """
    Establishes a connection to the Senior database.

    This function imports the `pyodbc` module and uses it to connect to the Senior database. It uses the following connection parameters:
    - Driver: SQL Server
    - Server: 191.238.216.86,1515
    - Database: AquSap_prd
    - UID: usrAquBIread
    - PWD: Ll1ne3-8Yx$c4p

    The function returns two objects:
    - `senior_cursor`: a cursor object for executing SQL queries on the Senior database
    - `senior_db`: the database connection object to the Senior database

    :return: A tuple containing the `senior_cursor` object and the `senior_db` object.
    :rtype: tuple
    """
    senior_db = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=191.238.216.86,1515;"
        "Database=AquSap_prd;"
        "UID=usrAquBIread;"
        "PWD=Ll1ne3-8Yx$c4p;"
    )
    senior_cursor = senior_db.cursor()
    return senior_cursor, senior_db


def nome_blend_aberto():
    file_path = bpy.path.basename(bpy.context.blend_data.filepath)
    return file_path.split(".")[0]


def colecoes_cena(t):
    # The code is defining a generator function called "colecoes_cena" that takes a tree-like data
    # structure as input. It yields the current node of the tree and then recursively yields all the
    # children nodes of the current node using the "yield from" statement. This allows the generator to
    # iterate through all the nodes in the tree in a depth-first manner.
    yield t
    for child in t.children:
        yield from colecoes_cena(child)


def lista_objetos():
    obj_cena = []

    obj_cena = [
        f"{ob.aqua.codigo}_{ob.aqua.nome}_{ob.aqua.leitura_derivacao.split('_')[1].upper()}"
        for ob in bpy.context.scene.objects
        if ob.aqua.nome != "" and ob.visible_get() == True
        if ob.aqua.leitura_derivacao != ""
        and ob.aqua.tipo_derivacao
        in [
            "05_unica",
            "10_cores",
            "20_tam mad plast",
        ]
    ]
    values_to_replace = [
        "_150 CM",
        "_230 CM",
        "_250 CM",
        "_270 CM",
        "_280 CM",
        "_300 CM",
        "_320 CM",
    ]
    for values in values_to_replace:
        obj_cena = [s.replace(f"{values}", "_UNICA") for s in obj_cena]

    return sorted(obj_cena)


def lista_parafuso():
    lista_parafuso = []
    lista_parafuso.clear()

    for col in bpy.data.collections:
        if col.hide_viewport == False:
            fix = bpy.context.scene.cena.ancoragem
            filtro = ["TERRA", "PISO"]
            col_keys = col.kit_pf.keys()
            if col_keys != []:
                for k in col_keys:
                    if fix in k:
                        lista_parafuso.append(k)
                    elif all(word not in k for word in filtro):
                        lista_parafuso.append(k)

                for obj in col.objects:
                    obj_keys = obj.kit_pf.keys()
                    if obj_keys != []:
                        for k in obj_keys:
                            if fix in k:
                                lista_parafuso.append(k)
                            elif all(word not in k for word in filtro):
                                lista_parafuso.append(k)

            else:
                for obj in col.objects:
                    if obj.hide_viewport == False and obj.kit_pf.keys() != []:
                        for k in obj.kit_pf.keys():
                            if fix in k:
                                lista_parafuso.append(k)
                            elif all(word not in k for word in filtro):
                                lista_parafuso.append(k)

    return [i for i in lista_parafuso if i != "0_KIT PF NULO"]


# REMOVER FACES E ARESTAS DA GUIA DA PLATAFORMA
def ajustar_guia_plataforma(obj):
    if obj.name.startswith("GUIA_PLATAFORMA"):
        # GARANTIR QUE NADA ESTEJA SELECIONADO
        bpy.ops.object.select_all(action="DESELECT")
        # SELECIONAR A GUIA DA PLATAFORMA E EXCLUIR AS FACES E VERTICE
        bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
        if bpy.context.mode == "OBJECT":
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.delete(type="EDGE_FACE")
            bpy.ops.object.editmode_toggle()


def preparar_objetos():
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        ajustar_guia_plataforma(obj)
        bpy.ops.object.select_all(action="SELECT")


def output_modelo_exportar(extensao):
    DESKTOP = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    nome_arquivo_exportado = bpy.context.scene.nome_arquivo_exportado

    output_modelo = os.path.join(DESKTOP, nome_arquivo_exportado + extensao)

    return output_modelo


# ------------------------------------------------------
# GERAR E SALVAR IMAGENS NO .BLEND E DEPOIS EXPORTAR PARA
# LOCAL SELECIONADO
# ------------------------------------------------------
def incorporar_imagens_catalogo():
    """
    Incorporates catalog images into the scene.

    Raises:
        Exception: If the file has not been saved.

    Returns:
        None
    """
    if not bpy.data.is_saved:
        raise Exception("Arquivo precisa ser salvo")

    bpy.ops.scene.criar_vistas(action="criar_circulacao")
    bpy.ops.scene.criar_vistas(action="vista_topo")
    bpy.ops.scene.criar_vistas(action="iso_frontal")
    bpy.ops.scene.criar_vistas(action="iso_conica")

    modelo_img = str(bpy.context.scene.cena.nome_vistas)
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    img_isolada = os.path.join(desktop, modelo_img)
    img_folder = os.listdir(img_isolada)

    for img in img_folder:
        str_img = str(img)
        img_path = os.path.join(img_isolada, img)
        bpy.ops.image.open(filepath=img_path, use_udim_detecting=False)
        bpy.data.images[str_img].save_render(
            filepath=os.path.join(os.path.dirname(bpy.data.filepath), modelo_img, img),
            scene=None,
        )
        bpy.data.images[img].use_fake_user = True

    bpy.ops.file.pack_all()
    bpy.ops.wm.save_mainfile()
    shutil.rmtree(img_isolada, ignore_errors=True)


classes = ()


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
