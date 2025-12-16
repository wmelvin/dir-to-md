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
