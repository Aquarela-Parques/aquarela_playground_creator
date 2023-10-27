import os
import secrets
import bpy
import bmesh
import contextlib
from bpy.props import (
    EnumProperty,
    FloatProperty,
    # CollectionProperty,
    # PointerProperty,
    # BoolProperty,
)
import mathutils
from bpy_extras import object_utils
from bpy.types import Context, Operator, Panel, PropertyGroup
from funcoes.aqua_funcoes import (
    # incorporar_imagens_catalogo,
    # caminho_base,
    caminho_base,
    caminhos_pastas,
    incorporar_imagens_catalogo,
    # render_metadados,
)
from bpy_plus.file_system import Path


def update_camera_360(self, context):
    # TODO ADICIONAR CONTROLE ESPACIAL PARA A CAMERA
    for guia in bpy.data.objects:
        if guia.name.startswith("guia_360"):
            bpy.data.objects[guia.name].rotation_euler[2] = bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].gerar_vistas.rotacao
            bpy.data.objects[guia.name].scale[0] = bpy.data.objects[guia.name].scale[
                1
            ] = bpy.data.objects[guia.name].scale[2] = bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].gerar_vistas.distancia
            bpy.data.objects[guia.name].location[2] = bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].gerar_vistas.altura

            bpy.data.objects[guia.name].rotation_euler[2] = bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].gerar_vistas.rotacao
    bpy.data.objects["camera_360"].rotation_euler[0] = bpy.data.scenes[
        bpy.context.scene.cena.usuarios_pm
    ].gerar_vistas.ang_camera


class PLAYMAKER_PG_gerar_vistas(PropertyGroup):
    distancia: FloatProperty(
        name="Distância",
        default=1,
        update=update_camera_360,
        precision=2,
        soft_min=2,
        soft_max=8,
    )

    rotacao: FloatProperty(
        name="Rotação",
        default=0.0,
        soft_min=0.0,
        soft_max=6.2833,
        step=1,
        precision=2,
        update=update_camera_360,
    )

    altura: FloatProperty(
        name="Altura", default=2, update=update_camera_360, soft_min=2, soft_max=8
    )

    ang_camera: FloatProperty(
        name="Angulo da câmera",
        default=1.570796,
        update=update_camera_360,
        soft_min=-0.57,
        soft_max=0,
    )


# ----------------------------------------------------------
# IMPORTAR COLECAO COM DIMENSÕES CASO NÃO ESTEJA NA CENA
# ----------------------------------------------------------
def import_col_gerar_vistas():
    category = "MODELOS_PM"
    object_name = "GERAR_VISTAS"
    file_path = (
        f"{bpy.data.window_managers['WinMan'].caminho_modelo}\\{object_name}.blend"
    )
    inner_path = "Collection"
    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name,
    )

    bpy.context.scene.camera = bpy.data.objects["camera"]

    # CORRIGIR NOMES -  EXCLUIR .001 .002 ETC
    for obj in bpy.data.collections["GERAR_VISTAS"].objects:
        part = obj.name.rpartition(".")
        if part[2].isnumeric():
            part = part[0]
            obj.name = part


def update_esconder_sapatas(self, context):
    # ISOLAR OBJ COM NOME DE SAPATA
    for obj in bpy.context.scene.objects:
        if obj.name.startswith("SAPATA"):
            # GARANTIR QUE TODAS ESTEJAM VISIVEIS
            if bpy.data.collections["SAPATAS"].hide_viewport == True:
                bpy.data.collections["SAPATAS"].hide_viewport = False

            # INVERTER A CONDIÇÃO
            obj.hide_viewport = bpy.context.scene.esconder_sapatas == False


def Update_Ocultar_Colecoes(self, context):
    bpy.data.collections["GERAR_VISTAS"].hide_viewport = (
        bpy.context.scene.ocultar == True
    )

    bpy.data.collections["GERAR_VISTAS"].hide_render = bpy.context.scene.ocultar == True
    return


