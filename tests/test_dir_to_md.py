import sys
import pytest
from dir_to_md import main


def test_help_short(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["dir-to-md", "-h"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "usage:" in captured.out


def test_help_long(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["dir-to-md", "--help"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "usage:" in captured.out


def test_empty_directory(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(sys, "argv", ["dir-to-md", str(tmp_path)])
    monkeypatch.chdir(tmp_path)

    main()

    captured = capsys.readouterr()
    assert "No files found" in captured.out

    # Should not produce a document
    md_files = list(tmp_path.glob("dir-to-md-*.md"))
    assert len(md_files) == 0


def test_directory_with_files(monkeypatch, capsys, tmp_path):
    files_dir = tmp_path / "files"
    files_dir.mkdir()
    (files_dir / "test-1.txt").touch()
    (files_dir / "test-2.txt").touch()
    (files_dir / "test-3.txt").touch()

    monkeypatch.setattr(sys, "argv", ["dir-to-md", str(files_dir)])
    monkeypatch.chdir(tmp_path)

    main()

    md_files = list(tmp_path.glob("dir-to-md-*.md"))
    assert len(md_files) == 1

    content = md_files[0].read_text(encoding="utf-8")
    assert "test-1.txt" in content
    assert "test-2.txt" in content
    assert "test-3.txt" in content


def test_output_filename(monkeypatch, capsys, tmp_path):
    files_dir = tmp_path / "files"
    files_dir.mkdir()
    (files_dir / "test.txt").touch()

    monkeypatch.setattr(sys, "argv", ["dir-to-md", str(files_dir), "-o", "output.md"])
    monkeypatch.chdir(tmp_path)

    main()

    assert (tmp_path / "output.md").exists()


def test_output_path(monkeypatch, capsys, tmp_path):
    files_dir = tmp_path / "files"
    files_dir.mkdir()
    (files_dir / "test.txt").touch()

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    output_file = out_dir / "output.md"

    monkeypatch.setattr(
        sys, "argv", ["dir-to-md", str(files_dir), "-o", str(output_file)]
    )
    monkeypatch.chdir(tmp_path)

    main()

    assert output_file.exists()


def test_output_path_missing_parent(monkeypatch, capsys, tmp_path):
    files_dir = tmp_path / "files"
    files_dir.mkdir()
    (files_dir / "test.txt").touch()

    output_file = tmp_path / "missing" / "output.md"

    monkeypatch.setattr(
        sys, "argv", ["dir-to-md", str(files_dir), "-o", str(output_file)]
    )
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "Parent directory" in captured.err
    assert "does not exist" in captured.err


def test_overwrite_fail(monkeypatch, capsys, tmp_path):
    files_dir = tmp_path / "files"
    files_dir.mkdir()
    (files_dir / "test.txt").touch()

    output_file = tmp_path / "output.md"
    output_file.touch()

    monkeypatch.setattr(
        sys, "argv", ["dir-to-md", str(files_dir), "-o", str(output_file)]
    )
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit):
        main()

    captured = capsys.readouterr()
    assert "already exists" in captured.err


def test_overwrite_force(monkeypatch, capsys, tmp_path):
    files_dir = tmp_path / "files"
    files_dir.mkdir()
    (files_dir / "test.txt").touch()

    output_file = tmp_path / "output.md"
    output_file.write_text("old content")

    monkeypatch.setattr(
        sys, "argv", ["dir-to-md", str(files_dir), "-o", str(output_file), "-f"]
    )
    monkeypatch.chdir(tmp_path)

    main()

    assert output_file.read_text(encoding="utf-8") != "old content"


def test_version(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["dir-to-md", "--version"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    # argparse prints version to stdout
    assert "dir-to-md" in captured.out
