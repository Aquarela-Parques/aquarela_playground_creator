bl_info = {
    "name": "Area Custom",
    "author": "Igor",
    "version": (1, 0, 0),  # Corrected version format
    "blender": (2, 93, 0),  # Updated Blender version
    "location": "View3d > Tool",
}

import bpy


def update_dim_x(self, context):
    obj = bpy.context.object
    obj.dimensions.x = obj.dimensao_x
    bpy.data.curves["escalaX"].body = str(obj.dimensao_x)[:4] + "m"


def update_dim_y(self, context):
    obj = bpy.context.object
    obj.dimensions.y = obj.dimensao_y
    bpy.data.curves["escalaY"].body = str(obj.dimensao_y)[:4] + "m"


bpy.types.Object.dimensao_x = bpy.props.FloatProperty(
    name="Dimensao X",
    min=1,
    max=100,
    default=1,
    step=25,
    unit="LENGTH",
    precision=3,
    update=update_dim_x,
)
bpy.types.Object.dimensao_y = bpy.props.FloatProperty(
    name="Dimensao Y",
    min=1,
    max=100,
    default=1,
    step=25,
    unit="LENGTH",
    precision=3,
    update=update_dim_y,
)


class EscalaPlano(bpy.types.Operator):
    bl_label = "Escala e Plano"
    bl_idname = "object.scale_plane"  # Changed operator ID name

    def execute(self, context):
        obj = bpy.context.object

        # Insert, name, set the plane to 1x1m, apply the scale, lock position, and Z scale
        mesh = bpy.ops.mesh.primitive_plane_add(
            enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 0)
        )
        scale_obj = context.object
        scale_obj.name = "area_parque"
        scale_obj.data.name = scale_obj.name
        scale_obj.scale[0] = 0.5
        scale_obj.scale[1] = 0.5
        scale_obj.scale[2] = 0
        apply_scale = bpy.ops.object.transform_apply(
            location=True, rotation=True, scale=True
        )
        scale_obj.lock_location[2] = True
        scale_obj.lock_scale[2] = True

        # Change the handler to MOVE for easier plane positioning
        change_handler = bpy.ops.wm.tool_set_by_id(name="builtin.move")

        # Get dimensions X and Y of the plane and convert them to a string
        string_scale1 = str(scale_obj.scale[0])
        string_scale2 = str(scale_obj.scale[1])
        M = "m"
        string_scale11 = string_scale1 + M
        string_scale22 = string_scale2 + M

        bpy.ops.object.text_add(
            enter_editmode=True, location=(-0.5, -0.5, 0), rotation=(0, 0, 0)
        )
        bpy.ops.font.delete(type="PREVIOUS_WORD")
        bpy.ops.font.text_insert(text=string_scale11)
        bpy.ops.object.editmode_toggle()

        bpy.ops.object.text_add(
            enter_editmode=True, location=(-0.6, -0.38, 0), rotation=(0, 0, 1.57)
        )
        bpy.ops.font.delete(type="PREVIOUS_WORD")
        bpy.ops.font.text_insert(text=string_scale22[:4])
        bpy.ops.object.editmode_toggle()

        # Change the names of the added text to "escalaX" and "escalaY"
        bpy.data.objects["Text"].name = "escalaX"
        bpy.data.objects["escalaX"].data.name = "escalaX"

        bpy.data.objects["Text.001"].name = "escalaY"
        bpy.data.objects["escalaY"].data.name = "escalaY"

        area_parque = bpy.data.objects["area_parque"]
        escalaX = bpy.data.objects["escalaX"]
        escalaY = bpy.data.objects["escalaY"]

        # Select the objects escalaX and escalaY for parenting
        bpy.context.view_layer.objects.active = escalaX
        bpy.data.objects["escalaX"].select_set(True)
        bpy.context.view_layer.objects.active = escalaY
        bpy.data.objects["escalaY"].select_set(True)
        bpy.context.view_layer.objects.active = area_parque

        # Lock position to prevent the user from moving the numbers
        bpy.data.objects["escalaX"].lock_location[0] = True
        bpy.data.objects["escalaX"].lock_location[1] = True
        bpy.data.objects["escalaX"].lock_location[2] = True
        bpy.data.objects["escalaX"].lock_rotation[0] = True
        bpy.data.objects["escalaX"].lock_rotation[1] = True
        bpy.data.objects["escalaX"].lock_rotation[2] = True

        bpy.data.objects["escalaY"].lock_location[0] = True
        bpy.data.objects["escalaY"].lock_location[1] = True
        bpy.data.objects["escalaY"].lock_location[2] = True
        bpy.data.objects["escalaY"].lock_rotation[0] = True
        bpy.data.objects["escalaY"].lock_rotation[1] = True
        bpy.data.objects["escalaY"].lock_rotation[2] = True

        # Parent the measurement texts to the plane
        bpy.ops.object.parent_set(type="VERTEX")

        # Create a material for the plane
        material = bpy.data.materials.new(name="CorPlano")
        bpy.data.objects["area_parque"].active_material = bpy.data.materials["CorPlano"]

        return {"FINISHED"}


class CalcArea(bpy.types.Panel):
    bl_label = "Medir Área"
    bl_idname = "CALC_PT_area"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FERRAMENTAS"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        area_parque = bpy.context.scene.objects.get("area_parque")

        if not area_parque:
            row.operator("object.scale_plane", text="Área", icon="MESH_GRID")

        elif bpy.context.object.name.startswith("area_parque"):
            layout.prop(bpy.context.object, "dimensao_y", text="COMPRIMENTO")
            layout.prop(bpy.context.object, "dimensao_x", text="LARGURA")

        else:
            layout.label(text="Selecione a área")


classes = (EscalaPlano, CalcArea)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