def remover_obj():
    for ob in bpy.data.objects:
        if ob.name.startswith("LIMITES_PARQUES"):
            bpy.data.objects.remove(ob, do_unlink=True)

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block, do_unlink=True)


def add_box(width, height, depth):
    verts = [
        (+1.0, +1.0, -1.0),
        (+1.0, -1.0, -1.0),
        (-1.0, -1.0, -1.0),
        (-1.0, +1.0, -1.0),
        (+1.0, +1.0, +1.0),
        (+1.0, -1.0, +1.0),
        (-1.0, -1.0, +1.0),
        (-1.0, +1.0, +1.0),
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (4, 0, 3, 7),
    ]

    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces


def ajustar_area_circulacao():
    # bpy.ops.outliner.orphans_purge()
    dimensoes = bpy.data.objects["DIMENSOES"]
    limite = bpy.data.objects["LIMITES_PARQUES"]
    limite.hide_viewport = False

    ac = 2.6
    margem = 2

    media = (dimensoes.scale.x + dimensoes.scale.y) / 4

    # AJUSTAR POSICAO
    dimensoes.location.xy = limite.location.xy

    # AJUSTAR LIMITE E DIMENSAO
    dimensoes.dimensions.xy = ((limite.dimensions.x + ac), (limite.dimensions.y + ac))
    limite.dimensions.xy = (
        (limite.dimensions.x + ac + margem + media),
        (limite.dimensions.y + ac + margem + media),
    )

    media = (dimensoes.scale.x + dimensoes.scale.y) / 4
    # AJUSTAR VETOR
    bpy.data.objects["dim_x"].scale.x = dimensoes.scale.x
    bpy.data.objects["dim_y"].scale.y = dimensoes.scale.y

    # AJUSTAR TEXTO
    bpy.data.curves["x"].body = "% s mts" % round(
        bpy.data.objects["dim_x"].dimensions.x, 1
    )
    bpy.data.curves["y"].body = "% s mts" % round(
        bpy.data.objects["dim_y"].dimensions.y, 1
    )

    bpy.data.objects["x"].scale.xy = media
    bpy.data.objects["y"].scale.xy = media

    limite.hide_viewport = True


def ajustar_area_limite():
    # bpy.ops.outliner.orphans_purge()
    dimensoes = bpy.data.objects["DIMENSOES"]
    limite = bpy.data.objects["LIMITES_PARQUES"]
    limite.hide_viewport = False

    ac = 0
    margem = 0

    media = (dimensoes.scale.x + dimensoes.scale.y) / 4

    # AJUSTAR POSICAO
    dimensoes.location.xy = limite.location.xy

    # AJUSTAR LIMITE E DIMENSAO
    dimensoes.dimensions.xy = ((limite.dimensions.x + ac), (limite.dimensions.y + ac))
    limite.dimensions.xy = (
        (limite.dimensions.x + ac + margem + media),
        (limite.dimensions.y + ac + margem + media),
    )

    media = (dimensoes.scale.x + dimensoes.scale.y) / 4
    # AJUSTAR VETOR
    bpy.data.objects["dim_x"].scale.x = dimensoes.scale.x
    bpy.data.objects["dim_y"].scale.y = dimensoes.scale.y

    # AJUSTAR TEXTO
    bpy.data.curves["x"].body = "% s mts" % round(
        bpy.data.objects["dim_x"].dimensions.x, 1
    )
    bpy.data.curves["y"].body = "% s mts" % round(
        bpy.data.objects["dim_y"].dimensions.y, 1
    )

    bpy.data.objects["x"].scale.xy = media
    bpy.data.objects["y"].scale.xy = media

    limite.hide_viewport = True


