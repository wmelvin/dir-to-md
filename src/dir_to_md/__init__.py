import argparse
import sys
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Generate a Markdown listing of a directory.")
    parser.add_argument("dir_name", help="Directory to scan")
    args = parser.parse_args()

    dir_path = Path(args.dir_name)

    if not dir_path.exists():
        print(f"Error: '{dir_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{dir_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Get sorted list of files (no recursion)
    files = sorted([f for f in dir_path.iterdir() if f.is_file()], key=lambda x: x.name)

    # Generate Markdown content
    lines = []
    lines.append(f"# {dir_path.name}")
    lines.append("")
    lines.append("## Contents")
    lines.append("")

    for f in files:
        # Create anchor link based on example: File1.ext -> #file1ext
        # Removing dots and lowercasing.
        anchor = f.name.lower().replace('.', '').replace(' ', '-')
        lines.append(f"* [{f.name}](#{anchor})")

    lines.append("")

    for f in files:
        lines.append(f"### {f.name}")
        lines.append("")

    output_filename = f"dir-to-md-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
