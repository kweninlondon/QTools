import bpy
import math
import mathutils

def move_objects_to_ground():
    """Moves all selected objects so their lowest bounding box point aligns with Z=0."""
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':  # Ensure it's a mesh object
            world_matrix = obj.matrix_world
            bbox_corners = [world_matrix @ mathutils.Vector(corner) for corner in obj.bound_box]

            # Find the lowest Z coordinate among the bounding box corners
            min_z = min(corner.z for corner in bbox_corners)

            # Move object up so the lowest point is at Z=0
            obj.location.z += -min_z

def rotate_object_for_largest_side():
    """Rotates all selected objects so their longest side aligns with the X-axis."""
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':  # Ensure it's a mesh object
            world_matrix = obj.matrix_world
            bbox_corners = [world_matrix @ mathutils.Vector(corner) for corner in obj.bound_box]

            # Calculate object dimensions
            x_min = min(corner.x for corner in bbox_corners)
            x_max = max(corner.x for corner in bbox_corners)
            y_min = min(corner.y for corner in bbox_corners)
            y_max = max(corner.y for corner in bbox_corners)

            width_x = x_max - x_min  # Width along X
            depth_y = y_max - y_min  # Depth along Y

            # If the Y dimension is larger, rotate 90 degrees around Z
            if depth_y > width_x:
                obj.rotation_euler.z += math.radians(90)

# Run both functions
move_objects_to_ground()
rotate_object_for_largest_side()
print("Objects moved to ground and rotated.")