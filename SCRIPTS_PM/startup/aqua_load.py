import os

import bpy
from bpy.app.handlers import persistent
from mathutils import Color

# def TrocaUsuarioPadrao(self, context, *args, **kwargs):
#     pm_readme = os.path.join(os.path.expanduser("~"), "pm_readme.txt")
#     try:
#         with open(pm_readme) as f:
#             user = f.readline()
#         if bpy.data.is_saved:
#             bpy.context.scene.cena.usuarios = user.split(";")[0]
#         else:
#             print(f"Olá, {user.split(';')[1]}")

#             with open(
#                 f"{caminhos_pastas()[9]}\\usuarios_pm.json", "r"
#             ) as json_usuarios:
#                 json_usuarios_lista = json.load(json_usuarios)

#             if not bpy.data.is_saved:
#                 bpy.context.scene.cena.funcoes_usuarios = user.split(";")[0]
#                 bpy.context.scene.cena.usuarios_pm = user.split(";")[1]
#             else:
#                 for key, values in json_usuarios_lista.items():
#                     if key == bpy.context.scene.name:
#                         bpy.context.scene.cena.funcoes_usuarios = values
#                         bpy.context.scene.cena.usuarios_pm = bpy.context.scene.name
#         update_workspace(self, context)
#     except Exception as erro:
#         print(erro)
#         self.report({"ERROR"}, "Não é possível validar. Favor checar .csv base.")


# def LimpezaDeBlendsDuplicados(self, context, *args, **kwargs):
#     diretorio = f"{caminhos_pastas()[0]}"
#     dir_base = f"{caminhos_pastas()[10]}\\FLUXO"

#     # The above code is searching for files in two directories (`dir_base` and `dir`) and creating a list
#     # of files with extensions that are considered safe (`extensoes_seguras`). It then adds the full
#     # path of the remaining unsafe files to a list called `ls_excluir`. Finally, it loops through the `ls_excluir`
#     # list and removes each file from the system and prints the name of the deleted file. However, the
#     # code is currently commented out, so the files are not actually being deleted.
#     ls_excluir = []
#     extensoes_seguras = [
#         ".blend",
#         ".png",
#         ".banco",
#         ".tag",
#         ".txt",
#         ".CSV",
#         ".csv",
#         ".py",
#         ".pdf",
#         ".jpg",
#         ".png",
#         ".lnk",
#         ".docx",
#         ".rar",
#         ".webp",
#         ".svg",
#         ".rar",
#         ".xlsx",
#         ".xls",
#         ".PDF",
#         ".pptx",
#     ]
#     ls_excluir = [
#         (os.path.join(root, f))
#         for root, dirs, files in os.walk(diretorio)
#         for f in files
#         if os.path.splitext(f)[1] not in extensoes_seguras
#     ]
#     ls_excluir_ = [
#         (os.path.join(root, f))
#         for root, dirs, files in os.walk(dir_base)
#         for f in files
#         if os.path.splitext(f)[1] not in extensoes_seguras
#     ]

#     for i in ls_excluir:
#         arquivos_excluidos = {i.split("\\")[-1]}
#         os.remove(i)
#         print(f"{arquivos_excluidos} excluido")

#     for i in ls_excluir_:
#         arquivos_excluidos = {i.split("\\")[-1]}
#         os.remove(i)
#         print(f"{arquivos_excluidos} excluidos")

# def menu_override_draw_func(self, context):
#     layout = self.layout
#     obj = context.object
#     aqua = obj.aqua if hasattr(obj, "aqua") else None
#     if bpy.context.object.select_get():
#         layout.label(text=f"Nome: {aqua.nome}")
#         layout.label(text=f"Codigo: {str(aqua.codigo)}")
#         layout.label(text=f"Peso: {aqua.peso} kg")
#         if obj.aqua.fixo:
#             layout.label(text=f"Altura Fixa em {round(obj.location.z, 2)} Mts")
#         layout.prop(aqua, "derivacao", text="")
#         if obj.aqua.codigo == "40410001":
#             layout.prop(obj, '["COLUNA_CUSTOM"]')
#         layout.separator()

#         layout.prop(context.scene.cena, "ancoragem", expand=False, text="")
#         act_obj = bpy.context.active_object.name_full
#         scale = 0.4
#         for col in bpy.data.objects[act_obj].users_collection:
#             layout.prop(
#                 col.aqua,
#                 "excluir",
#                 toggle=True,
#                 icon="CANCEL",
#                 text="EXCLUIR ITEM",
#             )
#         layout.operator("object.girar_90", icon="ORIENTATION_GIMBAL")
#         layout.operator(
#             "scene.recarregar_dados", icon="FILE_REFRESH"
#         ).action = "carregar_dados_objeto"
#         layout.operator(
#             "admin.admin_op", text="Distribuir Cores", icon="SHADING_RENDERED"
#         ).action = "DISTRIBUIR_CORES"

#         layout.operator(
#             "scene.recarregar_dados", text="Recarregar KIT PF", icon="FILE_REFRESH"
#         ).action = "carregar_dados_kit_pf_objeto"
#         layout.operator("objects.ajustar_colunas", icon="EMPTY_SINGLE_ARROW")

