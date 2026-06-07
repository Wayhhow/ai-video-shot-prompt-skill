#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 回归测试：3 套提示词模板的输出与 v0.1 baseline 行为对比。

测试策略：
- 3 套模板（single-shot / multi-shot / action-scene）分别跑 validate_prompt.py
- multi-shot / action-scene 跑 --min-chars 200 --max-chars 3000（与 baseline 一致）
- 关键不变量：exit code 0，issues = 0
- 软不变量：3 大段、景别、构图、运镜、参考图、声音、字数 9 大类"通过"项数 >= 7

如果 baseline 文件不存在，所有测试 skip 而非 fail（首次跑或清理后不阻塞）。
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "docs" / "baseline-v0.1.txt"
SCRIPT = ROOT / "scripts" / "validate_prompt.py"
TEMPLATES_DIR = ROOT / "templates"


def _run_validator(extra_args: list, stdin_text: str | None = None):
    """跑 validate_prompt.py 并返回 (returncode, stdout, stderr)。"""
    cmd = [sys.executable, str(SCRIPT.relative_to(ROOT))]
    if stdin_text is None:
        cmd.extend(extra_args)
    else:
        # stdin 模式：args 只有一个 `-`
        cmd.append(extra_args[0] if extra_args else "-")
    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        input=stdin_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode, result.stdout, result.stderr


def _parse_counts(stdout: str) -> dict:
    """从 validate_prompt.py 输出中提取：n_pass / n_warn / n_issues / max_classes。"""
    m_pass = re.search(r"通过:\s*(\d+)\s*项", stdout)
    m_warn = re.search(r"警告:\s*(\d+)\s*项", stdout)
    m_fail = re.search(r"严重:\s*(\d+)\s*项", stdout)
    return {
        "n_pass": int(m_pass.group(1)) if m_pass else 0,
        "n_warn": int(m_warn.group(1)) if m_warn else 0,
        "n_issues": int(m_fail.group(1)) if m_fail else 0,
        "all_pass": "[OK] 提示词结构通过" in stdout,
    }


def _has_marker(stdout: str, marker: str) -> bool:
    return marker in stdout


# ====== pytest fixtures / skip ======

@pytest.fixture(scope="module", autouse=True)
def require_baseline():
    """若 baseline 缺失，全部测试 skip。"""
    if not BASELINE.exists():
        pytest.skip(f"baseline not found: {BASELINE}", allow_module_level=True)


# ====== 3 套模板回归 ======

TEMPLATES = [
    ("single-shot", "templates/single-shot.md", []),
    ("multi-shot", "templates/multi-shot.md", ["--min-chars", "200", "--max-chars", "3000"]),
    ("action-scene", "templates/action-scene.md", ["--min-chars", "200", "--max-chars", "3000"]),
]


@pytest.mark.parametrize("name,path,extra", TEMPLATES)
def test_template_exit_code_zero(name, path, extra):
    """每套模板的 validate_prompt.py 必须以退出码 0 通过。"""
    rc, out, err = _run_validator([path] + extra)
    assert rc == 0, f"{name} validate 失败: exit={rc}\nstdout={out}\nstderr={err}"


@pytest.mark.parametrize("name,path,extra", TEMPLATES)
def test_template_no_issues(name, path, extra):
    """每套模板的严重缺失数 (issues) 必须为 0。"""
    rc, out, err = _run_validator([path] + extra)
    counts = _parse_counts(out)
    assert counts["n_issues"] == 0, f"{name} 有严重缺失: {counts}\n{out}"
    assert counts["all_pass"], f"{name} 未打'提示词结构通过':\n{out}"


@pytest.mark.parametrize("name,path,extra", TEMPLATES)
def test_template_three_sections_present(name, path, extra):
    """3 大段（基础设定 / 氛围画质 / 画面内容）都必须存在。"""
    rc, out, err = _run_validator([path] + extra)
    for section in ["基础设定", "氛围画质", "画面内容"]:
        assert _has_marker(out, f"[OK] {section}: 存在"), f"{name} 缺大节 {section}"


@pytest.mark.parametrize("name,path,extra", TEMPLATES)
def test_template_min_passed_classes(name, path, extra):
    """软不变量：至少 7 类规则 [OK] 通过（防核心退化）。"""
    rc, out, err = _run_validator([path] + extra)
    counts = _parse_counts(out)
    assert counts["n_pass"] >= 7, f"{name} 通过项过少: {counts}\n{out}"


# ====== 红线测试：故意改坏模板应当被检出 ======

def test_red_line_synthetic_prompt_detected():
    """故意造一份完全不合规的提示词，validate_prompt.py 必须 fail。"""
    synthetic = """【画面内容】
- 景别：中景
"""
    # 缺【基础设定】、缺【氛围画质】、缺参考图、字数过少
    rc, out, err = _run_validator(["-"], stdin_text=synthetic)
    counts = _parse_counts(out)
    assert rc != 0, f"应当被检出为不合规：exit={rc}\n{out}"
    assert counts["n_issues"] >= 2, f"严重缺失数应 >= 2: {counts}\n{out}"


# ====== baseline 文件结构完整性 ======

def test_baseline_file_contains_three_reports():
    """baseline 必须含 3 套模板的报告（按顺序）。"""
    text = BASELINE.read_text(encoding="utf-8")
    n_titles = text.count("AI 视频提示词结构自检")
    assert n_titles == 3, f"baseline 应含 3 份报告，实际 {n_titles}"
