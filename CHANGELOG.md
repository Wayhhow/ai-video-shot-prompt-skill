# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- v0.2 — More style presets (mecha / gufeng / Hong Kong cinema / Nordic cool / retro Hong Kong)
- v0.3 — Auto storyboard timing allocator
- v0.4 — LLM-as-judge prompt quality scorer

## [0.1.0] - 2026-06

### Added
- 三大部分提示词框架 (基础设定 / 氛围画质 / 画面内容)
- 200+ 关键词库 (风格 / 限制 / 设备 / 色调 / 光线 / 氛围)
- 景别 / 构图 / 运镜 完整清单
- 4 套提示词模板 (single-shot / multi-shot / action-scene / style-presets)
- 10 种风格预设 (原子朋克 / 电影动作 / 赛博朋克 / 武侠 / 复古胶片 / 黑色电影 / 纪录片 / 国产爱死机 / 喜剧荒诞 / 监控)
- 提示词结构自检脚本 `scripts/validate_prompt.py` (8 大类规则)
- 短剧 Agent 2.0 工作流与抽卡策略
- 后期剪辑技巧（动作匹配、调色、空间一致性等）
- ASR 辅助脚本 `assets/transcribe.py`（基于 faster-whisper；供用户自行从源视频生成转录，**默认不进入仓库**）

### Notes
- 仓库**不包含**视频音频、字幕、完整转录
- 视频转录与摘要仅在本地保留供开发者调试，**通过 `.gitignore` 排除**
- 所有方法论归 [Mx-Shell](https://space.bilibili.com/388217494) 所有；本仓库为方法论的可执行封装