def group_bounding_box():
    # APAGAR BOUNDBOX (CASO EXISTA)
    remover_obj()

    # SELECIONAR OBJETOS
    bpy.ops.object.select_all(action="DESELECT")
    for ob in bpy.context.scene.objects:
        if ob.users_collection[0] != bpy.data.collections["GERAR_VISTAS"]:
            ob.select_set(True)

    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    location = [
        0.0,
    ] * 3
    for obj in bpy.context.selected_objects:
        for v in obj.bound_box:
            v_world = obj.matrix_world @ mathutils.Vector((v[0], v[1], v[2]))

            if v_world[0] < minx:
                minx = v_world[0]
            if v_world[0] > maxx:
                maxx = v_world[0]

            if v_world[1] < miny:
                miny = v_world[1]
            if v_world[1] > maxy:
                maxy = v_world[1]

            if v_world[2] < minz:
                minz = v_world[2]
            if v_world[2] > maxz:
                maxz = v_world[2]

    verts_loc, faces = add_box((maxx - minx) / 2, (maxz - minz) / 2, (maxy - miny) / 2)

    # CRIAR BOUNDBOX
    mesh = bpy.data.meshes.new("LIMITES_PARQUES")

    bm = bmesh.new()
    for v_co in verts_loc:
        bm.verts.new(v_co)
    bm.verts.ensure_lookup_table()

    for f_idx in faces:
        bm.faces.new([bm.verts[i] for i in f_idx])

    bm.to_mesh(mesh)
    mesh.update()
    location[0] = minx + ((maxx - minx) / 2)
    location[1] = miny + ((maxy - miny) / 2)
    location[2] = minz + ((maxz - minz) / 2)
    bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)

    bbox.location = location
    bbox.display_type = "BOUNDS"
    bbox.hide_render = True


# ------------------ CAMERA ---------------------------
def camera_iso():
    bpy.data.objects["camera"].data.lens = 360
    bpy.data.cameras["camera"].sensor_width = 36


def camera_micro():
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"
    bpy.data.cameras["camera"].clip_start = 0.0010
    bpy.data.objects["camera"].data.lens = 50
    bpy.data.cameras["camera"].sensor_width = 18


def camera_persp():
    bpy.data.objects["camera"].data.lens = 18
    bpy.data.cameras["camera"].sensor_width = 18


def angulo_camera(x, y, z, a):
    controle = bpy.data.objects["controle"]
    bpy.data.objects["controle"].rotation_euler.x = x
    bpy.data.objects["controle"].rotation_euler.y = y
    bpy.data.objects["controle"].rotation_euler.z = z
    bpy.data.objects["controle"].location[2] = a


def enquadrar_camera_topo():
    bpy.ops.object.select_all(action="SELECT")
    bpy.data.objects["LIMITES_PARQUES"].select_set(state=True)
    with contextlib.suppress(Exception):
        if bpy.context.scene.camera is None:
            bpy.ops.wm.save_mainfile()
            bpy.context.scene.camera = bpy.context.scene.objects["camera"]
    bpy.ops.view3d.camera_to_view_selected()


def enquadrar_camera():
    bpy.ops.object.select_all(action="SELECT")
    bpy.data.objects["LIMITES_PARQUES"].select_set(state=False)
    bpy.data.objects["DIMENSOES"].select_set(state=False)
    bpy.data.objects["dim_x"].select_set(state=False)
    bpy.data.objects["dim_y"].select_set(state=False)
    with contextlib.suppress(Exception):
        if bpy.context.scene.camera is None:
            bpy.ops.wm.save_mainfile()
            bpy.context.scene.camera = bpy.context.scene.objects["camera"]

    bpy.ops.view3d.camera_to_view_selected()


def enquadrar_camera_subprocess():
    bpy.ops.object.select_all(action="SELECT")
    bpy.data.objects["LIMITES_PARQUES"].select_set(state=False)
    # bpy.data.objects["DIMENSOES"].select_set(state=False)
    # bpy.data.objects["dim_x"].select_set(state=False)
    # bpy.data.objects["dim_y"].select_set(state=False)
    with contextlib.suppress(Exception):
        if bpy.context.scene.camera is None:
            bpy.ops.wm.save_mainfile()
            bpy.context.scene.camera = bpy.context.scene.objects["camera"]

    bpy.ops.view3d.camera_to_view_selected()


