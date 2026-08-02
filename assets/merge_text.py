#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把带时间戳的分段文案合并为自然段落（按静音停顿切分），输出纯净版。

路径解析（v0.2.0 起）：
- 通过 --src / --dst 显式传入；或环境变量 MERGE_SRC / MERGE_DST。
- 不再硬编码 Windows 路径，跨平台可用。
- 不传任何参数时，输出 ERROR 并以退出码 2 退出。
"""
import re
import json
import sys
import os
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="把带时间戳的分段文案合并为自然段落（v0.2.0 起支持跨平台路径）"
    )
    parser.add_argument(
        "--src",
        help="输入 transcript.json 路径（也可通过环境变量 MERGE_SRC 传入）",
    )
    parser.add_argument(
        "--dst",
        help="输出纯文本路径（也可通过环境变量 MERGE_DST 传入；默认同目录的 transcript_纯文本.txt）",
    )
    parser.add_argument(
        "--gap", type=float, default=1.5,
        help="段间停顿超过 N 秒视为换段（默认 1.5）",
    )
    parser.add_argument(
        "--title", default="《丧尸清道夫》创作思路分享 — 文案（ASR 转录）",
        help="输出文件头部的标题",
    )
    parser.add_argument(
        "--source-info", default="原视频：BV1xuVC6AEbg  UP主：Mx-Shell（刘紫鱼）  时长：约 42 分 53 秒",
        help="输出文件头部的源信息",
    )
    return parser.parse_args()


def resolve_paths(args: argparse.Namespace) -> tuple:
    src = args.src or os.environ.get("MERGE_SRC")
    if not src:
        print("ERROR: 必须通过 --src 或环境变量 MERGE_SRC 指定 transcript.json 路径", file=sys.stderr)
        print("示例: python assets/merge_text.py --src transcript.json --dst merged.txt", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(src):
        print(f"ERROR: 输入文件不存在: {src}", file=sys.stderr)
        sys.exit(2)

    if args.dst:
        dst = args.dst
    elif os.environ.get("MERGE_DST"):
        dst = os.environ["MERGE_DST"]
    else:
        dst = os.path.join(os.path.dirname(os.path.abspath(src)) or ".", "transcript_纯文本.txt")
    return src, dst


def fix_punct(s: str) -> str:
    # 中文标点后不补空格；英文/数字前后补空格
    s = re.sub(r"([\u4e00-\u9fff])([A-Za-z0-9])", r"\1 \2", s)
    s = re.sub(r"([A-Za-z0-9])([\u4e00-\u9fff])", r"\1 \2", s)
    # 标点规范化
    s = s.replace(" ,", "，").replace(" .", "。")
    s = s.replace(" ?", "？").replace(" !", "！")
    s = s.replace("  ", " ").replace("  ", " ")
    return s


def main():
    args = parse_args()
    SRC, DST = resolve_paths(args)
    GAP = args.gap

    try:
        with open(SRC, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON 解析失败: {SRC}（{e}）", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"ERROR: 无法读取输入文件: {SRC}（{e}）", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict) or "segments" not in data:
        print(f"ERROR: {SRC} 缺少 'segments' 字段（应传入 transcribe.py 生成的 transcript.json）", file=sys.stderr)
        sys.exit(2)
    segs = data["segments"]
    if not isinstance(segs, list):
        print(f"ERROR: {SRC} 中 'segments' 不是列表", file=sys.stderr)
        sys.exit(2)
    paragraphs = []
    buf = []
    last_end = None
    for s in segs:
        text = s["text"].strip()
        if not text:
            continue
        if last_end is not None and (s["start"] - last_end) > GAP and buf:
            paragraphs.append("".join(buf))
            buf = []
        buf.append(text)
        last_end = s["end"]
    if buf:
        paragraphs.append("".join(buf))

    with open(DST, "w", encoding="utf-8") as f:
        f.write(f"# {args.title}\n\n")
        f.write(f"{args.source_info}\n")
        f.write(f"段数：{len(segs)}  段落数：{len(paragraphs)}\n\n")
        f.write("---\n\n")
        for i, p in enumerate(paragraphs, 1):
            f.write(fix_punct(p) + "\n\n")

    print(f"paragraphs={len(paragraphs)} chars={sum(len(p) for p in paragraphs)}")
    print(f"saved -> {DST}")


if __name__ == "__main__":
    main()
