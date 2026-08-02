#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用 faster-whisper 对视频音频做中文 ASR 转录。

模型选型：
- 优先尝试 medium（精度/速度较平衡）；若内存不足自动回退到 small。
- 量化 int8 节省内存并加速 CPU 推理。
- 启用 VAD 过滤静音段，减少幻觉与重复。

路径解析（v0.2.0 起）：
- 通过 --audio / --out-dir 显式传入；或环境变量 AUDIO / TRANSCRIBE_OUT_DIR。
- 不再硬编码 Windows 路径，跨平台可用。
- 不传任何参数时，输出 ERROR 并以退出码 2 退出。
"""
import os
import sys
import time
import json
import argparse


def fmt_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def fmt_srt_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    ms = int((s - int(s)) * 1000)
    return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"


def try_model(name: str):
    from faster_whisper import WhisperModel
    print(f"[load] WhisperModel({name}, cpu, int8) ...", flush=True)
    t0 = time.time()
    model = WhisperModel(name, device="cpu", compute_type="int8")
    print(f"[load] ok in {time.time()-t0:.1f}s", flush=True)
    return model


def resolve_paths(args: argparse.Namespace) -> dict:
    """按优先级解析输入/输出路径：CLI > 环境变量 > 错误退出。"""
    audio = args.audio or os.environ.get("AUDIO")
    if not audio:
        print("ERROR: 必须通过 --audio 或环境变量 AUDIO 指定输入音频", file=sys.stderr)
        print("示例: python assets/transcribe.py --audio /path/to/audio.wav", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(audio):
        print(f"ERROR: 输入文件不存在: {audio}", file=sys.stderr)
        sys.exit(2)

    out_dir = args.out_dir or os.environ.get("TRANSCRIBE_OUT_DIR") or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    return {
        "audio": audio,
        "out_txt": os.path.join(out_dir, "transcript.txt"),
        "out_srt": os.path.join(out_dir, "transcript.srt"),
        "out_json": os.path.join(out_dir, "transcript.json"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="使用 faster-whisper 对音频做中文 ASR 转录（v0.2.0 起支持跨平台路径）"
    )
    parser.add_argument(
        "--audio",
        help="输入音频文件路径（也可通过环境变量 AUDIO 传入）",
    )
    parser.add_argument(
        "--out-dir",
        help="输出目录（也可通过环境变量 TRANSCRIBE_OUT_DIR 传入；默认当前目录）",
    )
    parser.add_argument(
        "--model",
        default="medium",
        help="Whisper 模型名（默认 medium；内存不足时自动回退到 small）",
    )
    parser.add_argument(
        "--beam", type=int, default=5,
        help="beam_size（默认 5）",
    )
    parser.add_argument(
        "--language", default="zh",
        help="识别语言代码（默认 zh；传 auto 让模型自动检测语言）",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    paths = resolve_paths(args)
    AUDIO = paths["audio"]
    OUT_TXT = paths["out_txt"]
    OUT_SRT = paths["out_srt"]
    OUT_JSON = paths["out_json"]

    # faster-whisper 会把整段音频解码进内存，超大文件可能耗尽内存，提前提示
    size_mb = os.path.getsize(AUDIO) / (1024 * 1024)
    if size_mb > 500:
        print(f"[warn] 输入音频约 {size_mb:.0f}MB，解码后内存占用较大，建议先切分或压缩音频", flush=True)

    candidates = [args.model]
    if args.model != "small":
        candidates.append("small")

    model = None
    for n in candidates:
        try:
            model = try_model(n)
            break
        except Exception as e:
            print(f"[load] {n} failed: {e}", flush=True)
    if model is None:
        print("FATAL: no model loaded", file=sys.stderr)
        sys.exit(1)

    lang = None if args.language.strip().lower() in ("auto", "none") else args.language
    # 中文 initial_prompt 仅在中文识别时注入，避免干扰其他语言
    zh_prompt = "以下是普通话视频文案，可能涉及AI创作、影视制作、剧本、绘画、分镜等话题。"

    print(f"[asr] start: {AUDIO}", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(
        AUDIO,
        language=lang,
        beam_size=args.beam,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=True,
        initial_prompt=zh_prompt if lang == "zh" else None,
    )
    print(f"[asr] language={info.language} prob={info.language_probability:.3f} duration={info.duration:.1f}s", flush=True)

    lines = []
    srt_blocks = []
    json_segments = []
    n = 0
    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        # 跳过空文本段后再自增，保证 SRT 序号连续（严格解析器要求 1,2,3...）
        n += 1
        ts = fmt_ts(seg.start)
        lines.append(f"[{ts}] {text}")
        srt_blocks.append(f"{n}\n{fmt_srt_ts(seg.start)} --> {fmt_srt_ts(seg.end)}\n{text}\n")
        json_segments.append({
            "id": seg.id,
            "start": seg.start,
            "end": seg.end,
            "text": text,
            "avg_logprob": seg.avg_logprob,
            "no_speech_prob": seg.no_speech_prob,
        })
        # 进度输出
        if n % 20 == 0:
            print(f"[asr] {n} segs | last={ts} | elapsed={time.time()-t0:.1f}s", flush=True)

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(OUT_SRT, "w", encoding="utf-8") as f:
        # 每个 block 已以 \n 结尾，用 \n 连接即得到 SRT 块间空行；
        # 注意 f.write 不接受 list，必须先 join
        f.write("\n".join(srt_blocks))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"language": info.language, "duration": info.duration,
                   "segments": json_segments}, f, ensure_ascii=False, indent=2)

    print(f"[done] segments={n} elapsed={time.time()-t0:.1f}s", flush=True)
    print(f"[done] TXT  -> {OUT_TXT}", flush=True)
    print(f"[done] SRT  -> {OUT_SRT}", flush=True)
    print(f"[done] JSON -> {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
