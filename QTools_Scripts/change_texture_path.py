import bpy
import os

def change_texture_paths():
    """Update only missing image texture paths to a new folder."""
    new_texture_folder = globals().get("new_texture_folder", None)
    broken_only = False
    if not new_texture_folder:
        print("❌ No texture path provided!")
        return

    new_texture_folder = bpy.path.abspath(new_texture_folder)  # Ensure absolute path
    print(f"🔹 Checking for missing textures and updating paths to: {new_texture_folder}")

    updated = False  # Track if any textures were updated

    for image in bpy.data.images:
        if image.filepath:
            abs_path = bpy.path.abspath(image.filepath)  # Get absolute path
            if  broken_only:
                print(f"Updating only broken paths")
                if not os.path.exists(abs_path):  # Only update if missing
                    old_name = os.path.basename(abs_path)  # Get the filename
                    new_path = os.path.join(new_texture_folder, old_name)

                    if os.path.exists(new_path):  # Ensure new file exists
                        image.filepath = new_path
                        image.reload()
                        updated = True
                        print(f"✅ Fixed Missing Texture: {old_name} -> {new_path}")
                    else:
                        print(f"⚠️ Still Missing: {old_name} (Tried: {new_path})")
            else:
                print(f"Updating all paths")
                old_name = os.path.basename(abs_path)  # Get the filename
                new_path = os.path.join(new_texture_folder, old_name)

                if os.path.exists(new_path):  # Ensure new file exists
                    image.filepath = new_path
                    image.reload()
                    updated = True
                    print(f"✅ Fixed Missing Texture: {old_name} -> {new_path}")
                else:
                    print(f"⚠️ Still Missing: {old_name} (Tried: {new_path})")

    if updated:
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Force UI refresh
        print("🔄 Blender Viewport Updated!")

    print("🎉 Texture paths checked and missing ones were fixed!")

change_texture_paths()
