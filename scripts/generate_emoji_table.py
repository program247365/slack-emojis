#!/usr/bin/env python3
"""
Generate emoji table for README.md
Scans the emojis directory and creates a markdown table with name and emoji image.
"""
import os
import hashlib
from pathlib import Path


def check_for_duplicate_images():
    """
    Check for duplicate images in the emojis directory using MD5 hashing.
    Returns True if no duplicates found, False if duplicates exist.
    """
    root_dir = Path(__file__).parent.parent
    emojis_dir = root_dir / "emojis"

    if not emojis_dir.exists():
        print("Error: emojis directory not found")
        return False

    # Get all emoji files, excluding hidden files
    emoji_files = [f for f in emojis_dir.iterdir() if f.is_file() and f.name != '.DS_Store' and not f.name.startswith('.')]

    if not emoji_files:
        return True

    # Dictionary to store: {hash: [list of files with that hash]}
    hash_map = {}

    # Calculate MD5 hash for each file
    for emoji_file in emoji_files:
        md5_hash = hashlib.md5()

        # Read file in chunks for memory efficiency (though not critical for small emoji files)
        with open(emoji_file, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5_hash.update(chunk)

        file_hash = md5_hash.hexdigest()

        # Add file to hash map
        if file_hash not in hash_map:
            hash_map[file_hash] = []
        hash_map[file_hash].append(emoji_file.name)

    # Check for duplicates
    duplicates_found = False
    for file_hash, files in hash_map.items():
        if len(files) > 1:
            if not duplicates_found:
                print("❌ Duplicate images detected!")
                duplicates_found = True
            print(f"   Hash {file_hash[:8]}... has {len(files)} copies:")
            for filename in files:
                print(f"     - {filename}")

    if duplicates_found:
        print("\n⚠️  Please remove duplicate images before committing.")
        return False

    return True


def generate_emoji_table():
    """Generate a markdown table of all emojis in the emojis directory."""
    # Get the root directory (parent of scripts)
    root_dir = Path(__file__).parent.parent
    emojis_dir = root_dir / "emojis"

    if not emojis_dir.exists():
        print("Error: emojis directory not found")
        return ""

    # Get all files in emojis directory, excluding .DS_Store and hidden files
    emoji_files = sorted([f for f in emojis_dir.iterdir() if f.is_file() and f.name != '.DS_Store' and not f.name.startswith('.')])

    if not emoji_files:
        return ""

    # Start building the table
    table = "\n## Emoji Collection\n\n"
    table += "| Name | Emoji |\n"
    table += "|------|-------|\n"

    for emoji_file in emoji_files:
        # Get the name without extension
        name = emoji_file.stem
        # Format name for display with backticks to prevent GitHub emoji rendering
        display_name = f"`:{name}:`"
        # Create relative path for markdown
        emoji_path = f"emojis/{emoji_file.name}"
        # Add row to table with HTML img tag for consistent sizing
        table += f'| {display_name} | <img src="{emoji_path}" alt="{name}" width="64"> |\n'

    return table


def update_readme():
    """Update README.md with the generated emoji table."""
    # First check for duplicate images
    if not check_for_duplicate_images():
        return False

    root_dir = Path(__file__).parent.parent
    readme_path = root_dir / "README.md"
    emojis_dir = root_dir / "emojis"

    if not readme_path.exists():
        print("Error: README.md not found")
        return False

    # Count emoji files, excluding .DS_Store and hidden files
    emoji_count = len([f for f in emojis_dir.iterdir() if f.is_file() and f.name != '.DS_Store' and not f.name.startswith('.')])

    # Read current README
    with open(readme_path, 'r') as f:
        content = f.read()

    # Generate the new table
    new_table = generate_emoji_table()

    # Check if table already exists
    table_marker = "## Emoji Collection"

    if table_marker in content:
        # Replace existing table
        # Find the start of the table section
        start_idx = content.find(table_marker)
        # Find the next section (if any) or end of file
        # Look for next ## heading or end of file
        next_section_idx = content.find("\n##", start_idx + len(table_marker))

        if next_section_idx == -1:
            # No next section, replace to end of file
            new_content = content[:start_idx] + new_table
        else:
            # Replace up to next section
            new_content = content[:start_idx] + new_table + "\n" + content[next_section_idx:]
    else:
        # Append table to end of README
        new_content = content.rstrip() + "\n" + new_table

    # Write updated README
    with open(readme_path, 'w') as f:
        f.write(new_content)

    # Verify the table was generated correctly
    table_row_count = new_table.count("| `:")

    if table_row_count != emoji_count:
        print(f"⚠️  Warning: Mismatch detected!")
        print(f"   Emoji files in directory: {emoji_count}")
        print(f"   Emoji rows in table: {table_row_count}")
        print(f"   Difference: {emoji_count - table_row_count} emojis missing from table")
        return False

    print(f"✓ Updated README.md with {emoji_count} emojis")
    print(f"✓ Verified: All {emoji_count} emojis are in the table")
    return True


if __name__ == "__main__":
    import sys
    result = update_readme()
    if result is False:
        sys.exit(1)
