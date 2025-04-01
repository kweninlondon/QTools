import bpy

# Get all selected objects in the viewport
selected_objects = bpy.context.selected_objects

if not selected_objects:
    print("No objects selected.")
else:
    print(f"Making {len(selected_objects)} selected objects local...")

    for obj in selected_objects:
        if obj.library is not None:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.make_local(type='ALL')

    print("Done making objects local.")