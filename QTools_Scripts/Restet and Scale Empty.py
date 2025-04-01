import bpy

# Loop through selected objects
for obj in bpy.context.selected_objects:
    # Only act on Empties or Collection Instances
    if obj.type == 'EMPTY':
        # Reset transforms
        obj.location = (0, 0, 0)
        obj.rotation_euler = (0, 0, 0)
        obj.scale = (1, 1, 1)

        # Set display settings
        obj.empty_display_type = 'CUBE'  # 'CUBE' = box
        obj.empty_display_size = 0.01

        print(f"Updated empty: {obj.name}")

print("Done updating empties and linked collections.")