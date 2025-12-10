#!/usr/bin/env python3
"""
Generate emoji table for README.md
Scans the emojis directory and creates a markdown table with name and emoji image.
"""
import os
from pathlib import Path


def generate_emoji_table():
    """Generate a markdown table of all emojis in the emojis directory."""
    # Get the root directory (parent of scripts)
    root_dir = Path(__file__).parent.parent
    emojis_dir = root_dir / "emojis"

    if not emojis_dir.exists():
        print("Error: emojis directory not found")
        return ""

    # Get all files in emojis directory
    emoji_files = sorted([f for f in emojis_dir.iterdir() if f.is_file()])

    if not emoji_files:
        return ""

    # Start building the table
    table = "\n## Emoji Collection\n\n"
    table += "| Name | Emoji |\n"
    table += "|------|-------|\n"

    for emoji_file in emoji_files:
        # Get the name without extension
        name = emoji_file.stem
        # Format name for display (replace dashes/underscores with spaces)
        display_name = f":{name}:"
        # Create relative path for markdown
        emoji_path = f"emojis/{emoji_file.name}"
        # Add row to table
        table += f"| {display_name} | ![{name}]({emoji_path}) |\n"

    return table


def update_readme():
    """Update README.md with the generated emoji table."""
    root_dir = Path(__file__).parent.parent
    readme_path = root_dir / "README.md"
    emojis_dir = root_dir / "emojis"

    if not readme_path.exists():
        print("Error: README.md not found")
        return

    # Count emoji files
    emoji_count = len([f for f in emojis_dir.iterdir() if f.is_file()])

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

    print(f"✓ Updated README.md with {emoji_count} emojis")


if __name__ == "__main__":
    update_readme()
