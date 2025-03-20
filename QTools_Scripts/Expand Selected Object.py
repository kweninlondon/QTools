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

            # Calculate object dimensions in world space
            x_min = min(corner.x for corner in bbox_corners)
            x_max = max(corner.x for corner in bbox_corners)
            y_min = min(corner.y for corner in bbox_corners)
            y_max = max(corner.y for corner in bbox_corners)

            width_x = x_max - x_min  # Width along X
            depth_y = y_max - y_min  # Depth along Y

            # If the Y dimension is larger, rotate 90 degrees around Z
            if depth_y > width_x:
                obj.rotation_euler.z += math.radians(90)

def move_objects_side_by_side(padding=1):
    objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not objects:
        return

    # Move objects to ground and rotate them for correct alignment first
    move_objects_to_ground()
    rotate_object_for_largest_side()

    # Ensure transformations are applied before sorting
    bpy.context.view_layer.update()

    # Sort objects by their current X position after processing
    objects.sort(key=lambda obj: obj.location.x)

    current_x = 0  # Start position on X-axis

    for obj in objects:
        # Refresh object bounding box after transformations
        bpy.context.view_layer.update()
        world_matrix = obj.matrix_world
        bbox_corners = [world_matrix @ mathutils.Vector(corner) for corner in obj.bound_box]

        # Get object width from transformed bounding box
        x_min = min(corner.x for corner in bbox_corners)
        x_max = max(corner.x for corner in bbox_corners)
        width = x_max - x_min

        # Get object center on Y-axis
        y_min = min(corner.y for corner in bbox_corners)
        y_max = max(corner.y for corner in bbox_corners)
        bbox_center_y = (y_max + y_min) / 2

        # Align object X position
        bbox_center_x = (x_max + x_min) / 2
        obj.location.x = current_x + (width / 2) - bbox_center_x

        # Align object Y position to the center (Y=0)
        obj.location.y += -bbox_center_y

        # Update position for next object
        current_x += width + padding

move_objects_side_by_side()

import math

def estimate_grid_size(total_length, row_height):
    """Estimates an optimal grid width using both line length and row height."""
    estimated_size = math.sqrt(total_length * row_height)  # Balance width and height
    print(f"Estimated Grid Width: {estimated_size}")
    return estimated_size

def move_objects_in_grid(padding=1):
    """Arranges objects into a square-like grid layout after they are aligned in a row."""
    objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not objects:
        return

    # Step 1: Get total length of the line layout
    x_min = min(min((obj.matrix_world @ mathutils.Vector(corner)).x for corner in obj.bound_box) for obj in objects)
    x_max = max(max((obj.matrix_world @ mathutils.Vector(corner)).x for corner in obj.bound_box) for obj in objects)
    total_length = x_max - x_min  # Correct total length
    print(f"Corrected Total Line Length: {total_length} meters")

    # Step 2: Get bounding box height of the first row
    min_z = min(min((obj.matrix_world @ mathutils.Vector(corner)).z for corner in obj.bound_box) for obj in objects)
    max_z = max(max((obj.matrix_world @ mathutils.Vector(corner)).z for corner in obj.bound_box) for obj in objects)
    row_height = max_z - min_z
    print(f"Calculated Row Height: {row_height}")

    # Step 3: Estimate grid width using new function
    grid_width = estimate_grid_size(total_length, row_height)

    current_z_offset = 0  # Track the Z level for stacking

    while True:
        # Step 4: Select objects beyond the grid width on X-axis
        objects_to_move = [obj for obj in objects if obj.location.x > grid_width]

        if not objects_to_move:
            break  # Exit when no more objects exceed the grid width

        print(f"Moving {len(objects_to_move)} objects to new row at Z offset: {current_z_offset + row_height + padding}")

        # Step 5: Move selected objects upward in Z
        for obj in objects_to_move:
            obj.location.z += row_height + padding

        # Step 6: Align objects' left edge with X origin
        min_x = min(obj.location.x for obj in objects_to_move)
        for obj in objects_to_move:
            obj.location.x -= min_x  # Align to X=0

        # Update Z offset for the next row
        current_z_offset += row_height + padding

move_objects_in_grid()
