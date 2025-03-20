import bpy

# Collect all texture file paths
texture_paths = set()

for image in bpy.data.images:
    if image.filepath:
        texture_paths.add(image.filepath)

# Print results
for path in texture_paths:
    print(path)
