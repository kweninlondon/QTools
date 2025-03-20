import bpy
import re

# Get all empties in the scene
empties = [obj for obj in bpy.data.objects if obj.type == 'EMPTY']

for empty in empties:
    if not empty.children:
        continue  # Skip empties with no children

    children = list(empty.children)  # Convert to list to avoid reference issues
    mesh_children = [child for child in children if child.type == 'MESH']

    # Clean up the collection name
    collection_name = empty.name
    collection_name = re.sub(r'KB3D_SHG_', '', collection_name)  # Remove "KB3D_SHG_"
    collection_name = re.sub(r'_grp$', '', collection_name)  # Remove "_grp" at the end

    # Move empty to world origin (0,0,0) without affecting children
    for child in children:
        child.matrix_world = empty.matrix_world @ child.matrix_local

    empty.location = (0, 0, 0)

    if len(mesh_children) == 1:  # If there's only one mesh child, leave it in the scene collection
        obj = mesh_children[0]
        if obj.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(obj)  # Move object to scene collection
        print(f"Kept single mesh {obj.name} in scene collection.")
    else:  # If multiple children, create a collection
        if collection_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(new_collection)
        else:
            new_collection = bpy.data.collections[collection_name]

        # Move children into the new collection
        for child in children:
            if child.name not in new_collection.objects:
                new_collection.objects.link(child)
            bpy.context.scene.collection.objects.unlink(child)

        print(f"Moved objects to collection: {collection_name}")

    # Delete the empty
    bpy.data.objects.remove(empty)

print("All empties processed successfully with cleaned collection names!")