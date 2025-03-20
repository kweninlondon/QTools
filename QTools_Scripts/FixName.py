import bpy
import re
from collections import Counter

import re

import re

import re

def extract_base_index(name, default_index=None):  # Default index if none found
    print(f"🔍 Extracting base and index from {name}...")

    # Remove known suffixes (_SRT, _CST, numbers, etc.)
    cleaned_name = re.sub(r"(_SRT|_CST|_[\d._]*)$", "", name)

    # Find all isolated single letters (not next to another letter)
    isolated_letters = re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", cleaned_name)

    if isolated_letters:
        # Prioritize capitalized letters if present
        index = next((letter for letter in isolated_letters if letter.isupper()), isolated_letters[-1])

        # Extract base (everything before the index)
        base = cleaned_name.rsplit(f"_{index}", 1)[0]
        print(f"✅ Found Base: {base}, Index: {index}")
        return base, index

    print(f"❌ No valid index found. Using default: {default_index}")
    return name, default_index  # Return full name as base if no valid index is found

# Function to find all potential asset names in hierarchy and collections
def find_potential_asset_names(obj):
    asset_names = []

    # 1️⃣ Check the object's **own** collections
    for col in obj.users_collection:
        base, index = extract_base_index(col.name)
        if base and index:
            asset_names.append((base, index))

    # 2️⃣ Check the object's parent hierarchy
    current = obj
    while current:
        base, index = extract_base_index(current.name)
        if base and index:
            asset_names.append((base, index))
        current = current.parent

    return asset_names

# Function to determine the correct asset name based on frequency
def determine_asset_name(obj):
    asset_names = find_potential_asset_names(obj)

    if not asset_names:
        print(f"❌ Couldn't determine asset name for {obj.name}")
        return None

    # Count occurrences of bases and indices separately
    base_counts = Counter(base for base, index in asset_names)
    index_counts = Counter(index for base, index in asset_names)

    # Get the most common base and index
    most_common_base, _ = base_counts.most_common(1)[0]
    most_common_index, _ = index_counts.most_common(1)[0]

    return f"{most_common_base}_{most_common_index}"  # Returns [Base]_[Index]

# Function to rename the parent collection (and ensure all objects in it match)
def rename_parent_collection(obj, asset_name):
    for col in obj.users_collection:
        if col.name != asset_name:
            print(f"✅ Renaming collection: {col.name} → {asset_name}")
            col.name = asset_name
        # Recursively rename all objects inside the collection
        for child in col.objects:
            rename_object(child, asset_name)


def get_asset_variant(asset_name, obj_name):
    base, index = extract_base_index(asset_name)  # Get correct base & index from asset_name
    print(f"🔍 Extracting variant from {obj_name}, based on expected {base}_{index}")

    # Remove base & index from the object name to isolate the variant
    stripped_name = obj_name.replace(base, "").replace(f"_{index}", "").strip("_")

    variant = stripped_name if stripped_name else ""  # Assign variant if something remains

    print(f"✅ Found Variant: {variant if variant else 'None'}")
    return variant

def get_asset_name_with_variant(obj, asset_name):
    base, index = extract_base_index(asset_name)  # Get the correct base & index from asset_name
    print(f"🔍 Looking for a variant in {obj.name} based on expected {base}_{index}")

    # Extract the variant by comparing obj.name against asset_name
    variant = get_asset_variant(asset_name, obj.name)

    # Ensure the variant is **only before the index** and does not interfere with suffixes
    if variant and f"_{index}" in obj.name:
        variant = obj.name.split(f"_{index}")[0].replace(base, "").strip("_")

    print(f"🔍 Found Variant: {variant if variant else 'None'}")

    # Construct the corrected name while preserving suffixes
    corrected_name = f"{base}_{variant}_{index}" if variant else f"{base}_{index}"

    print(f"✅ Corrected Name: {corrected_name}")
    return corrected_name

    # Return unchanged if it's already correct
    return asset_name

# Function to rename a single object based on type
def rename_object(obj, asset_name):
    asset_name_with_variant = get_asset_name_with_variant(obj, asset_name)
    if obj.type == 'MESH':
        obj.name = asset_name_with_variant
        if hasattr(obj, "data") and obj.data:
            obj.data.name = f"{asset_name_with_variant}_MSH"

    elif obj.type == 'EMPTY':
        if "_CST" in obj.name:
            obj.name = f"{asset_name_with_variant}_CST"
        else:
            obj.name = f"{asset_name_with_variant}_SRT"

# Main function to rename all objects inside their asset hierarchy
def rename_selection():
    for obj in bpy.context.selected_objects:
        print(f"🔍 Debug: Processing '{obj.name}' of type '{obj.type}'")

        asset_name = determine_asset_name(obj)

        if not asset_name:
            continue  # Skip if no valid name was found

        # Rename the entire hierarchy, including the collection
        rename_parent_collection(obj, asset_name)

print("🚀 Running hierarchy-based renaming...")
rename_selection()
print("✅ Renaming complete!")
