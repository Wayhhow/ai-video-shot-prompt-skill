# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- v0.3 — Auto storyboard timing allocator
- v0.4 — LLM-as-judge prompt quality scorer

## [0.2.0] - 2026-06-07

### Added
- 5 套新风格预设：机甲 / 机甲战、古风 / 国风、港片 / 霓虹九龙、北欧冷调、复古港片（80s）
- 关键词库新增 5 个新分类（机甲 / 工笔 / 港片 / 北欧冷调 / 复古港片 80s），共 30+ 关键词
- `install.sh` / `install.ps1`：跨平台一键安装脚本，替换 INSTALL.md 的模板占位
- 单元测试 `tests/test_validate_prompt.py`：27 个用例覆盖 9 大类规则 + 边界 + CLI
- GitHub Actions CI：Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13 矩阵跑 pytest
- `pyproject.toml` 的 `[tool.pytest.ini_options]` 段
- `references/prompt-quality-checklist.md`：12 条可勾选质量清单
- `SKILL.md` frontmatter 中英双语 description + 可选 `keywords` 字段
- README 顶部新增 CI 徽章

### Changed
- `scripts/validate_prompt.py` 升级到 v0.2：
  - 三大段标题必须用 `【】` 包裹（不再接受"基础设定：xxx"等无【】写法）
  - 新增三大段顺序校验（基础设定 → 氛围画质 → 画面内容）
  - 新增 `--strict` / `--min-chars` / `--max-chars` CLI 参数
  - 参考图描述正则加固（接受"参考图描述："、"参考图："、"参考图" + 换行 + 描述）
  - Python 3.9+ 兼容（`from __future__ import annotations` 已在脚本中显式标注）
- `assets/transcribe.py` / `assets/merge_text.py` 改为 CLI 参数化（`--audio` / `--out-dir` / `--src` / `--dst`）+ 环境变量回退；不再硬编码 Windows 路径
- `templates/single-shot.md` 检验清单字数区间与自检脚本对齐（100-1500）
- `templates/multi-shot.md` / `templates/action-scene.md` 检验清单新增"多分镜可放宽到 3000 字"说明
- `INSTALL.md` 改为引用真实 `install.sh` / `install.ps1`

### BREAKING CHANGES ⚠️
- `scripts/validate_prompt.py` 不再接受"基础设定：xxx"等无【】大节标题的写法。
  - **影响**：使用 v0.1.0 时若提示词用 `基础设定：` 而非 `【基础设定】`，v0.2 会判为"基础设定缺失"。
  - **迁移**：把所有大节标题改为 `【基础设定】`、`【氛围画质】`、`【画面内容】`。
  - **机器验证**：`python scripts/validate_prompt.py your-prompt.md` 退出码 0 即合规。
- `assets/transcribe.py` 不再有内置的 Windows 默认路径。必须通过 `--audio` 或环境变量 `AUDIO` 显式传入。
  - **影响**：直接 `python assets/transcribe.py` 不再"自动"指向桌面某路径，而是直接 ERROR 退出。
  - **迁移**：`python assets/transcribe.py --audio /path/to/audio.wav`。
- `assets/merge_text.py` 同上。改用 `--src` / `--dst` / `MERGE_SRC` / `MERGE_DST`。

### Notes
- 基线（v0.1.0 行为）输出保存在 `docs/baseline-v0.1.txt`，便于 v0.2 行为对照
- 5 套新风格预设的关键词已并入 `references/keyword-library.md`
- 本版本不重写方法论本体，仅在末尾追加新预设与新检查项
- **PR 描述**：[docs/PR_v0.2.0.md](../docs/PR_v0.2.0.md)（完整动机 / Changes / Test Matrix / 升级指引）
- **下阶段路线**：[docs/NEXT_STEPS.md](../docs/NEXT_STEPS.md)（v0.3 多分镜分配 / v0.4 LLM-as-judge / v1.0 平台 API）

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
