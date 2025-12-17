# devnotes - dir-to-md

Create a Python program that writes a directory listing to a Markdown file.

Try 'Gemini 3 Pro (Preview)' via GitHub Copilot in VSCode.

## Log

### 2025-12-16

#### Create project

I created the initial project structure in a working directory.

    uv init dir-to-md

    cd dir-to-md
    
#### Prompt 1

Modify `main.py` to make a Python program that writes a directory listing to a Markdown file.

Use `argparse` to get one command line argument that specifies directory to scan, `dir_name`.

Use `pathlib.Path` to get `dir_path` from `args.dir_name`.

Exit with an error message if `dir_path` does not exist.

Exit with an error message if `dir_path` is not a directory.

Iterate over the files in the directory to write a listing of files to a Markdown document.

Only list files in the specified directory, do not recurse subdirectories.

The list of files should be sorted.

The document has a Contents section that is a list of file names as section links.

The document has a Files section that lists each file name (only the name) as a level-3 heading.

The markdown file layout is like the following example:

```
# {directory name}

## Contents

* [File1.ext](#file1ext)
* [File2.ext](#file2ext)
* [File3.ext](#file3ext)

### File1.ext

### File2.ext

### File3.ext
```

The document should be saved as `f"dir-to-md-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"` in the current directory.

---

#### Notes

I should have used `uv init --package dir-to-md`.

[Creating projects | uv](https://docs.astral.sh/uv/concepts/projects/init/#packaged-applications)

I'll ask to fix that.

#### Prompt 2

Modify the project tree from the current flat structure to a packaged application structure that uses a `src` directory.
The code in `main.py` should move to `src/dir_to_md/__init__.py`.

---

#### Prompt 3

Change the `build-backend` in `pyproject.toml` to use `uv_build`.

#### Results

This almost worked. I had to change the requires line.

    requires = ["uv_build>=0.9.16,<0.10.0"]

---

#### Prompt 4

Create a `tests` directory.
Create these tests to run using pytest:
1. Short help: Passing `-h` results in the help/usage message.
2. Long help: Passing `--help` results in the help/usage message.
3. Process an empty directory
    - Use `tmp_path` with no files.
    - Should result in 'No files found' message.
    - Should not produce a document.
4. Process a directory with test files.
    - Use `tmp_path / "files"` as the directory to scan.
    - Create three test files like `test-?.txt` in the directory.
    - Should produce a Markdown document in the current directory.
    - The document should contain the file names.
    - Do not remove the document file at end of test.

#### Results

I removed unused `from pathlib import Path` in test file.

Also added Ruff for dev.

    uv add --dev ruff

---

#### Prompt 5

Add a command line argument for specifying the output file using the `-o` and `--output` options.
The argument can be just the file name, or a full path for the file.
If the argument is only a file name then the file should be created in the current working directory.
If the argument includes a path then the parent directory must exist, otherwise exit with an error message.
By default, an existing file should not be overwritten.

Add another argument to allow overwriting an existing output file using the force option as `-f` or `--force`.

Add tests to cover these new options.

---

#### Prompt 6

Include the version number in the help/usage message. The version should be the same as in the `pyproject.toml` file.

---

### 2025-12-17

#### Prompt 7

Make the sorting of file names case insensitive. Also bump the version to `0.1.1`.

