import bpy

# List of asset names
asset_names = [
    "Basket_A", "Basket_B", "Basket_C", "Sword_A", "Sword_B",
    "Parasol_A", "Parasol_B", "Palanquin_A", "Palanquin_B",
    "Palanquin_C", "Palamquin_D", "Flag_A", "Flag_B", "Flag_D",
    "Flag_E", "Flag_F", "Spear_A", "Trumpet_A", "Trumpet_B",
    "Drum_A", "Symales_A", "Bow_A", "Stick_A"
]

# Function to create collection and an empty inside it
def create_collection_with_empty(asset_name):
    # Collection name
    collection_name = asset_name
    empty_name = f"{asset_name}_SRT"

    # Create new collection
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    else:
        new_collection = bpy.data.collections[collection_name]

    # Create Empty
    empty = bpy.data.objects.new(empty_name, None)
    empty.empty_display_type = 'PLAIN_AXES'

    # Link Empty to collection
    new_collection.objects.link(empty)

    # Set empty as active object (optional)
    bpy.context.view_layer.objects.active = empty

# Loop through asset names and create collections with empties
for asset in asset_names:
    create_collection_with_empty(asset)

print("Collections and empties created successfully.")
