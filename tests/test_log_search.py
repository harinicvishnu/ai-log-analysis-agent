import tempfile
from pathlib import Path

def search_log(path, keyword):
    matches = []
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        for number, line in enumerate(f, start=1):
            if keyword.casefold() in line.casefold():
                matches.append((number, line.rstrip("\r\n")))
    return matches

def test_case_insensitive_search():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "test.log"
        p.write_text("INFO Started\nERROR Timeout occurred\n", encoding="utf-8")
        result = search_log(p, "timeout")
        assert result == [(2, "ERROR Timeout occurred")]

def test_no_match():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "test.log"
        p.write_text("INFO Started\n", encoding="utf-8")
        assert search_log(p, "database") == []
