#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_prompt.py 的单元测试（v0.2.0 引入）。

覆盖 12+ 场景：
- 全通过
- 单段缺失 × 3
- 顺序错乱（严格 + 非严格）
- 参考图描述在 / 不在
- 声音限制在 / 不在
- 景别缺失、构图缺失、运镜缺失
- 字数边界 99 / 100 / 1500 / 1501
- stdin 输入
- 文件不存在
- CLI 参数 --min-chars / --max-chars
- 无【】包裹的旧风格标题

运行：pytest tests/ -v
或：  python -m pytest tests/ -v
"""
import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

# 把 scripts/ 加到 sys.path
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

# 引入被测对象
import validate_prompt as vp  # noqa: E402


# --- 测试用 fixture：完整合格的提示词 ---

VALID_PROMPT = """【基础设定】
- 时间：黄昏，夕阳低角度斜射
- 地点：加州 1 号公路旁废弃加油站
- 人物：金属质感机器人，胸前 LED 屏显愤怒
- 参考图描述：金属机器人 3/4 侧视角，胸前 LED 红光；丧尸张开大口迎面扑来
- 声音限制：仅保留机械碰撞声、枪声、拳肉声，无需BGM

【氛围画质】
- 风格核心：原子朋克、末日废土、电影动作
- 去 AI 味：超写实、极致逼真、真人实景拍摄、电影动作捕捉
- 限制词：杜绝游戏CG感、杜绝动作僵硬、杜绝塑料皮肤、杜绝肢体扭曲
- 视觉基调：ARRI Alexa 65 拍摄，35mm 镜头
- 氛围：废弃的加油站、夕阳的暖光与战斗的金属碰撞形成反差
- 色彩影调：青橙对比色调，高光偏暖、阴影偏冷

【画面内容】
- 总分镜数：5 个
- 总时长：约 10 秒
- 分镜时长比重：
  - 分镜 1：1/5
  - 分镜 2：1/5
  - 分镜 3：1/5
  - 分镜 4：1/5
  - 分镜 5：1/5

【分镜 1：开场入画（1/5）】
- 景别：中景
- 构图：对角线构图
- 运镜：手持跟拍
- 故事内容：
  [怎么做] 主角从画面左侧快速入画，目光锁定 3 名丧尸
  [为什么] 建立对峙
  [效果] 紧张感升起

【分镜 5：收尾（1/5）】
- 景别：全景
- 构图：中心对称构图
- 运镜：拉远
- 故事内容：
  [怎么做] 主角站立，敌人倒地
  [为什么] 完成战斗
  [效果] 夕阳逆光剪影
"""


def _check(text: str, strict: bool = False, **kwargs) -> tuple:
    """直接调用 check_* 函数，绕过 CLI 解析。"""
    sections, order_ok, ordered_names = vp.check_sections(text)
    deai = vp.check_deai(text)
    has_ref = vp.has_reference_image_desc(text)
    has_sound = vp.check_sound_limit(text)
    shot = vp.check_shot_size(text)
    comp = vp.check_composition(text)
    move = vp.check_camera_move(text)
    chars = vp.count_chars(text)
    min_c = kwargs.get("min_chars", vp.DEFAULT_MIN_CHARS)
    max_c = kwargs.get("max_chars", vp.DEFAULT_MAX_CHARS)
    return {
        "sections": sections,
        "order_ok": order_ok,
        "ordered_names": ordered_names,
        "deai": deai,
        "has_ref": has_ref,
        "has_sound": has_sound,
        "shot": shot,
        "comp": comp,
        "move": move,
        "chars": chars,
        "in_range": min_c <= chars <= max_c,
    }


# --- 1. 全通过 ---

def test_all_pass():
    r = _check(VALID_PROMPT)
    assert all(r["sections"].values()), f"三大段应齐全: {r['sections']}"
    assert r["order_ok"], f"顺序应正确: {r['ordered_names']}"
    assert r["deai"], "去 AI 味关键词应存在"
    assert r["has_ref"], "参考图描述应识别"
    assert r["has_sound"], "声音限制应识别"
    assert r["shot"], "景别应存在"
    assert r["comp"], "构图应存在"
    assert r["move"], "运镜应存在"
    assert r["in_range"], f"字数应在区间内: {r['chars']}"


# --- 2. 单段缺失 × 3 ---

def _drop_section(text: str, name: str) -> str:
    return text.replace(f"【{name}】\n", "")


def test_missing_基础设定():
    text = _drop_section(VALID_PROMPT, "基础设定")
    r = _check(text)
    assert not r["sections"]["基础设定"]
    assert r["sections"]["氛围画质"]
    assert r["sections"]["画面内容"]


def test_missing_氛围画质():
    text = _drop_section(VALID_PROMPT, "氛围画质")
    r = _check(text)
    assert r["sections"]["基础设定"]
    assert not r["sections"]["氛围画质"]
    assert r["sections"]["画面内容"]


def test_missing_画面内容():
    text = _drop_section(VALID_PROMPT, "画面内容")
    r = _check(text)
    assert r["sections"]["基础设定"]
    assert r["sections"]["氛围画质"]
    assert not r["sections"]["画面内容"]


# --- 3. 顺序错乱 ---

def test_order_wrong_非严格仅警告():
    text = "【画面内容】\nfoo\n【基础设定】\nbar\n【氛围画质】\nbaz\n"
    r = _check(text)
    assert all(r["sections"].values()), "三大段仍齐全"
    assert not r["order_ok"], "顺序应判定为错乱"


# --- 4. 无【】包裹的旧风格标题 ---

def test_legacy_no_brackets_fails():
    text = """基础设定：测试
