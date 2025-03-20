import bpy
import math
import mathutils


def move_objects_to_ground(obj):
    """Moves an object so its lowest bounding box point aligns with Z=0."""
    world_matrix = obj.matrix_world
    bbox_corners = [world_matrix @ mathutils.Vector(corner) for corner in obj.bound_box]
    min_z = min(corner.z for corner in bbox_corners)
    obj.location.z += -min_z


def rotate_object_for_largest_side(obj):
    """Rotates the object so its longest side aligns with the X-axis."""
    world_matrix = obj.matrix_world
    bbox_corners = [world_matrix @ mathutils.Vector(corner) for corner in obj.bound_box]

    # Calculate dimensions
    x_min = min(corner.x for corner in bbox_corners)
    x_max = max(corner.x for corner in bbox_corners)
    y_min = min(corner.y for corner in bbox_corners)
    y_max = max(corner.y for corner in bbox_corners)

    width_x = x_max - x_min
    depth_y = y_max - y_min

    # If the Y dimension is larger, rotate 90 degrees around Z
    if depth_y > width_x:
        obj.rotation_euler.z += math.radians(90)


def move_objects_side_by_side(padding=1):  # Default padding value of 0.1 units
    objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not objects:
        return

    # Move objects to ground and rotate them for correct alignment
    for obj in objects:
        move_objects_to_ground(obj)
        rotate_object_for_largest_side(obj)

    # Sort objects by their current X position
    objects.sort(key=lambda obj: obj.location.x)

    current_x = 0  # Start position on X-axis

    for obj in objects:
        # Get bounding box in world space (considering rotation)
        world_matrix = obj.matrix_world
        bbox_corners = [world_matrix @ mathutils.Vector(corner) for corner in obj.bound_box]

        # Get object width from transformed bounding box
        x_min = min(corner.x for corner in bbox_corners)
        x_max = max(corner.x for corner in bbox_corners)
        width = x_max - x_min

        # Align based on bounding box instead of object origin
        bbox_center_x = (x_max + x_min) / 2
        obj.location.x += -bbox_center_x + current_x + (width / 2)

        # Update position for next object with padding
        current_x += width + padding

move_objects_side_by_side()