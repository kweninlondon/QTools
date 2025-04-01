import bpy

# Make sure the parent "ORIGINALS" collection exists and is linked to the scene
originals_name = "ORIGINALS"
scene_col = bpy.context.scene.collection

# Create or get ORIGINALS
if originals_name not in bpy.data.collections:
    originals = bpy.data.collections.new(originals_name)
    scene_col.children.link(originals)
else:
    originals = bpy.data.collections[originals_name]
    if originals.name not in scene_col.children:
        scene_col.children.link(originals)

# List of subcollection names
subcollections = [
    "Character_I", "Character_J",
    "Rider_A", "Rider_B", "Rider_C", "Rider_D", "Rider_E", "Rider_F",
    "Character_Basket_A", "Character_Basket_B", "Character_Basket_C",
    "RiderMusic_A", "RiderMusic_B", "RiderMusic_C", "RiderMusic_D",
    "Rider_G", "Rider_H", "Rider_I", "Rider_J", "Rider_L", "Rider_K",
    "Character_Parasol_A", "Character_Parasol_B",
    "Group_O", "Group_R_01", "Group_R_02", "Group_R_03", "Group_V", "Group_X"
]

# Create/link subcollections
for name in subcollections:
    if name not in bpy.data.collections:
        subcol = bpy.data.collections.new(name)
        originals.children.link(subcol)
    else:
        subcol = bpy.data.collections[name]
        if subcol.name not in originals.children:
            originals.children.link(subcol)

    # Make sure each subcollection is visible in the view layer
    if subcol.name not in scene_col.children and subcol.name != originals.name:
        scene_col.children.link(subcol)

# Clean up duplicates: unlink subcollections from the Scene Collection if also under ORIGINALS
for col in originals.children:
    if col.name in scene_col.children and col.name != originals.name:
        scene_col.children.unlink(col)
        print(f"Unlinked {col.name} from Scene Collection")

print("All collections are now visible in the View Layer.")