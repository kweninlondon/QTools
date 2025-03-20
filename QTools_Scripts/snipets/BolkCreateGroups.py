import bpy
import time  # Optional delay to prevent lag

# Define the collection name
collection_name = "Group_"
asset_drops = [
    (20, "Character_I"),
    (6, "Character_J"),
    (2, "Character_G"),
]

uids = {
    "Character_I": 42,
    "Character_J": 236,
    "Character_G": 391
}
# Function to get or create a collection
def get_or_create_collection(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    else:
        new_collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_collection)
        return new_collection

# Get or create the target collection
target_collection = get_or_create_collection(collection_name)

# Define the asset drop list: (quantity, session_uid)

# Fixed parameters for asset dropping
align = 'WORLD'
location = (0, 0, 0)
scale = (1, 1, 1)
drop_x = 1034
drop_y = 1794

# Loop through each (quantity, session_uid) pair
for quantity, session_uid in asset_drops:
    session_uid = uids[session_uid]
    for i in range(quantity):
        # Get a set of objects before dropping
        existing_objects = set(bpy.data.objects)

        # Drop the asset
        bpy.ops.object.collection_external_asset_drop(
            session_uid=session_uid,
            align=align,
            location=location,
            scale=scale,
            drop_x=drop_x,
            drop_y=drop_y
        )

        # Allow Blender to process the dropped asset
        bpy.context.view_layer.update()
        time.sleep(0.1)  # Short delay to prevent reference loss

        # Find the new objects that were added
        new_objects = set(bpy.data.objects) - existing_objects

        for obj in new_objects:
            if obj:
                # Store asset name before overriding
                asset_name = obj.name

                # Move the asset to the target collection
                if obj.name not in target_collection.objects:
                    target_collection.objects.link(obj)
                # Remove from the default scene collection
                bpy.context.scene.collection.objects.unlink(obj)

                # Apply Library Override
                if obj.override_library is None:  # Check if it's already overridden
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.make_override_library()

# ✅ **Mark the collection as an asset**
if target_collection:
    target_collection.asset_mark()
    print(f"Collection '{collection_name}' is now marked as an asset.")

print(f"All assets moved to collection '{collection_name}', overridden, and marked as an asset.")
