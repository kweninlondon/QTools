import bpy

# Get all selected objects that are empties and end with "_SRT"
selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'EMPTY' and obj.name.endswith("_SRT")]

if not selected_objects:
    print("No valid '_SRT' empties selected.")
else:
    for selected_obj in selected_objects:
        # Extract asset name (remove "_SRT" from the name)
        asset_name = selected_obj.name[:-4]  # Removes "_SRT"

        # Duplicate the selected empty
        new_empty = selected_obj.copy()
        new_empty.data = None  # Ensure it's a fresh empty object
        new_empty.name = f"{asset_name}_CST"  # Set the new name

        # Link the new empty to the same collections as the original
        for collection in selected_obj.users_collection:
            collection.objects.link(new_empty)

        # Adjust the empty display size (90% of original)
        new_empty.empty_display_size = selected_obj.empty_display_size * 0.9

        # Parent the original empty (_SRT) to the new empty (_CST)
        selected_obj.parent = new_empty

        print(f"Created {new_empty.name} in the same collection as {selected_obj.name}, adjusted its size, and parented {selected_obj.name} to it.")

print("Process completed for all selected '_SRT' empties.")