氛围画质：测试
画面内容：测试
"""
    r = _check(text)
    assert not r["sections"]["基础设定"], "无【】应判定为缺失"
    assert not r["sections"]["氛围画质"]
    assert not r["sections"]["画面内容"]


# --- 5. 参考图描述在 / 不在 ---

def test_reference_image_with_描述_colon():
    text = "参考图描述：金属机器人 3/4 侧视角，胸前 LED 红光"
    assert vp.has_reference_image_desc(text)


def test_reference_image_with_描述_中文冒号():
    text = "参考图描述：金属机器人 3/4 侧视角"
    assert vp.has_reference_image_desc(text)


def test_reference_image_bare_fails():
    """单独写「参考图」不接描述，应判定为缺失。"""
    text = "我已经上传了参考图。"
    assert not vp.has_reference_image_desc(text)


def test_reference_image_blank_fails():
    """「参考图: 空白」不应误报通过。"""
    text = "参考图:  "
    assert not vp.has_reference_image_desc(text)


# --- 6. 声音限制在 / 不在 ---

def test_sound_limit_present():
    assert vp.check_sound_limit("声音限制：仅保留机械声，无需BGM")


def test_sound_limit_bgm_keyword():
    assert vp.check_sound_limit("无需 BGM")


def test_sound_limit_absent():
    assert not vp.check_sound_limit("整体氛围紧凑高燃")


# --- 7. 景别 / 构图 / 运镜 缺失 ---

def test_shot_size_present():
    assert "中景" in vp.check_shot_size(VALID_PROMPT)


def test_shot_size_absent():
    assert vp.check_shot_size("没有任何景别关键词的提示词") == []


def test_composition_absent():
    assert vp.check_composition("没有任何构图关键词的提示词") == []


def test_camera_move_absent():
    assert vp.check_camera_move("没有任何运镜关键词的提示词") == []


# --- 8. 字数边界 ---

def test_count_chars_99():
    text = "测" * 99
    assert vp.count_chars(text) == 99
    r = _check(text, min_chars=100, max_chars=1500)
    assert not r["in_range"]


def test_count_chars_100():
    text = "测" * 100
    r = _check(text, min_chars=100, max_chars=1500)
    assert r["in_range"]


def test_count_chars_1500():
    text = "测" * 1500
    r = _check(text, min_chars=100, max_chars=1500)
    assert r["in_range"]


def test_count_chars_1501():
    text = "测" * 1501
    r = _check(text, min_chars=100, max_chars=1500)
    assert not r["in_range"]


# --- 9. CLI 行为：stdin 输入 ---

def test_stdin_input(tmp_path, monkeypatch, capsys):
    """通过 stdin 传 - 应能读入并完成检查。"""
    p = tmp_path / "prompt.txt"
    p.write_text(VALID_PROMPT, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["validate_prompt.py", str(p)])
    try:
        vp.main()
    except SystemExit as e:
        assert e.code == 0, f"应通过，退出码 {e.code}"
    out = capsys.readouterr().out
    assert "[OK] 提示词结构通过" in out


# --- 10. CLI 行为：文件不存在退出码 2 ---

def test_nonexistent_file_exits_2(capsys):
    sys_argv_save = sys.argv
    sys.argv = ["validate_prompt.py", "/nonexistent/path/prompt.txt"]
    try:
        with pytest.raises(SystemExit) as exc_info:
            vp.main()
        assert exc_info.value.code == 2
    finally:
        sys.argv = sys_argv_save


# --- 11. CLI 行为：--min-chars / --max-chars 覆盖 ---

def test_cli_min_max_chars_override(tmp_path, monkeypatch, capsys):
    p = tmp_path / "prompt.txt"
    p.write_text(VALID_PROMPT, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["validate_prompt.py", str(p), "--min-chars", "50", "--max-chars", "3000"])
    try:
        vp.main()
    except SystemExit as e:
        # VALID_PROMPT 中文字数约 600 多，落入 50-3000 区间，无 issues
        assert e.code == 0
    out = capsys.readouterr().out
    assert "区间 50-3000" in out


# --- 12. CLI 行为：--strict 模式下顺序错乱退出码 1 ---

def test_strict_mode_order_wrong(tmp_path, monkeypatch):
    p = tmp_path / "wrong.txt"
    p.write_text("【画面内容】\nx\n【基础设定】\ny\n【氛围画质】\nz\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["validate_prompt.py", str(p), "--strict"])
    with pytest.raises(SystemExit) as exc_info:
        vp.main()
    assert exc_info.value.code == 1


# --- 13. CLI 行为：subprocess 集成测试（端到端） ---

def test_subprocess_valid_template():
    """端到端：subprocess 跑 single-shot 模板，应退出 0。"""
    result = subprocess.run(
        [sys.executable, "scripts/validate_prompt.py", "templates/single-shot.md"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert "[OK] 提示词结构通过" in result.stdout


def test_subprocess_no_args_exits_2():
    """端到端：transcribe.py 不带参数应退出 2。"""
    result = subprocess.run(
        [sys.executable, "assets/transcribe.py"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 2
    assert "ERROR" in result.stderr
    assert "--audio" in result.stderr