def ajustar_visual(show_overlay):
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.overlay.show_overlays = show_overlay

                    # TROCAR P VISAO CAMERA
                    cam = bpy.data.objects.get("camera")
                    bpy.context.view_layer.objects.active = cam
                    bpy.context.scene.camera = cam
                    area.spaces[0].region_3d.view_perspective = "CAMERA"


def salvar_vista(nome_vista, diretorio):
    ajustar_visual(False)
    # wm = bpy.context.window_manager

    col = str(bpy.context.scene.cena.nome_vistas)
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    file = os.path.join(f"{desktop}\\{col}", f"{col}-{nome_vista}")

    # se o diretorio do operador estiver vazio, ira salvar no desktop

    if diretorio == "":
        bpy.context.scene.render.filepath = file

    else:
        bpy.context.scene.render.filepath = f"{diretorio}\\{col}{nome_vista}"

    bpy.ops.render.opengl(write_still=True)


def salvar_vista_temp(nome_vista, diretorio):
    ajustar_visual(False)
    roto_modelo = bpy.context.scene.cena.modelo
    path_temp = os.path.join(Path.blender(), "temp")

    bpy.context.scene.render.filepath = f"{diretorio}\\{nome_vista}"

    bpy.ops.render.opengl(write_still=True)


def salvar_vista_modelos(nome_vista, diretorio):
    ajustar_visual(False)
    # wm = bpy.context.window_manager

    col = str(bpy.context.scene.cena.nome_vistas)
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    file = os.path.join(f"{desktop}\\{col}", f"{col}-{nome_vista}")

    # se o diretorio do operador estiver vazio, ira salvar no desktop

    if diretorio == "":
        bpy.context.scene.render.filepath = file

    else:
        bpy.context.scene.render.filepath = f"{diretorio}\\{nome_vista}"

    bpy.ops.render.opengl(write_still=True)


def salvar_vista_360(nome_vista, diretorio):
    # wm = bpy.context.window_manager

    col = str(bpy.context.scene.cena.nome_vistas)
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    file = os.path.join(f"{desktop}\\{col}", f"{col}-{nome_vista}")

    # se o diretorio do operador estiver vazio, ira salvar no desktop

    if diretorio == "":
        bpy.context.scene.render.filepath = file

    else:
        bpy.context.scene.render.filepath = f"{diretorio}\\{col}{nome_vista}"

    bpy.ops.render.opengl(write_still=True)


