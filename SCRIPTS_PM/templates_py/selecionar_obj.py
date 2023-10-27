def selecionar_objetos_por_nome(obj_name):
    """
    Selects an object in Blender by its name.

    Parameters:
        obj_name (str): The name of the object to be selected.

    Returns:
        None
    """
    bpy.ops.object.select_all(action="DESELECT")  # Deselect all objects
    obj = bpy.data.objects[obj_name]  # Get the object
    obj.select_set(True)  # Select the object
    bpy.context.view_layer.objects.active = obj  # Set the object as active
