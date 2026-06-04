# -*- coding: utf-8 -*-
"""把带时间戳的分段文案合并为自然段落（按静音停顿切分），输出纯净版。"""
import re
import json

SRC = r"c:\Users\wayhow\Desktop\AI视频提示词\transcript.json"
DST = r"c:\Users\wayhow\Desktop\AI视频提示词\transcript_纯文本.txt"

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

segs = data["segments"]
GAP = 1.5  # 段间停顿超过 1.5s 视为换段

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

# 句间补空格（中英文混排，ASR 已无空格，需要适度补）
def fix_punct(s: str) -> str:
    # 中文标点后不补空格；英文/数字前后补空格
    s = re.sub(r"([\u4e00-\u9fff])([A-Za-z0-9])", r"\1 \2", s)
    s = re.sub(r"([A-Za-z0-9])([\u4e00-\u9fff])", r"\1 \2", s)
    # 标点规范化
    s = s.replace(" ,", "，").replace(" .", "。")
    s = s.replace(" ?", "？").replace(" !", "！")
    s = s.replace("  ", " ").replace("  ", " ")
    return s

with open(DST, "w", encoding="utf-8") as f:
    f.write(f"# 《丧尸清道夫》创作思路分享 — 文案（ASR 转录）\n\n")
    f.write(f"原视频：BV1xuVC6AEbg  UP主：Mx-Shell（刘紫鱼）  时长：约 42 分 53 秒\n")
    f.write(f"模型：faster-whisper medium（int8，中文）  段数：{len(segs)}  段落数：{len(paragraphs)}\n\n")
    f.write("---\n\n")
    for i, p in enumerate(paragraphs, 1):
        f.write(fix_punct(p) + "\n\n")

print(f"paragraphs={len(paragraphs)} chars={sum(len(p) for p in paragraphs)}")
print(f"saved -> {DST}")
