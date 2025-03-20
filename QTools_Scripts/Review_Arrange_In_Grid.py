import bpy

# User-defined settings
MAX_ROW_WIDTH = 40 / 100  # Maximum row width (converted to meters)
CLEARANCE_Z = 0.002  # Additional space for readability
ALIGN_TO_BOTTOM = True  # If True, creates a duplicate in "Review" collection and adjusts it

def get_object_width(obj):
    """ Returns the bounding box width of an object """
    min_x, max_x = min(v[0] for v in obj.bound_box), max(v[0] for v in obj.bound_box)
    return max_x - min_x

def get_object_height(obj):
    """ Returns the bounding box height of an object """
    min_z, max_z = min(v[2] for v in obj.bound_box), max(v[2] for v in obj.bound_box)
    return max_z - min_z

def get_bottom_offset(obj):
    """ Returns the offset needed to move the object's origin to the bottom of its bounding box """
    min_z = min(v[2] for v in obj.bound_box)  # Lowest Z-point in bounding box
    return -min_z  # Offset needed to align bottom to Z = 0

def duplicate_object_for_review(obj):
    """ Duplicates the object, renames it with '_REVIEW', and moves it to the 'Review' collection """
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()  # Ensure mesh data is copied
    new_obj.name = obj.name + "_REVIEW"

    # Add to the Review collection
    review_collection = bpy.data.collections.get("Review")
    if review_collection is None:
        review_collection = bpy.data.collections.new("Review")
        bpy.context.scene.collection.children.link(review_collection)
    
    review_collection.objects.link(new_obj)

    return new_obj  # Return the duplicated object

def set_origin_to_bottom(obj):
    """ Moves the object's origin to the bottom of its bounding box """
    offset_z = get_bottom_offset(obj)

    # Apply the transformation in Edit Mode
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Move geometry down so that the lowest point aligns with the origin
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, offset_z))
    bpy.ops.object.mode_set(mode='OBJECT')

def arrange_objects_in_grid():
    """ Arranges selected objects in an X-Z grid while handling duplicates for review """
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    selected_objects.sort(key=lambda obj: obj.name.lower())

    if not selected_objects:
        print("No mesh objects selected.")
        return

    start_x = 0  # Starting X position
    start_z = 0  # Starting Z position
    current_x = start_x
    current_z = start_z
    max_row_height = 0

    for obj in selected_objects:
        if ALIGN_TO_BOTTOM:
            # Duplicate the object and work on the duplicate
            obj = duplicate_object_for_review(obj)
            set_origin_to_bottom(obj)

        obj_width = get_object_width(obj)
        obj_height = get_object_height(obj)

        # If adding the object exceeds the max row width, move to the next row (stack on Z)
        if (current_x + obj_width) - start_x > MAX_ROW_WIDTH:
            current_x = start_x
            current_z += max_row_height + 0.05  # Increase row spacing for readability
            max_row_height = obj_height  # Reset row height

        # Move the object to the calculated position
        obj.location.x = current_x + (obj_width / 2)  # Offset by half width
        obj.location.z = current_z

        # Update current X position for the next object
        current_x += obj_width + 0.05  # Add small spacing between objects
        max_row_height = max(max_row_height, obj_height)  # Update row height

    # Enable object name display in the viewport
    for obj in selected_objects:
        obj.show_name = True

    print("Objects arranged successfully in 'Review' collection with corrected pivots.")

# Run the function
arrange_objects_in_grid()