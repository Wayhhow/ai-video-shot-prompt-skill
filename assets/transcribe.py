# -*- coding: utf-8 -*-
"""使用 faster-whisper 对视频音频做中文 ASR 转录。

模型选型：
- 优先尝试 medium（精度/速度较平衡）；若内存不足自动回退到 small。
- 量化 int8 节省内存并加速 CPU 推理。
- 启用 VAD 过滤静音段，减少幻觉与重复。
"""
import os
import sys
import time
import json

AUDIO = r"c:\Users\wayhow\Desktop\AI视频提示词\audio_16k_mono.wav"
OUT_TXT = r"c:\Users\wayhow\Desktop\AI视频提示词\transcript.txt"
OUT_SRT = r"c:\Users\wayhow\Desktop\AI视频提示词\transcript.srt"
OUT_JSON = r"c:\Users\wayhow\Desktop\AI视频提示词\transcript.json"


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


def main():
    model_name = sys.argv[1] if len(sys.argv) > 1 else "medium"
    beam = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    candidates = [model_name]
    if model_name != "small":
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

    print(f"[asr] start: {AUDIO}", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(
        AUDIO,
        language="zh",
        beam_size=beam,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=True,
        initial_prompt="以下是普通话视频文案，可能涉及AI创作、影视制作、剧本、绘画、分镜等话题。",
    )
    print(f"[asr] language={info.language} prob={info.language_probability:.3f} duration={info.duration:.1f}s", flush=True)

    lines = []
    srt_blocks = []
    json_segments = []
    n = 0
    for seg in segments:
        n += 1
        text = seg.text.strip()
        if not text:
            continue
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
