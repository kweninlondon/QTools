import bpy
import re
from collections import Counter

def extract_base_index(name, default_index=None):
    """ Extracts the base name and index from a given name. """
    print(f"🔍 Analyzing name: {name}")

    cleaned_name = re.sub(r"(_SRT|_CST|_[\d._]*)$", "", name)
    isolated_letters = re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", cleaned_name)

    if isolated_letters:
        index = next((letter for letter in isolated_letters if letter.isupper()), isolated_letters[-1])
        base = cleaned_name.rsplit(f"_{index}", 1)[0]
        print(f"✅ Extracted Base: '{base}', Index: '{index}'")
        return base, index

    print(f"❌ No valid index found. Defaulting to full name: '{name}'")
    return name, default_index  # Return full name if no valid index is found

def find_potential_asset_names(obj):
    """ Finds possible asset names from collections and hierarchy. """
    asset_names = []
    print(f"\n🔎 Searching asset names for '{obj.name}'...")

    # Check the object's collections (IGNORE "Scene Collection")
    for col in obj.users_collection:
        if col.name == "Scene Collection":
            print(f"🚫 Ignoring Scene Collection")
            continue
        print(f"📂 Checking Collection: {col.name}")
        base, index = extract_base_index(col.name)
        if base and index:
            asset_names.append((base, index))

    # Check the object's parent hierarchy
    current = obj
    while current:
        print(f"🔗 Checking Parent: {current.name}")
        base, index = extract_base_index(current.name)
        if base and index:
            asset_names.append((base, index))
        current = current.parent

    print(f"🔍 Found potential names: {asset_names if asset_names else 'None'}")
    return asset_names

def determine_asset_name(obj):
    """ Determines the asset name based on the most common base and index. """
    asset_names = find_potential_asset_names(obj)

    if not asset_names:
        print(f"❌ No common asset name found for '{obj.name}'!")
        return None  # No asset name found

    base_counts = Counter(base for base, index in asset_names)
    index_counts = Counter(index for base, index in asset_names)

    most_common_base, _ = base_counts.most_common(1)[0]
    most_common_index, _ = index_counts.most_common(1)[0]

    asset_name = f"{most_common_base}_{most_common_index}"
    print(f"✅ Most common asset name determined: '{asset_name}'")
    return asset_name  # Format: Base_Index

class AssetNamePopup(bpy.types.Operator):
    """ Popup to enter an asset name manually (ensures input before proceeding) """
    bl_idname = "object.asset_name_popup"
    bl_label = "Enter Asset Name"

    asset_name: bpy.props.StringProperty(name="Asset Name")

    def execute(self, context):
        context.scene.asset_name = self.asset_name
        print(f"📝 User entered asset name: '{self.asset_name}'")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def get_or_prompt_asset_name(obj):
    """ Gets the asset name, or prompts user if not found """
    print(f"\n🚀 Determining asset name for '{obj.name}'...")
    asset_name = determine_asset_name(obj)

    if asset_name:
        print(f"✅ Final asset name: '{asset_name}'")
        return asset_name

    print("⚠️ No asset name found! Requesting user input...")

    def store_name_callback():
        new_name = bpy.context.scene.get("asset_name", None)
        if new_name:
            print(f"✅ User confirmed asset name: '{new_name}'")
            bpy.types.Scene.asset_name_callback = new_name  # Store the name globally
            return None  # Stop the timer
        return 0.1  # Keep checking every 0.1 sec

    # Open the popup and wait for input before continuing
    bpy.ops.object.asset_name_popup('INVOKE_DEFAULT')
    bpy.app.timers.register(store_name_callback)

    return bpy.types.Scene.asset_name_callback  # This ensures we use the correct name

def ensure_object_in_correct_collection(obj, asset_name):
    """ Ensures the object is in a collection named after the asset, renaming or creating one if needed. """

    valid_collections = [col for col in obj.users_collection if col.name != "Scene Collection"]

    if valid_collections:
        # If object is already in a collection, rename it
        collection = valid_collections[0]  # Choose first valid collection
        if collection.name != asset_name:
            print(f"✏️ Renaming collection '{collection.name}' → '{asset_name}'")
            collection.name = asset_name
    else:
        # If object has no collection, create one
        print(f"📁 Creating new collection '{asset_name}' and assigning '{obj.name}' to it.")
        new_collection = bpy.data.collections.new(asset_name)
        bpy.context.scene.collection.children.link(new_collection)  # Add to scene
        new_collection.objects.link(obj)  # Link object to new collection

        # Remove object from the original "Scene Collection"
        bpy.context.scene.collection.objects.unlink(obj)

# Register classes
def register():
    bpy.utils.register_class(AssetNamePopup)
    bpy.types.Scene.asset_name = bpy.props.StringProperty(name="Asset Name")
    bpy.types.Scene.asset_name_callback = None  # To store the value after popup

def unregister():
    bpy.utils.unregister_class(AssetNamePopup)
    del bpy.types.Scene.asset_name
    del bpy.types.Scene.asset_name_callback

if __name__ == "__main__":
    register()

    # Example usage: Get asset name and ensure correct collection
    obj = bpy.context.active_object
    if obj:
        asset_name = get_or_prompt_asset_name(obj)
        if asset_name:
            ensure_object_in_correct_collection(obj, asset_name)
        print(f"\n🎯 FINAL RESULT: Asset Name → {asset_name}")
