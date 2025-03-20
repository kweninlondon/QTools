def move_objects_in_grid(padding=1):
    """Arranges objects into a grid layout using a structured step-by-step approach."""
    objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not objects:
        print("No objects selected.")
        return

    print(f"Total objects: {len(objects)}")

    # First, arrange objects in a line
    move_objects_side_by_side(padding)

    # Step 1: Get total line length
    total_length = max(obj.location.x + max((obj.matrix_world @ mathutils.Vector(corner)).x for corner in obj.bound_box)
                       for obj in objects)

    # Step 2: Determine grid width (divide total length by 4)
    grid_width = total_length / 4
    print(f"Calculated Grid Width: {grid_width}")

    # Step 3: Get bounding box height of the full line
    min_z = min(min((obj.matrix_world @ mathutils.Vector(corner)).z for corner in obj.bound_box) for obj in objects)
    max_z = max(max((obj.matrix_world @ mathutils.Vector(corner)).z for corner in obj.bound_box) for obj in objects)
    line_height = max_z - min_z
    print(f"Calculated Line Height: {line_height}")

    current_z_offset = 0  # Track the Z level for stacking

    while True:
        # Step 4: Select objects beyond the grid width on X-axis
        objects_to_move = [obj for obj in objects if obj.location.x > grid_width]

        if not objects_to_move:
            break  # Exit when no more objects exceed the grid width

        print(f"Moving {len(objects_to_move)} objects to new row at Z offset: {current_z_offset + line_height + padding}")

        # Step 5: Move selected objects upward in Z
        for obj in objects_to_move:
            obj.location.z += line_height + padding

        # Step 6: Align objects' left edge with X origin
        min_x = min(obj.location.x for obj in objects_to_move)
        for obj in objects_to_move:
            obj.location.x -= min_x  # Align to X=0

        # Update Z offset for the next row
        current_z_offset += line_height + padding

move_objects_in_grid()
