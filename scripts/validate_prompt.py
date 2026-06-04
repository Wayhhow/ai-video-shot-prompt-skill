#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词结构自检工具

检查一个 AI 视频提示词是否符合"基础设定 / 氛围画质 / 画面内容"三大部分框架，
以及是否包含去 AI 味关键词、景别/构图/运镜、参考图描述等关键要素。

Usage:
    python validate_prompt.py <prompt_file>
    python validate_prompt.py <prompt_file> --strict
    cat prompt.txt | python validate_prompt.py -

Exit codes:
    0 = 通过（或警告）
    1 = 严重缺失
    2 = 文件/参数错误
"""
import sys
import re
import io
import argparse
from pathlib import Path

# 强制 stdout/stderr 使用 UTF-8（解决 Windows GBK 编码问题）
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 兼容旧 Python：用 ASCII 符号代替 Unicode
OK = "[OK]"
FAIL = "[X]"
WARN = "[!]"


# 三大段标记（必须存在）
REQUIRED_SECTIONS = [
    ("基础设定", ["基础设定", "设定"]),
    ("氛围画质", ["氛围画质", "画质", "氛围"]),
    ("画面内容", ["画面内容", "画面", "内容"]),
]

# 关键要素
DEAI_KEYWORDS = ["超写实", "极致逼真", "真人实景拍摄"]  # 至少 1 个
SHOT_SIZES = ["特写", "近景", "中景", "远景", "全景", "微距", "广角", "监控", "POV", "第一人称"]
COMPOSITIONS = ["三分线", "黄金分割", "对角线", "引导线", "荷兰角", "对称", "框架式"]
CAMERA_MOVES = ["推", "拉", "摇", "移", "跟", "固定", "手持", "环绕", "仰拍", "俯拍", "航拍", "变焦"]

# 推荐字数范围
MIN_CHARS = 100
MAX_CHARS = 1500


def load_prompt(path_or_dash: str) -> str:
    if path_or_dash == "-":
        return sys.stdin.read()
    p = Path(path_or_dash)
    if not p.exists():
        print(f"ERROR: 文件不存在: {p}", file=sys.stderr)
        sys.exit(2)
    return p.read_text(encoding="utf-8")


def has_any(text: str, keywords: list) -> list:
    return [k for k in keywords if k in text]


def check_sections(text: str) -> dict:
    result = {}
    for name, aliases in REQUIRED_SECTIONS:
        result[name] = any(a in text for a in aliases)
    return result


def check_deai(text: str) -> list:
    return has_any(text, DEAI_KEYWORDS)


def check_shot_size(text: str) -> list:
    return has_any(text, SHOT_SIZES)


def check_composition(text: str) -> list:
    return has_any(text, COMPOSITIONS)


def check_camera_move(text: str) -> list:
    return has_any(text, CAMERA_MOVES)


def has_reference_image_desc(text: str) -> bool:
    """检查参考图描述是否存在。"""
    has_keyword = "参考图" in text or "参考" in text
    has_description = bool(re.search(r"参考图.{0,8}[:：]", text)) or "参考图描述" in text
    return has_keyword and has_description


def check_sound_limit(text: str) -> bool:
    """检查是否提及声音限制（仅 C-Dance 类必填）。"""
    return "声音" in text or "BGM" in text or "配乐" in text


def count_chars(text: str) -> int:
    """中文字符数。"""
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def main():
    parser = argparse.ArgumentParser(description="AI 视频提示词结构自检")
    parser.add_argument("input", help="提示词文件路径，或 - 表示从 stdin 读取")
    parser.add_argument("--strict", action="store_true", help="严格模式：任何缺失都返回非零退出码")
    args = parser.parse_args()

    try:
        text = load_prompt(args.input)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    print("=" * 60)
    print("AI 视频提示词结构自检")
    print("=" * 60)

    issues = []
    warnings = []
    passes = []

    # 1. 三大段
    sections = check_sections(text)
    print("\n【1. 三大段结构】")
    for name, ok in sections.items():
        mark = OK if ok else FAIL
        print(f"  {mark} {name}: {'存在' if ok else '缺失'}")
        if ok:
            passes.append(f"三大段-{name}")
        else:
            issues.append(f"三大段缺失: {name}")

    # 2. 去 AI 味关键词
    print("\n【2. 去 AI 味关键词（强制）】")
    deai = check_deai(text)
    if deai:
        print(f"  {OK} 已包含: {', '.join(deai)}")
        passes.append("去AI味关键词")
    else:
        print(f"  {FAIL} 未找到以下任何关键词: {', '.join(DEAI_KEYWORDS)}")
        issues.append("去AI味关键词缺失")

    # 3. 参考图描述
    print("\n【3. 参考图描述】")
    if has_reference_image_desc(text):
        print(f"  {OK} 已包含参考图描述")
        passes.append("参考图描述")
    else:
        print(f"  {WARN} 未发现「参考图描述」字段")
        warnings.append("建议添加参考图描述（即使是虚拟参考图）")

    # 4. 声音限制
    print("\n【4. 声音限制】")
    if check_sound_limit(text):
        print(f"  {OK} 已提及声音处理")
        passes.append("声音限制")
    else:
        print(f"  {WARN} 未提及声音限制")
        warnings.append("若用 C-Dance 类自动配乐平台，务必加「无需 BGM、仅保留对白/环境音」")

    # 5. 景别
    print("\n【5. 景别】")
    shot = check_shot_size(text)
    if shot:
        print(f"  {OK} 已包含: {', '.join(shot)}")
        passes.append("景别")
    else:
        print(f"  {FAIL} 未找到任何景别（建议从 {', '.join(SHOT_SIZES)} 中选 1 个）")
        issues.append("景别缺失")

    # 6. 构图
    print("\n【6. 构图】")
    comp = check_composition(text)
    if comp:
        print(f"  {OK} 已包含: {', '.join(comp)}")
        passes.append("构图")
    else:
        print(f"  {WARN} 未找到任何构图（建议从 {', '.join(COMPOSITIONS)} 中选 1 个）")
        warnings.append("建议添加构图（如「三分线构图」）")

    # 7. 运镜
    print("\n【7. 运镜】")
    move = check_camera_move(text)
    if move:
        print(f"  {OK} 已包含: {', '.join(move)}")
        passes.append("运镜")
    else:
        print(f"  {WARN} 未找到任何运镜（建议从 {', '.join(CAMERA_MOVES)} 中选 1 个）")
        warnings.append("建议添加运镜（如「手持跟拍」）")

    # 8. 字数
    print("\n【8. 字数】")
    cn_chars = count_chars(text)
    print(f"  中文字符数: {cn_chars}")
    if cn_chars < MIN_CHARS:
        print(f"  {WARN} 字数偏少（建议 >= {MIN_CHARS}）")
        warnings.append(f"字数 {cn_chars} < {MIN_CHARS}")
    elif cn_chars > MAX_CHARS:
        print(f"  {WARN} 字数偏多（建议 <= {MAX_CHARS}，过多会分散 AI 注意力）")
        warnings.append(f"字数 {cn_chars} > {MAX_CHARS}")
    else:
        print(f"  {OK} 字数合理")
        passes.append("字数")

    # 9. 总结
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    print(f"  {OK} 通过: {len(passes)} 项")
    print(f"  {WARN} 警告: {len(warnings)} 项")
    print(f"  {FAIL} 严重: {len(issues)} 项")

    if issues:
        print("\n严重问题（必须修复）:")
        for i in issues:
            print(f"  - {i}")
    if warnings:
        print("\n建议优化:")
        for w in warnings:
            print(f"  - {w}")

    print()
    if issues:
        print(f"{FAIL} 提示词存在严重缺失，请补充")
        sys.exit(1)
    elif warnings and args.strict:
        print(f"{WARN} 严格模式下存在警告")
        sys.exit(1)
    else:
        print(f"{OK} 提示词结构通过")
        sys.exit(0)


if __name__ == "__main__":
    main()
