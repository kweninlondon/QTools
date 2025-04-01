import bpy

# Count how many times each mesh is used
mesh_usage = {}

for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.data:
        mesh = obj.data
        mesh_usage[mesh] = mesh_usage.get(mesh, 0) + 1

# Go through again and rename if mesh is local and editable
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        mesh = obj.data

        if mesh.library is not None:
            print(f"Skipping '{mesh.name}' — it's linked.")
            continue  # Can't rename linked mesh data

        if mesh_usage[mesh] > 1:
            # Shared mesh — keep its name and just append _MSH if not already
            base_name = mesh.name.split("_MSH")[0]
            new_name = f"{base_name}_MSH"
        else:
            # Unique mesh — rename based on the object
            new_name = f"{obj.name}_MSH"

        if mesh.name != new_name:
            print(f"Renaming mesh '{mesh.name}' → '{new_name}'")
            mesh.name = new_name

print("Mesh renaming complete.")