class PLAYMAKER_OT_criar_vistas(Operator):
    bl_idname = "scene.criar_vistas"
    bl_label = "Criar Vistas"
    bl_options = {"REGISTER", "UNDO"}
    action: EnumProperty(
        items=[
            ("criar_limitador", "criar_limitador", "criar_limitador"),
            ("criar_circulacao", "criar_circulacao", "criar_circulacao"),
            ("vista_topo", "vista_topo", "vista_topo"),
            (
                "vista_topo_thumb_parque",
                "vista_topo_thumb_parque",
                "vista_topo_thumb_parque",
            ),
            (
                "vista_topo_lista_confirmacao",
                "vista_topo_lista_confirmacao",
                "vista_topo_lista_confirmacao",
            ),
            ("iso_frontal", "iso_frontal", "iso_frontal"),
            ("iso_frontal_modelos", "iso_frontal_modelos", "iso_frontal_modelos"),
            ("iso_posterior", "iso_posterior", "iso_posterior"),
            ("iso_conica", "iso_conica", "iso_conica"),
            ("iso_conica_subprocess", "iso_conica_subprocess", "iso_conica_subprocess"),
            ("iso_custom", "iso_custom", "iso_custom"),
            ("completo", "completo", "completo"),
            ("incorporar_imagens", "incorporar_imagens", "incorporar_imagens"),
            ("imagens_batch", "imagens_batch", "imagens_batch"),
            ("insert_imagens_banco", "insert_imagens_banco", "insert_imagens_banco"),
            ("gerar_360", "gerar_360", "gerar_360"),
            ("upload_sharepoint", "upload_sharepoint", "upload_sharepoint"),
        ]
    )

    resolution: bpy.props.IntProperty(default=1000)
    caminho: bpy.props.StringProperty(default="")

    def execute(self, context):
        # -------------------------------------------------------------
        # ESSE TRECHO DEVE SER RESOLVIDO NA FUNCAO QUE CHAMAR O OPERADOR
        # -------------------------------------------------------------

        bpy.context.scene.render.resolution_x = self.resolution
        bpy.context.scene.render.resolution_y = self.resolution

        bpy.context.scene.render.image_settings.file_format = "PNG"
        bpy.context.scene.render.image_settings.color_mode = "RGBA"
        bpy.context.scene.render.film_transparent = True

        # -------------------------------------------------------------
        # VERIFICAR SE COLEÇAO EXISTE E IMPORTAR
        if bpy.context.scene.collection.children.find("GERAR_VISTAS") == -1:
            import_col_gerar_vistas()
        else:
            bpy.data.collections["GERAR_VISTAS"].hide_viewport = True

        # AJUSTAR PARAMETROS GLOBAIS
        bpy.context.scene.unit_settings.length_unit = "METERS"
        bpy.data.cameras["camera"].clip_start = 0.10

        # -------------------------------------------------------------

        if self.action == "criar_limitador":
            self.criar_limitador(context=context, self=self)

        if self.action == "criar_circulacao":
            self.criar_circulacao(context=context, self=self)
            self.criar_circulacao(context=context, self=self)

            with contextlib.suppress(Exception):
                # MOVER LIMITE PARA COLECAO GERAR VISTAS
                for limites_parque in bpy.data.objects:
                    if limites_parque != bpy.data.objects["LIMITES_PARQUES"]:
                        limites = bpy.data.objects["LIMITES_PARQUES"]
                        bpy.data.collections["GERAR_VISTAS"].objects.link(limites)
                        bpy.context.scene.collection.objects.unlink(limites)

        if self.action == "vista_topo":
            self.vista_topo(context=context, self=self)

        if self.action == "vista_topo_thumb_parque":
            self.vista_topo_thumb_parque(context=context, self=self)

        if self.action == "vista_topo_lista_confirmacao":
            self.vista_topo_lista_confirmacao(context=context, self=self)

        if self.action == "iso_frontal":
            self.iso_frontal(context=context, self=self)

        if self.action == "iso_frontal_modelos":
            self.iso_frontal_modelos(context=context, self=self)

        if self.action == "iso_posterior":
            self.iso_posterior(context=context, self=self)

        if self.action == "completo":
            self.completo(context=context, self=self)

        if self.action == "iso_conica":
            self.iso_conica(context=context, self=self)

        if self.action == "iso_conica_subprocess":
            self.iso_conica_subprocess(context=context, self=self)

        if self.action == "incorporar_imagens":
            self.incorporar_imagens(context=context, self=self)

        if self.action == "imagens_batch":
            self.imagens_batch(context=context, self=self)

        if self.action == "insert_imagens_banco":
            self.insert_imagens_banco(context=context, self=self)

        if self.action == "iso_custom":
            self.iso_custom(context=context, self=self)

        if self.action == "gerar_360":
            self.gerar_360(context=context, self=self)

        if self.action == "upload_sharepoint":
            self.upload_sharepoint(context=context, self=self)

        return {"FINISHED"}

    @staticmethod
    def criar_limitador(self, context):
        group_bounding_box()

    @staticmethod
    def criar_circulacao(self, context):
        try:
            group_bounding_box()
            ajustar_area_circulacao()
        except Exception:
            group_bounding_box()
            ajustar_area_limite()

        bpy.data.collections["GERAR_VISTAS"].hide_viewport = False
        bpy.types.PLAYMAKER_PT_gerar_vistas.estado = 1

    @staticmethod
    def vista_topo(self, context):
        bpy.data.collections["GERAR_VISTAS"].hide_viewport = False
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = False
        camera_iso()
        angulo_camera(0, 0, 0, 0)
        enquadrar_camera_topo()
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista("vista_topo", self.caminho)
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True

    @staticmethod
    def vista_topo_thumb_parque(self, context):
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = False
        camera_iso()
        angulo_camera(0, 0, 0, -150)
        enquadrar_camera()
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista(bpy.context.scene.cena.modelo_item, caminho_base())

    @staticmethod
    def vista_topo_lista_confirmacao(self, context):
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = False
        camera_iso()
        angulo_camera(0, 0, 0, -150)
        enquadrar_camera()
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista(bpy.context.scene.cena.modelo, self.caminho)

    @staticmethod
    def iso_frontal(self, context):
        camera_iso()
        angulo_camera(0.78, 0, 0.78, 0)
        enquadrar_camera()
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista("iso_frontal", self.caminho)

    @staticmethod
    def iso_frontal_modelos(self, context):
        if bpy.context.window_manager.obj_category == "COMPONENTES":
            camera_micro()
        else:
            camera_persp()
        angulo_camera(1.5, 0, 0.6, 0)
        enquadrar_camera()
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista_modelos(bpy.context.scene.cena.modelo_item, caminho_base())

        # AJUSTAR PARAMETROS GLOBAIS - REDUNDANCIA CASO UTILIZE O MODO MICRO
        bpy.context.scene.unit_settings.length_unit = "METERS"
        bpy.data.cameras["camera"].clip_start = 0.10

    @staticmethod
    def iso_posterior(self, context):
        camera_iso()
        angulo_camera(0.78, 0, 2.7, 0)
        enquadrar_camera()
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista("iso_posterior", self.caminho)

    @staticmethod
    def completo(self, context):
        try:
            if bpy.context.scene.cena.nome_vistas != "":
                self.criar_circulacao(self, context)
                self.vista_topo(self, context)
                bpy.data.collections["GERAR_VISTAS"].hide_viewport = True
                self.iso_frontal(self, context)
                self.iso_posterior(self, context)
                self.iso_conica(self, context)
                self.report({"INFO"}, "Imagens salvas na pasta do modelo.")
        except Exception:
            self.report({"ERROR"}, "Adicone um nome ao Modelo")

    @staticmethod
    def iso_conica(self, context):
        camera_persp()
        angulo_camera(1.5, 0, 0.6, 0)
        enquadrar_camera()
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista("iso_conica", self.caminho)

    @staticmethod
    def iso_custom(self, context):
        camera_persp()
        bpy.ops.view3d.camera_to_view()
        enquadrar_camera()
        # render_metadados(bpy.context.scene.cena.gerar_metadados)
        salvar_vista(f"iso_custom_{secrets.randbits(5)}", self.caminho)

    @staticmethod
    def iso_conica_subprocess(self, context):
        enquadrar_camera_subprocess()
        camera_persp()
        angulo_camera(1.5, 0, 0.6, 0)
        salvar_vista("iso_conica_subprocess", self.caminho)

    @staticmethod
    def incorporar_imagens(self, context):
        incorporar_imagens_catalogo()

    @staticmethod
    def imagens_batch(self, context):
        bpy.ops.scene.subprocess(action="IMAGE")

    @staticmethod
    def insert_imagens_banco(self, context):
        bpy.context.scene.eevee.use_gtao = True

        dir_base = ""
        try:
            dir_base = bpy.path.abspath(bpy.context.blend_data.filepath).split(
                bpy.path.basename(bpy.context.blend_data.filepath)
            )[0]
        except Exception:
            if dir_base == "":
                dir_base = f"{caminhos_pastas()[0]}"

            elif not os.path.exists(
                f"{dir_base}{bpy.path.basename(bpy.context.blend_data.filepath).split('.')[0]}"
            ):
                os.makedirs(
                    f"{dir_base}{bpy.path.basename(bpy.context.blend_data.filepath).split('.')[0]}"
                )
        camera_iso()
        angulo_camera(0.78, 0, 0.78, 0)
        enquadrar_camera()

        salvar_vista(
            "-iso_frontal",
            f"{dir_base}{bpy.path.basename(bpy.context.blend_data.filepath).split('.')[0]}",
        )

        bpy.data.collections["GERAR_VISTAS"].hide_viewport = False
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = False
        camera_iso()
        angulo_camera(0, 0, 0, 0)
        enquadrar_camera_topo()

        salvar_vista(
            "-vista_topo",
            f"{dir_base}{bpy.path.basename(bpy.context.blend_data.filepath).split('.')[0]}",
        )

    @staticmethod
    def gerar_360(self, context):
        from bpy_plus.collections import Collections

        Collections.set_active(name="Scene Collection")

        bpy.ops.object.empty_add(
            type="SPHERE",
            radius=4.0,
            align="WORLD",
            location=(0.0, 0.0, 2),
            rotation=(0.0, 0.0, 0.0),
            scale=(0.0, 0.0, 0.0),
        )

        bpy.ops.object.camera_add(
            enter_editmode=False,
            align="WORLD",
            location=(0, -6, 2),
            rotation=(1.570796, 0.0, 0.0),
            scale=(0.0, 0.0, 0.0),
        )
        # Get the active scene
        scene = bpy.context.scene

        # Get the Scene Collection
        scene_collection = scene.collection

        # Get all objects in the Scene Collection
        objects_in_collection = [
            obj for obj in scene_collection.objects if obj.type == "EMPTY"
        ]

        # Print the names of empty objects in the Scene Collection
        for obj in objects_in_collection:
            print(obj.name)
            bpy.data.objects[obj.name].name = "guia_360"

        # troca o nome dos texto adicionado por escalaX e escalaY
        for obj in bpy.data.objects:
            if obj.name.startswith("Camera"):
                bpy.data.objects[obj.name].name = "camera_360"
            if obj.name.startswith("Empty"):
                pass
                # bpy.data.objects[obj.name].name = "guia_360"

        for cam in bpy.data.cameras:
            if cam.name.startswith("Camera"):
                bpy.data.cameras[cam.name].name = "camera_360"

        # Get the child and parent objects
        for cam in bpy.data.objects:
            if cam.name.startswith("camera_360"):
                child_obj = bpy.data.objects[cam.name]
            if cam.name.startswith("guia_360"):
                parent_obj = bpy.data.objects[cam.name]

        # Set the parent of the child object
        child_obj.parent = parent_obj
        #        child_obj.parent_type = "VERTEX"
        child_obj.parent_type = "OBJECT"
        # Keep the transform of the child object
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()

        # Update the Outliner to reflect the change
        bpy.context.view_layer.update()

        area = next(area for area in bpy.context.screen.areas if area.type == "VIEW_3D")
        area.spaces[0].region_3d.view_perspective = "CAMERA"
        if (
            bpy.data.scenes[bpy.context.scene.cena.usuarios_pm].camera
            != bpy.data.objects["camera_360"]
        ):
            bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].camera = bpy.data.objects["camera_360"]
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.overlay.show_overlays = False
        bpy.data.scenes[bpy.context.scene.cena.usuarios_pm].eevee.use_gtao = True
        bpy.data.scenes[bpy.context.scene.cena.usuarios_pm].eevee.use_ssr = True

    @staticmethod
    def upload_sharepoint(self, context):
        """FUNÇÃO PARA SALVAR AS IMAGENS DIRETAMENTE NA PASTA TEMP DO PLAYMAKER"""
        bpy.context.scene.eevee.use_gtao = True
        bpy.data.collections["GERAR_VISTAS"].hide_viewport = False
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = False
        nome_pasta_parque = f"{str(bpy.context.scene.cena.pedido)}_{str(bpy.context.scene.cena.modelo)}_P{str(bpy.context.scene.cena.parte)}_V{str(bpy.context.scene.cena.versao)}"
        path_temp = os.path.join(Path.blender(), "temp")

        if Path.temp() == "":
            os.mkdir(path_temp)

        camera_iso()
        angulo_camera(0.78, 0, 0.78, 0)
        enquadrar_camera()

        bpy.data.collections["GERAR_VISTAS"].hide_viewport = True
        bpy.data.objects["LIMITES_PARQUES"].hide_viewport = True

        salvar_vista_temp(
            "img1",
            f"{path_temp}\\{nome_pasta_parque}",
        )
        camera_iso()
        angulo_camera(0, 0, 0, 0)
        enquadrar_camera_topo()
        salvar_vista_temp(
            "img2",
            f"{path_temp}\\{nome_pasta_parque}",
        )


