import bpy
import os

# Collect all texture file paths
texture_paths = set()

for image in bpy.data.images:
    if image.filepath:
        texture_paths.add(image.filepath)

# Print results
for path in texture_paths:
    texture_status = "✅ Exists" if os.path.exists(bpy.path.abspath(path)) else "❌ Missing"
    print(f"{texture_status} {path}")

# Collect missing texture names
missing_names = []
for path in texture_paths:
    absolute_path = bpy.path.abspath(path) if path else None
    if not absolute_path or not os.path.exists(absolute_path):
        missing_names.append(os.path.basename(path))

if missing_names:
    print("\nMissing Textures:")
    for name in missing_names:
        print(f"🖼️  {name}")
else:
    print("\nNo missing textures found.")
