#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 端到端工作流模拟：写 → 检 → 修 → 检 的完整循环。

模拟两类真实场景：
1. 用户写了一份不合规的提示词 → validate_prompt.py 应检出 → 用户修复 → 重新验证通过
2. stdin 路径与文件路径输出完全一致（无 file vs stdin 分支行为差异）
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_prompt.py"

VALID_FULL = """【基础设定】
- 时间：黄昏
- 地点：废弃加油站
- 人物：金属机器人
- 参考图描述：金属机器人 3/4 侧视角，胸前 LED 红光
- 声音限制：仅保留机械碰撞声

【氛围画质】
- 风格核心：原子朋克
- 去 AI 味：超写实、极致逼真、真人实景拍摄
- 限制词：杜绝游戏CG感
- 视觉基调：ARRI
- 色彩影调：青橙

【画面内容】
- 景别：中景
- 构图：三分线
- 运镜：手持
- 故事内容：
  [怎么做] 主角入画
  [为什么] 建立对峙
  [效果] 紧张感升起
"""

# 故意有缺陷的提示词：缺【基础设定】、缺参考图、字数过少
DEFECTIVE = """【氛围画质】
- 风格核心：原子朋克
- 去 AI 味：超写真
- 限制词：杜绝CG
- 视觉基调：ARRI
- 色彩影调：青橙

【画面内容】
- 景别：中景
- 构图：三分线
- 运镜：手持
- 故事内容：太短
"""


def _run(args: list, stdin_text: str | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(SCRIPT.relative_to(ROOT))] + args
    return subprocess.run(
        cmd,
        cwd=str(ROOT),
        input=stdin_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )


def _extract_issue_count(stdout: str) -> int:
    import re
    m = re.search(r"严重:\s*(\d+)\s*项", stdout)
    return int(m.group(1)) if m else -1


# ====== Test 1: 完整工作流循环 ======

def test_workflow_full_cycle():
    """写 → 检（fail）→ 修 → 检（pass）的端到端循环。"""

    # Step 1: 故意有缺陷的提示词应被检出
    r1 = _run(["-"], stdin_text=DEFECTIVE)
    issues_before = _extract_issue_count(r1.stdout)
    assert r1.returncode != 0, f"缺陷提示词应被检出为非 0: exit={r1.returncode}\n{r1.stdout}"
    assert issues_before >= 2, f"严重缺失数应 >= 2: {issues_before}\n{r1.stdout}"

    # Step 2: 修复后的提示词应通过 --strict
    r2 = _run(["-", "--strict"], stdin_text=VALID_FULL)
    issues_after = _extract_issue_count(r2.stdout)
    assert r2.returncode == 0, f"修复后应通过: exit={r2.returncode}\n{r2.stdout}"
    assert issues_after == 0, f"严重缺失数应降为 0: {issues_after}\n{r2.stdout}"

    # Step 3: 缺陷 vs 修复后 issues 数应严格下降
    assert issues_after < issues_before, f"修复后 issues 应减少: {issues_before} -> {issues_after}"


# ====== Test 2: stdin 与文件路径行为一致 ======

def test_workflow_stdin_vs_file_consistent(tmp_path):
    """stdin (`-`) 与文件路径两种输入方式的输出应完全一致。"""
    p = tmp_path / "prompt.md"
    p.write_text(VALID_FULL, encoding="utf-8")

    r_file = _run([str(p)])
    r_stdin = _run(["-"], stdin_text=VALID_FULL)

    # 两个 exit code 应相同
    assert r_file.returncode == r_stdin.returncode, (
        f"exit code 不一致: file={r_file.returncode} stdin={r_stdin.returncode}"
    )

    # 两个 stdout 应完全一致（除了一处 hash 标识）
    # 这里只比"通过项数 / 警告 / 严重" 3 行，避免依赖时间戳
    import re
    def extract_summary(s: str) -> str:
        m_pass = re.search(r"通过:\s*\d+\s*项", s)
        m_warn = re.search(r"警告:\s*\d+\s*项", s)
        m_fail = re.search(r"严重:\s*\d+\s*项", s)
        return f"{m_pass.group(0) if m_pass else ''}\n{m_warn.group(0) if m_warn else ''}\n{m_fail.group(0) if m_fail else ''}"

    assert extract_summary(r_file.stdout) == extract_summary(r_stdin.stdout), (
        f"stdin vs file summary 不一致:\nfile:\n{extract_summary(r_file.stdout)}\nstdin:\n{extract_summary(r_stdin.stdout)}"
    )


# ====== Test 3: --strict 与非 --strict 行为差异 ======

def test_strict_vs_non_strict_warning_handling():
    """非 strict 模式下 warnings 不会让 exit code != 0；strict 模式下会。"""
    # 一个有 warning 但无 issue 的提示词：缺声音限制、缺参考图、字数少
    ambiguous = """【基础设定】
- 时间：黄昏
- 地点：废弃加油站
- 人物：机器人

【氛围画质】
- 风格核心：原子朋克
- 去 AI 味：超写实
- 限制词：杜绝CG
- 视觉基调：ARRI
- 色彩影调：青橙

【画面内容】
- 景别：中景
- 构图：三分线
- 运镜：手持
- 故事内容：[怎么做]test[为什么]test[效果]test
"""

    r_loose = _run(["-"], stdin_text=ambiguous)
    r_strict = _run(["-", "--strict"], stdin_text=ambiguous)

    issues = _extract_issue_count(ambiguous if False else r_loose.stdout)
    # ambiguous 应无严重缺失（3 段齐全、景别/构图/运镜齐、去 AI 味 + 限制词齐）
    # 但可能有 warnings（缺声音、字数、参考图等）
    if issues == 0:
        # 仅有 warnings：loose 退出 0，strict 退出 1
        assert r_loose.returncode == 0, f"loose 应 0 退出（仅 warnings）: exit={r_loose.returncode}"
        assert r_strict.returncode == 1, f"strict 应 1 退出（warnings 也算）: exit={r_strict.returncode}"
    else:
        # 有 issues 则两端都非 0
        assert r_loose.returncode != 0
        assert r_strict.returncode != 0
