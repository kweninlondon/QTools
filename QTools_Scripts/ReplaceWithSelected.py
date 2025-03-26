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

    for obj in others:
        # Create new instance of inst_obj's data
        if inst_obj.instance_type == 'COLLECTION':
            new_inst = bpy.data.objects.new(name=inst_obj.name + "_instance", object_data=None)
            new_inst.instance_type = 'COLLECTION'
            new_inst.instance_collection = inst_obj.instance_collection
        else:
            new_inst = bpy.data.objects.new(name=inst_obj.name + "_instance", object_data=inst_obj.data)
        bpy.context.collection.objects.link(new_inst)

        # Match transform
        new_inst.matrix_world = obj.matrix_world

        # Move old object to backup
        for col in obj.users_collection:
            col.objects.unlink(obj)
        backup_col.objects.link(obj)

    print("Replacement complete.")

# Call the function
replace_with_selected_instance()
