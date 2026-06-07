# Tasks

按"先正确性、再工程化、再能力扩展"的顺序排列。每条任务都是可在 1-2 个 PR 内完成的可验证交付物。

## Task 0：基线记录

> 任务编号沿用 CHANGELOG 风格从 0 开始，方便后续 spec 续编

- [x] **Task 0.1**：在 CHANGELOG.md 顶部 `[Unreleased]` 段下新增 `### Changed (v0.2.0 BREAKING)` 段，把"validate_prompt 三大段别名收紧"列为 BREAKING CHANGE。
- [x] **Task 0.2**：跑一次 `python scripts/validate_prompt.py templates/single-shot.md` 把当前输出截图保存到 `docs/baseline-v0.1.png`（如无 GUI 可改为保存文本输出到 `docs/baseline-v0.1.txt`），作为 v0.2 行为变更的对照基线。

## Task 1：修复硬编码路径

- [x] SubTask 1.1：在 `assets/transcribe.py` 顶部把 `AUDIO` / `OUT_TXT` / `OUT_SRT` / `OUT_JSON` 改为函数 `resolve_paths(audio: str | None, out_dir: str | None) -> dict` 的返回值，命令行 `argparse` 接受 `--audio`、`--out-dir`，未传参时回退到 `os.environ.get("AUDIO")` / 当前目录。
- [x] SubTask 1.2：在 `assets/transcribe.py` 增加 `if audio is None: print("ERROR: 必须通过 --audio 或环境变量 AUDIO 指定输入音频", file=sys.stderr); sys.exit(2)`。
- [x] SubTask 1.3：把 `assets/merge_text.py` 同样改为 CLI 参数化（`--src`、`--dst`），不再读 `r"c:\Users\wayhow\..."`。
- [x] SubTask 1.4：在两个脚本顶部加 `#!/usr/bin/env python3` shebang（已有）与 `# -*- coding: utf-8 -*-`（已有）确认。

## Task 2：加固自检脚本

- [x] SubTask 2.1：在 `scripts/validate_prompt.py` 中引入 `SECTION_PATTERN = r"【\s*基础设定\s*】"` 等 3 个正则，按顺序扫描原文，输出每个大节出现的 `start_char`。
- [x] SubTask 2.2：检查 `basic.start < mood.start < content.start`，否则在 strict 模式计为 issue、非 strict 计为 warning。
- [x] SubTask 2.3：把 `REQUIRED_SECTIONS` 改为只接受 `【xxx】` 包裹的精确标题，删除"设定""氛围""画面"宽松别名。
- [x] SubTask 2.4：把 `has_reference_image_desc` 改为同时匹配 `参考图描述[:：]?`、`参考图[:：]?`、`参考图\n`，并在前面 30 字符内要求至少 4 个中文字（避免误匹配"参考图：空白"）。
- [x] SubTask 2.5：把 `MIN_CHARS=100` / `MAX_CHARS=1500` 拆为 `--min-chars` / `--max-chars` CLI 参数，默认保留 100/1500。
- [x] SubTask 2.6：把 `templates/single-shot.md` 检验清单的 "200-800 中文字" 改为 "100-1500 中文字"（与脚本一致），并在 multi-shot / action-scene 的检验清单中标注"长多分镜可放宽到 3000 字"。

## Task 3：单元测试与 CI

- [x] SubTask 3.1：新增 `tests/__init__.py`（空）与 `tests/test_validate_prompt.py`。
- [x] SubTask 3.2：在 `tests/test_validate_prompt.py` 中提供至少 12 个 fixture / 用例：全通过、单段缺失、顺序错乱、参考图缺失、声音缺失、景别缺失、构图缺失、运镜缺失、字数 99、字数 1501、stdin 输入、文件不存在。
- [x] SubTask 3.3：在仓库根新增 `pyproject.toml` 的 `[tool.pytest.ini_options]` 段（如尚无 pyproject.toml，则新建最小化的）。
- [x] SubTask 3.4：新增 `.github/workflows/ci.yml`，矩阵 Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13，步骤 `pip install pytest` + `pytest -v`。
- [x] SubTask 3.5：在 README.md 顶部"演示"段后加一个 `[![CI](https://github.com/.../workflows/ci.yml/badge.svg)]()` 徽章（徽章脚本 placeholder，待真实仓库 URL 填入；用 `OWNER/REPO` 占位即可）。

## Task 4：真实安装脚本

- [x] SubTask 4.1：新增 `install.sh`：bash 脚本，`chmod +x`，接受可选参数 `$1` 作为目标目录；默认 `$HOME/.trae/skills/crafting-ai-video-shot-prompts/`；`mkdir -p` 后 `cp -R "$SRC"/. "$DST"/`；打印 `Installed to $DST`。
- [x] SubTask 4.2：新增 `install.ps1`：PowerShell 脚本，接受可选 `-DestDir`；默认 `$env:USERPROFILE\.trae\skills\crafting-ai-video-shot-prompts`；`Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force`。
- [x] SubTask 4.3：在 `INSTALL.md` 中删除"install.sh 模板"与"install.ps1 模板"两个代码段，改为引用"见仓库根的 `install.sh` / `install.ps1`"。

## Task 5：5 套新风格预设

