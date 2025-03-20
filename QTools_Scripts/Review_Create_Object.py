import bpy
import mathutils
def apply_modifiers(obj):
    """ Apply all modifiers of a given object """
    if obj.modifiers:
        for mod in obj.modifiers:
            try:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                print(f"Could not apply modifier {mod.name} on {obj.name}: {e}")

def get_object_width(obj):
    """Calculate the width of an object using its bounding box"""
    if obj is None or obj.type != 'MESH':
        return 0  # Return 0 if object is not valid

    # Ensure object has evaluated mesh data
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)

    # Get the world-space bounding box
    bbox_corners = [obj_eval.matrix_world @ mathutils.Vector(corner) for corner in obj_eval.bound_box]

    # Get min/max X values
    min_x = min(corner.x for corner in bbox_corners)
    max_x = max(corner.x for corner in bbox_corners)

    width = max_x - min_x
    return width

def process_selected_mesh():
    # Ensure at least one object is selected
    if not bpy.context.selected_objects:
        print("No objects selected")
        return

    # Duplicate selected objects
    bpy.ops.object.duplicate()
    duplicated_objects = bpy.context.selected_objects

    # Ensure active object is set before switching mode
    if not duplicated_objects:
        print("Duplication failed or no objects duplicated")
        return

    bpy.context.view_layer.objects.active = duplicated_objects[0]  # Set active object

    # Ensure we are in Object Mode
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Apply modifiers and convert to mesh
    for obj in duplicated_objects:
        bpy.context.view_layer.objects.active = obj
        apply_modifiers(obj)  # Apply all modifiers before conversion
        bpy.ops.object.convert(target='MESH')

    # Join all duplicated meshes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in duplicated_objects:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = duplicated_objects[0]
    bpy.ops.object.join()

    merged_mesh = bpy.context.active_object
    if not merged_mesh:
        print("❌ Merging failed")
        return

    # Set transform properties
    width = get_object_width(merged_mesh)
    merged_mesh.location.x = width*1.1
    merged_mesh.rotation_euler.z = -45 * (3.14159 / 180)  # Convert degrees to radians

    # Rename merged mesh based on first two characters of original name
    original_name = duplicated_objects[0].name
    new_name_prefix = original_name[:2]
    merged_mesh.name = f"{new_name_prefix}_Merged_45Degrees"

    # Duplicate and modify new meshes
    bpy.ops.object.duplicate()
    merged_02 = bpy.context.active_object
    merged_02.location.x = width*2*1.1
    merged_02.rotation_euler.z = -90 * (3.14159 / 180)
    merged_02.name = f"{new_name_prefix}_Merged_Side"

    bpy.ops.object.duplicate()
    merged_03 = bpy.context.active_object
    merged_03.location.x = width*3*1.1
    merged_03.rotation_euler.z = -180 * (3.14159 / 180)
    merged_03.name = f"{new_name_prefix}_Merged_Back"

    print("Process completed successfully.")

# Run the function
process_selected_mesh()
