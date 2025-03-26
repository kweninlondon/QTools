import bpy

def replace_with_selected_instance():
    selected_objs = bpy.context.selected_objects

    if len(selected_objs) < 2:
        print("Select at least two objects, including one with '_INST' in the name.")
        return

    inst_obj = None
    others = []

    for obj in selected_objs:
        if "_INST" in obj.name:
            inst_obj = obj
        else:
            others.append(obj)

    if not inst_obj:
        print("No object with '_INST' in name found in selection.")
        return

    # Create or get BACKUP collection
    backup_col = bpy.data.collections.get("BACKUP")
    if not backup_col:
        backup_col = bpy.data.collections.new("BACKUP")
        bpy.context.scene.collection.children.link(backup_col)
        for layer in bpy.context.view_layer.layer_collection.children:
            if layer.collection == backup_col:
                layer.exclude = True
                break

    for i, obj in enumerate(others):
        print(f"Replacing '{obj.name}' — type: {obj.type}, instance_type: {obj.instance_type}, is_collection_instance: {obj.instance_type == 'COLLECTION'}")

        # Always create new instance from inst_obj
        base_name = inst_obj.name
        if base_name.endswith("_INST"):
            base_name = base_name[:-5]  # strip "_INST"
        new_name = f"{base_name}_{i:03d}"
        new_inst = bpy.data.objects.new(name=new_name, object_data=None)

        if inst_obj.instance_type == 'COLLECTION':
            new_inst.instance_type = 'COLLECTION'
            new_inst.instance_collection = inst_obj.instance_collection
        else:
            new_inst.data = inst_obj.data

        if obj.users_collection:
            obj.users_collection[0].objects.link(new_inst)
        else:
            bpy.context.scene.collection.objects.link(new_inst)

        # Match transform
        new_inst.matrix_world = obj.matrix_world

        # Move old object to backup
        for col in obj.users_collection:
            col.objects.unlink(obj)
        backup_col.objects.link(obj)

    print("Replacement complete.")

# Call the function
replace_with_selected_instance()
