import bpy
import os
import sys

def change_texture_paths(new_texture_folder):
    """Update only missing image texture paths to a new folder."""
    if not new_texture_folder:
        print("❌ No texture path provided!")
        sys.stdout.flush()
        return

    new_texture_folder = bpy.path.abspath(new_texture_folder)  # Ensure absolute path
    print(f"🔹 Checking for missing textures and updating paths to: {new_texture_folder}")
    sys.stdout.flush()

    updated = False  # Track if any textures were updated
    broken_only = True
    for image in bpy.data.images:
        if image.filepath:
            abs_path = bpy.path.abspath(image.filepath)  # Get absolute path
            if  broken_only:
                print(f"Updating only broken paths")
                sys.stdout.flush()
                if not os.path.exists(abs_path) or not image.has_data:  # Also check if Blender failed to load the texture
                    old_name = os.path.basename(abs_path)  # Get the filename
                    new_path = os.path.join(new_texture_folder, old_name)

                    if os.path.exists(new_path):  # Ensure new file exists
                        image.filepath = new_path
                        image.reload()
                        updated = True
                        print(f"✅ Fixed Missing Texture: {old_name} -> {new_path}")
                        sys.stdout.flush()
                    else:
                        print(f"⚠️ Still Missing: {old_name} (Tried: {new_path})")
                        sys.stdout.flush()
            else:
                print(f"Updating all paths")
                sys.stdout.flush()
                old_name = os.path.basename(abs_path)  # Get the filename
                new_path = os.path.join(new_texture_folder, old_name)

                if os.path.exists(new_path):  # Ensure new file exists
                    image.filepath = new_path
                    image.reload()
                    updated = True
                    print(f"✅ Fixed Missing Texture: {old_name} -> {new_path}")
                    sys.stdout.flush()
                else:
                    print(f"⚠️ Still Missing: {old_name} (Tried: {new_path})")
                    sys.stdout.flush()

    if updated:
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Force UI refresh
        print("🔄 Blender Viewport Updated!")
        sys.stdout.flush()

    print("🎉 Texture paths checked and missing ones were fixed!")
    sys.stdout.flush()

if __name__ == "__main__":
    print("🔍 Running change_texture_path.py")  # Debug print
    sys.stdout.flush()

    if "new_texture_folder" in globals():
        print(f"📂 Received texture path: {new_texture_folder}")  # Debug print
        sys.stdout.flush()
        change_texture_paths(new_texture_folder)
    else:
        print("❌ No texture path argument provided!")
        sys.stdout.flush()
