import bpy
import os

# Dictionary to store unique images by filename
unique_images = {}

# Iterate through all images in Blender
for image in bpy.data.images:
    if image.filepath:
        filename = os.path.basename(bpy.path.abspath(image.filepath))

        # If this texture has already been encountered, replace duplicates
        if filename in unique_images:
            print(f"🔄 Replacing duplicate: {filename}")

            # Replace texture in all materials
            for mat in bpy.data.materials:
                if mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image == image:
                            node.image = unique_images[filename]  # Replace with shared image
        else:
            unique_images[filename] = image  # Store as unique

print("✅ All duplicate textures have been linked!")