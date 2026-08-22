import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "assets" / "merge_text.py"


def run_merge(tmp_path, payload, *extra):
    src = tmp_path / "transcript.json"
    dst = tmp_path / "merged.txt"
    src.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--src", str(src), "--dst", str(dst), *extra],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    ), dst


def test_merge_rejects_malformed_segment_without_traceback(tmp_path):
    result, _ = run_merge(tmp_path, {"segments": [{"text": "缺时间"}]})
    assert result.returncode == 2
    assert "segment" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()


def test_merge_rejects_negative_gap(tmp_path):
    result, _ = run_merge(tmp_path, {"segments": []}, "--gap", "-1")
    assert result.returncode == 2
    assert "gap" in result.stderr.lower()


def test_merge_preserves_word_boundary_between_segments(tmp_path):
    result, dst = run_merge(tmp_path, {"segments": [
        {"start": 0, "end": 1, "text": "Run"},
        {"start": 1.2, "end": 2, "text": "way"},
    ]})
    assert result.returncode == 0, result.stderr
    assert "Run way" in dst.read_text(encoding="utf-8")