class PLAYMAKER_OT_gerar_360(Operator):
    bl_idname = "playmaker.gerar_360"
    bl_label = "GERAR 360"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        area = next(area for area in bpy.context.screen.areas if area.type == "VIEW_3D")
        area.spaces[0].region_3d.view_perspective = "CAMERA"
        if (
            bpy.data.scenes[bpy.context.scene.cena.usuarios_pm].camera
            != bpy.data.objects["camera_360"]
        ):
            bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].camera = bpy.data.objects["camera_360"]
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.overlay.show_overlays = False
        for ang in range(0, 7):
            bpy.data.scenes[
                bpy.context.scene.cena.usuarios_pm
            ].gerar_vistas.rotacao = ang
            salvar_vista_360(f"iso_360_{secrets.randbits(10)}", "")
        return {"FINISHED"}


class PLAYMAKER_PT_gerar_vistas(Panel):
    bl_idname = "PLAYMAKER_PT_gerar_vistas"
    bl_label = "GERAR VISTAS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CRIAR PARQUES"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 1

    estado = 0

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="RESTRICT_RENDER_OFF")

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        rt = context.scene.cena

        # layout.prop(rt, "modelo")
        layout.prop(rt, "nome_vistas")

        if rt.nome_vistas == "":
            layout.label(text="Preencha o campo 'MODELO'")

        else:
            row = layout.row()
            row.operator(
                "scene.criar_vistas", text="Ajustar Area Circulacao"
            ).action = "criar_circulacao"
            row = layout.row()
            layout.prop(
                bpy.context.scene, "ocultar", text="Ocultar Gerar Vistas", toggle=True
            )
            row1 = layout.row()
            row1.operator("scene.criar_vistas", text="TOPO").action = "vista_topo"
            row1.operator("scene.criar_vistas", text="FRONTAL").action = "iso_frontal"

            row2 = layout.row()
            row2.operator(
                "scene.criar_vistas", text="TRASEIRA"
            ).action = "iso_posterior"
            row2.operator(
                "scene.criar_vistas", text="PERSPECTIVA"
            ).action = "iso_conica"

            row3 = layout.row()
            row3.prop(bpy.context.scene.cena, "gerar_metadados", text="Gerar Metadados")
            row3.prop(bpy.context.scene, "esconder_sapatas", text="Sapatas")

            if self.estado == 0:
                row1.enabled = False
                row2.enabled = False
                row3.enabled = False
            else:
                row1.enabled = True
                row2.enabled = True
                row3.enabled = True


print("@Gerar_Vistas")

classes = (
    PLAYMAKER_PT_gerar_vistas,
    PLAYMAKER_OT_criar_vistas,
    PLAYMAKER_PG_gerar_vistas,
    PLAYMAKER_OT_gerar_360,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.gerar_vistas = bpy.props.PointerProperty(
        type=PLAYMAKER_PG_gerar_vistas
    )
    bpy.types.Scene.esconder_sapatas = bpy.props.BoolProperty(
        update=update_esconder_sapatas
    )


def unregister():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


if __name__ == "__main__":
    register()