- [x] SubTask 5.1：在 `templates/style-presets.md` 末尾追加"## 预设 11：机甲 / 机甲战"——风格核心 5 个、去 AI 味 + 电影动作捕捉、限制词 4 个、视觉基调 ARRI Alexa 65、氛围"高燃机械对战"、色彩影调"青橙 + 金属反光"。
- [x] SubTask 5.2：追加"## 预设 12：古风 / 国风"——风格核心含`古风、青瓦白墙、红灯笼、油纸伞、工笔重彩`，去 AI 味含`东方美学质感`，视觉基调 ARRI Alexa 65 + 模拟工笔重彩，氛围"含蓄、留白、东方意境"，色彩影调"低饱和 + 朱红 + 黛青"。
- [x] SubTask 5.3：追加"## 预设 13：港片 / 霓虹九龙"——风格核心含`港片、九龙城寨、霓虹招牌、雨夜、复古怀旧`，去 AI 味含`极致逼真`，限制词含`杜绝霓虹过曝`，视觉基调 ARRI Alexa Mini LF，氛围"潮湿、霓虹、压抑"，色彩影调"品红 + 青蓝 + 暖黄高光"。
- [x] SubTask 5.4：追加"## 预设 14：北欧冷调"——风格核心含`北欧冷调、极简、自然光、雪原、木屋`，去 AI 味含`极致逼真、北欧纪录片质感`，视觉基调 ARRI Alexa 65 + 自然光，氛围"孤寂、克制、留白"，色彩影调"高亮灰白 + 冷蓝阴影"。
- [x] SubTask 5.5：追加"## 预设 15：复古港片（80s）"——风格核心含`复古港片、80 年代、磁带质感、青黄调、单色光`，去 AI 味含`极致逼真、复古胶片质感`，视觉基调 Kodak Vision3 500T 胶片，氛围"江湖义气、复古霓虹"，色彩影调"青黄高光 + 暖色偏移"。
- [x] SubTask 5.6：在 `references/keyword-library.md` 的"风格核心关键词"段补 5 个新分类的 4-6 个关键词（如"机甲"分类下加 `HUD 界面`、`机械外骨骼`、`等离子武器`、`过载警报`）。
- [x] SubTask 5.7：在 `README.md` 的"10 种风格预设"段更新为"15 种风格预设"并链接新预设。

## Task 6：SKILL.md frontmatter 双语

- [x] SubTask 6.1：在 `SKILL.md` 的 frontmatter `description` 字段改为 YAML 折叠块，先放中文（保留原文），换行后追加英文翻译：
  > "Writes, reviews, and refines Chinese shot-list prompts for AI video generators (即梦/Vidu/可灵/小云雀/Sora/Runway). Encapsulates the '基础设定/氛围画质/画面内容' three-part framework and de-AI-flavor techniques from Mx-Shell's 'Zombie Scavenger' methodology. Use when the user wants to write a single shot, plan a multi-shot short, score an AI video script, or reduce AI artifacts (plastic skin, stiff motion, game-CG feel) in action/cinematic/atomic-punk/zombie scenes."
- [x] SubTask 6.2：确认总字符数 < 1024（中文 + 英文）。如超长可裁剪中文部分细节。
- [x] SubTask 6.3：在 `description` 后追加可选 `keywords:` 字段，逗号分隔 8-12 个英文关键词：`ai video prompt, shot list, chinese, sora, runway, kling, 即梦, vidu, atomic punk, cinematic, action, scoring`（keywords 不是 Anthropic 官方 frontmatter 字段，但部分客户端支持；先加上作为"建议"，如未来官方支持扩展会自然迁移）。

## Task 7：质量检查清单文档

- [x] SubTask 7.1：新增 `references/prompt-quality-checklist.md`，包含 12 条 markdown 复选框。
- [x] SubTask 7.2：每条复选框配 1 句解释 + 1 个"❌ 反例" / "✅ 正例"。
- [x] SubTask 7.3：在 `SKILL.md` 的"反模式"段后加一行：`完整 12 条质量清单见 [references/prompt-quality-checklist.md](references/prompt-quality-checklist.md)`。
- [x] SubTask 7.4：在 `templates/single-shot.md` 末尾的"检验清单"段后加一个链接，指向 prompt-quality-checklist。

## Task 8：CHANGELOG 与文档收尾

- [x] SubTask 8.1：在 `CHANGELOG.md` 的 `[Unreleased]` 段补 `## [0.2.0] - 2026-06-??` 子段，列出 Added/Changed/Breaking。
- [x] SubTask 8.2：把 CHANGELOG 中 Planned 的 `v0.2 — More style presets` 标记为 `[x]`，`v0.3 / v0.4 / v1.0` 保留为 `[ ]`。
- [x] SubTask 8.3：在 `README.md` 的"路线图"段把 `v0.2` 的 `[ ]` 改为 `[x]` 并标注日期。
- [x] SubTask 8.4：在 `INDEX.md` 的"统计"段把"风格预设数 10"更新为 15，"Python 脚本 3"更新为 3（不变），"仓库实际文件"按实际增量更新。

# Task Dependencies

- [Task 2] 依赖 [Task 1]（先确保现有测试通过再改行为）
- [Task 3] 依赖 [Task 2]（测试覆盖新行为）
- [Task 6] 依赖 [Task 4]（安装脚本让 frontmatter 描述更可验证）
- [Task 8] 依赖 [Task 1, 2, 3, 4, 5, 6, 7]（CHANGELOG 收尾）
- Task 5 / Task 7 互相独立

# 可并行执行

- Task 1（路径修复）与 Task 5（新风格预设）完全独立，可并行
- Task 6（frontmatter）与 Task 7（检查清单）完全独立，可并行
- Task 4（安装脚本）与 Task 3（CI）相互独立，但都依赖 Task 2（脚本行为稳定后再补 CI）
