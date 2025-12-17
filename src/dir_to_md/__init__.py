import argparse
import sys
from pathlib import Path
from datetime import datetime
from importlib.metadata import version, PackageNotFoundError


def main():
    try:
        __version__ = version("dir-to-md")
    except PackageNotFoundError:
        __version__ = "unknown"

    parser = argparse.ArgumentParser(
        description="Generate a Markdown listing of a directory."
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("dir_name", help="Directory to scan")
    parser.add_argument("-o", "--output", help="Output file name or path")
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite existing output file"
    )
    args = parser.parse_args()

    dir_path = Path(args.dir_name)

    if not dir_path.exists():
        print(f"Error: '{dir_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{dir_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Get sorted list of files (no recursion)
    files = sorted(
        [f for f in dir_path.iterdir() if f.is_file()], key=lambda x: x.name.lower()
    )

    if not files:
        print("No files found.")
        return

    # Generate Markdown content
    lines = []
    lines.append(f"# {dir_path.name}")
    lines.append("")
    lines.append("## Contents")
    lines.append("")

    for f in files:
        # Create anchor link based on example: File1.ext -> #file1ext
        # Removing dots and lowercasing.
        anchor = f.name.lower().replace(".", "").replace(" ", "-")
        lines.append(f"* [{f.name}](#{anchor})")

    lines.append("")

    for f in files:
        lines.append(f"### {f.name}")
        lines.append("")

    if args.output:
        output_path = Path(args.output)
        # Check if parent directory exists
        # Path('filename').parent is Path('.') which exists.
        # Path('path/to/filename').parent is Path('path/to')
        if not output_path.parent.exists():
            print(
                f"Error: Parent directory '{output_path.parent}' does not exist.",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        output_path = Path(f"dir-to-md-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

    if output_path.exists() and not args.force:
        print(
            f"Error: Output file '{output_path}' already exists. Use -f to overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
