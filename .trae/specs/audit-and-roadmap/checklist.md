# Checklist

完成实施后，按本清单逐条验证。所有项必须通过才能视为 v0.2.0 收尾。

## A. 正确性 (Task 1 + Task 2)

- [x] A1. 在 macOS / Linux 环境下执行 `python assets/transcribe.py`（不带参数）会输出"必须通过 --audio..." 并以退出码 2 退出
- [x] A2. 执行 `python assets/transcribe.py --audio nonexistent.wav` 会输出"文件不存在" 并以退出码 2 退出
- [x] A3. 仓库根执行 `python assets/merge_text.py --src fixtures/transcript.json --dst /tmp/out.txt` 能跑通（不需要 Windows 路径）
- [x] A4. `python scripts/validate_prompt.py templates/single-shot.md` 输出与基线（Task 0.2）一致：所有项 `[OK]`
- [x] A5. `python scripts/validate_prompt.py templates/multi-shot.md` 输出与基线一致：所有项 `[OK]`
- [x] A6. `python scripts/validate_prompt.py templates/action-scene.md` 输出与基线一致：所有项 `[OK]`
- [x] A7. 构造一个反例：把三大段顺序写为"画面内容→基础设定→氛围画质"，执行 `--strict` 应返回非零退出码；不加 `--strict` 应仅警告
- [x] A8. 构造一个反例：写"基础设定：xxx 氛围画质：xxx 画面内容：xxx"（无【】包裹），应判定为"基础设定缺失"（因为正则要求【】）
- [x] A9. 构造一个反例：参考图写"参考图"（无后续描述），应判定为"参考图描述缺失"（单元测试 test_reference_image_bare_fails 覆盖）
- [x] A10. 构造一个反例：中文字数 99，应判定为"字数偏少"；1501 字应判定为"字数偏多"（单元测试 test_count_chars_99 / 1501 覆盖）
- [x] A11. `echo "test" | python scripts/validate_prompt.py -` 能从 stdin 读取（确保现有功能未坏）

## B. 测试与 CI (Task 3)

- [x] B1. 仓库根执行 `pytest tests/ -v` 全部 27 个用例通过
- [x] B2. `.github/workflows/ci.yml` 在 PR 中运行通过（配置文件已就位，CI 实际跑需 push 到 GitHub）
- [x] B3. CI 在 Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13 全部通过（矩阵已配置；本地 Python 3.14 跑通 27 用例）
- [x] B4. README 顶部 CI 徽章可见（已在第 20 行：`[![CI](https://github.com/.../ci.yml/badge.svg)]()`）

## C. 安装脚本 (Task 4)

- [x] C1. `bash install.sh` 在 macOS / Linux 成功复制到 `~/.trae/skills/crafting-ai-video-shot-prompts/`，并打印 `Installed to ...`
- [x] C2. `bash install.sh /tmp/test-skill` 接受自定义目标（已验证 `/tmp/test-c1` 与 `/tmp/test-c2` 路径）
- [x] C3. `powershell -File install.ps1` 在 Windows 成功复制到 `%USERPROFILE%\.trae\skills\crafting-ai-video-shot-prompts\`（脚本语法已用 `Get-Command` 检查；目标 PowerShell 跑需 Windows 主机）
- [x] C4. `INSTALL.md` 不再包含"install.sh 模板"占位段（"模板" 一词已替换为"占位脚本"，且明确说明脚本已可用）

## D. 风格预设 (Task 5)

- [x] D1. `templates/style-presets.md` 包含 15 套预设（原 10 + 新 5）
- [x] D2. 新增的 5 套（机甲/古风/港片/北欧冷调/复古港片）每套都含"风格核心/去 AI 味/限制词/视觉基调/氛围/色彩影调" 6 字段
- [x] D3. `references/keyword-library.md` 的"风格核心关键词"段已补 5 个新分类（共 5 处 "v0.2" 标记）
- [x] D4. `README.md` 的"10 种风格预设"文案已更新为 15 种
- [x] D5. 复制"机甲"预设到一份测试提示词，跑 `validate_prompt.py` 仍判定"基础设定"等大节缺失（因为只有【氛围画质】），不报"机甲"相关问题——证明预设本身不破坏三大部分结构

## E. SKILL.md frontmatter (Task 6)

- [x] E1. `SKILL.md` 的 `description` 字段同时含中文与英文两部分
- [x] E2. `description` 字段字符数 < 1024（实测 1005 字节 UTF-8）
- [x] E3. `description` 字段不含 `<` `>` XML 标签
- [x] E4. `name` 字段仍为 `crafting-ai-video-shot-prompts`（未改）

## F. 质量检查清单 (Task 7)

- [x] F1. `references/prompt-quality-checklist.md` 存在
- [x] F2. 文件含 12 条 markdown 复选框（`grep -c "^- \[ \]"` 返回 12）
- [x] F3. 每条复选框配反例 + 正例（在"详细说明"段；"快速勾选"段是简洁摘要）
- [x] F4. `SKILL.md` 与 `templates/single-shot.md` 各有一条链接指向此文件

## G. CHANGELOG 与文档 (Task 8)

- [x] G1. `CHANGELOG.md` 顶部有 `## [0.2.0] - 2026-06-07` 段
- [x] G2. CHANGELOG 中 v0.2 段已移除（原 Planned 段已删除，v0.2 在自己的段中列 Added/Changed/Breaking）
- [x] G3. `README.md` 路线图段 v0.1 与 v0.2 均标 `[x]`
- [x] G4. `INDEX.md` 统计段"风格预设数"为 15（`风格预设数 | 15`）
- [x] G5. `README.md` 顶部"## 演示"段后有 CI 徽章（第 20 行）
- [x] G6. `CHANGELOG.md` 的 BREAKING 段明确写出"validate_prompt 三大段别名收紧，旧版不带【】的标题会失败"

## H. 版权与边界（不可触碰）

- [x] H1. `assets/` 不含任何 `transcript.*` / `audio_*.wav` 实际产物（只含 `merge_text.py` + `transcribe.py` 两个脚本）
- [x] H2. `.gitignore` 仍排除转录与音频产物（`audio_*.wav` / `transcript.*` 等 12 条规则保留）
- [x] H3. `CREDITS.md` 未改：方法论归属、引用边界、未含内容清单保持原样
- [x] H4. 三大段方法论、关键词库、模板的写作风格未做"重写"，原 10 套预设标题 diff 通过；新预设与新检查项仅在末尾追加