#         layout.separator()
#         if obj.type in {"MESH", "CURVE", "SURFACE"}:
#             layout.operator("object.shade_smooth")
#             layout.operator(
#                 "object.shade_smooth", text="Shade Auto Smooth"
#             ).use_auto_smooth = True
#             layout.operator("object.shade_flat", text="Shade Flat")
#         if obj.type in {
#             "MESH",
#             "CURVE",
#             "SURFACE",
#             "GPENCIL",
#             "LATTICE",
#             "ARMATURE",
#             "META",
#             "FONT",
#         } or (obj.type == "EMPTY" and obj.instance_collection is not None):
#             layout.operator_context = "INVOKE_REGION_WIN"
#             layout.operator_menu_enum(
#                 "object.origin_set", text="Set Origin", property="type"
#             )
#             layout.operator_context = "INVOKE_DEFAULT"
#         layout.menu("VIEW3D_MT_mirror")
#         layout.menu("VIEW3D_MT_snap")
#         layout.menu("VIEW3D_MT_object_parent")
#         layout.operator_context = "INVOKE_REGION_WIN"
#     else:
#         layout.operator("custo.atualizar", icon="FILE_REFRESH")
#         layout.prop(context.scene.cena, "ancoragem", expand=False, text="")
#         act_obj = bpy.context.active_object.name_full
#         scale = 0.4
#         for col in bpy.data.objects[act_obj].users_collection:
#             layout.prop(
#                 col.aqua,
#                 "excluir",
#                 toggle=True,
#                 icon="CANCEL",
#                 text="EXCLUIR ITEM",
#             )
#         layout.operator("object.girar_90")
#         layout.operator(
#             "scene.recarregar_dados", icon="FILE_REFRESH"
#         ).action = "carregar_dados_objeto"
#         layout.operator(
#             "admin.admin_op", text="Distribuir Cores", icon="SHADING_RENDERED"
#         ).action = "DISTRIBUIR_CORES"

# bpy.types.VIEW3D_MT_object_context_menu.draw = menu_override_draw_func
# area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]


# @persistent
# def AttStartup(self, context):
#     """
#     AttStartup Permite Atualizar o Startup

#     Args:
#         context (_type_): _description_
#     """
#     import shutil as sht

#     from bpy_plus.file_system import Path
#     from pm_funcoes import caminhos_pastas

#     startup = "\\3.3\\config\\startup.blend"
#     startup_file = rf"{Path.blender()}{startup}"
#     print(startup_file)
#     startup_base = caminhos_pastas()[1]
#     print(f"{startup_base}\\startup.blend")
#     copiar_startup = sht.copy(f"{startup_base}\\startup.blend", startup_file)


@persistent
def carregar_cores_init(dummy):
    print("@Cores_Carregadas")
    bpy.ops.object.carregar_cores()
    bpy.context.preferences.themes["Default"].view_3d.wire = Color(
        (0.40000003576278687, 0.40000003576278687, 0.40000003576278687)
    )


# class TRANSFORM_PT_panel(Panel):
#     bl_space_type = "PROPERTIES"
#     bl_region_type = "WINDOW"
#     bl_context = "object"
#     bl_label = "Transform"
#     #    bl_space_type = "VIEW_3D"
#     #    bl_region_type = "UI"
#     bl_category = "Item"
#     #    bl_context = "objectmode"

#     def draw(self, context):
#         layout = self.layout
#         layout.use_property_split = True

#         ob = context.object

#         col = layout.column()
#         col.label(text="Location")
#         row = col.row(align=True)
#         row.prop(ob, "location", text="")
#         row.use_property_decorate = False
#         row.prop(ob, "lock_location", text="", emboss=False, icon="DECORATE_UNLOCKED")

#         col.label(text="Rotation")
#         rotation_mode = ob.rotation_mode
#         if rotation_mode == "QUATERNION":
#             col = layout.column()
#             row = col.row(align=True)
#             row.prop(ob, "rotation_quaternion", text="")
#             sub = row.column(align=True)
#             sub.use_property_decorate = False
#             sub.prop(
#                 ob, "lock_rotation_w", text="", emboss=False, icon="DECORATE_UNLOCKED"
#             )
#             sub.prop(
#                 ob, "lock_rotation", text="", emboss=False, icon="DECORATE_UNLOCKED"
#             )
#         elif rotation_mode == "AXIS_ANGLE":
#             col = layout.column()
#             row = col.row(align=True)
#             row.prop(ob, "rotation_axis_angle", text="")

#             sub = row.column(align=True)
#             sub.use_property_decorate = False
#             sub.prop(
#                 ob, "lock_rotation_w", text="", emboss=False, icon="DECORATE_UNLOCKED"
#             )
#             sub.prop(
#                 ob, "lock_rotation", text="", emboss=False, icon="DECORATE_UNLOCKED"
#             )
#         else:
#             col = layout.column()
#             row = col.row(align=True)
#             row.prop(ob, "rotation_euler", text="")
#             row.use_property_decorate = False
#             row.prop(
#                 ob, "lock_rotation", text="", emboss=False, icon="DECORATE_UNLOCKED"
#             )
#             row = layout.row(align=True)
#             row.prop(ob, "rotation_mode", text="Mode")
#             row.label(text="", icon="BLANK1")

#             col = layout.column()
#             col.label(text="Scale")
#             row = col.row(align=True)
#             row.prop(ob, "scale", text="")
#             row.use_property_decorate = False
#             row.prop(ob, "lock_scale", text="", emboss=False, icon="DECORATE_UNLOCKED")

#             col = layout.column()
#             col.label(text="Dimensions")
#             row = col.row(align=True)
#             row.prop(ob, "dimensions", text="")
#             row.use_property_decorate = False
#             # row.prop(ob, "lock_scale", text="", emboss=False, icon='DECORATE_UNLOCKED')


classes = ()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.app.handlers.load_post.append(carregar_cores_init)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
