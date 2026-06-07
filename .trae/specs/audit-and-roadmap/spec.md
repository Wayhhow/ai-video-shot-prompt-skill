# 项目状态审计与改进路线 Spec

## Why

`crafting-ai-video-shot-prompts` v0.1.0 已交付一套基本可用的中文 AI 视频提示词 Skill（三大部分框架 + 4 模板 + 10 风格预设 + 自检脚本），但通过逐文件审计 + 2026 年行业最佳实践对照，发现三类需要处理的问题：

1. **正确性 bug** — 资产脚本硬编码 Windows 路径、自检脚本对"三大段"的检查不查顺序、回填正则过于脆弱，可能在 macOS/Linux 环境下直接不可用
2. **可发现性不足** — SKILL.md description 是中文，不符合 Anthropic "description 包含做什么+何时用" 的最佳实践；仓库无 install 脚本、无 CI、无测试
3. **能力扩展** — CHANGELOG 已声明 v0.2 (新风格) / v0.3 (分镜自动分配) / v0.4 (LLM-as-judge 评分) / v1.0 (平台 API) 的路线，但都未启动

本 spec 不重写方法论，只**修复 bug + 补齐工程化基础设施 + 落地 CHANGELOG 已声明的下一阶段**。

## What Changes

- **修复** `assets/transcribe.py` 与 `assets/merge_text.py` 的硬编码 Windows 路径（→ CLI 参数 / 环境变量 / 默认值）
- **修复** `scripts/validate_prompt.py` 的三大段检查：改为"按顺序存在"而非"任意顺序存在"
- **修复** `scripts/validate_prompt.py` 的过于宽松别名（"设定""氛围""画面"易误报）+ 加固参考图描述正则
- **修复** `templates/single-shot.md` 检验清单中"200-800 字"与自检脚本"100-1500 字"的不一致
- **新增** `scripts/validate_prompt.py` 的单元测试（pytest，9 大类规则 + 边界 case）
- **新增** GitHub Actions CI：Python 3.9–3.13 矩阵跑测试 + UTF-8 输出
- **新增** `install.sh` 与 `install.ps1`（仓库内、可执行），替换 INSTALL.md 中的"模板占位"
- **新增** `templates/style-presets.md` 5 套新预设（机甲 / 古风 / 港片 / 北欧冷调 / 复古港片）— 兑现 CHANGELOG 的 v0.2
- **新增** `SKILL.md` 英文版 description 的中英双语 frontmatter（中文原文 + 英文翻译），提升可发现性
- **新增** `references/prompt-quality-checklist.md`：把 SKILL.md 中的"反模式"沉淀为 12 条可勾选清单
- **不修改** 三大段方法论本体、关键词库、模板的写作风格

## Impact

- **Affected specs**: 无（这是首次审计，无历史 spec 可影响）
- **Affected code**:
  - `assets/transcribe.py`（重构入口）
  - `assets/merge_text.py`（重构入口）
  - `scripts/validate_prompt.py`（行为变更：顺序校验 + 别名收紧 + 正则加固）
  - `templates/single-shot.md`（数字一致性）
  - `templates/style-presets.md`（追加内容）
  - `SKILL.md`（frontmatter 增字段）
  - `INSTALL.md`（移除"模板占位"段落，改为引用新脚本）
- **Affected docs**: CHANGELOG（更新 v0.2 条目）
- **下游影响**: 自检脚本的行为变化属于"加强约束"，对符合三大部分规范的提示词不会误伤；对故意乱序或缺段的提示词会从"通过"变"严重缺失"，这是符合预期的修复。

## ADDED Requirements

### Requirement: 跨平台 transcribe 入口

`assets/transcribe.py` 必须接受 `audio` / `--audio` 参数（或 `AUDIO` 环境变量）作为输入路径，并保留命令行覆盖。默认值仅在没有传参时使用，且默认值必须放在仓库根的 `assets/transcribe_defaults.json` 或脚本顶部常量的注释中（不要硬编码到具体用户名目录）。

#### Scenario: macOS 用户运行
- **WHEN** macOS 用户执行 `python assets/transcribe.py --audio /tmp/audio.wav`
- **THEN** 脚本使用指定路径，不再因找不到 `c:\Users\wayhow\...` 而崩溃

#### Scenario: 默认值兜底
- **WHEN** 用户不传任何参数
- **THEN** 脚本输出明确的"未指定输入文件"提示，退出码 = 2

### Requirement: 三大段顺序校验

`scripts/validate_prompt.py` 的检查项 1 必须从"存在即可"升级为"按 基础设定 → 氛围画质 → 画面内容 顺序出现"。可由 `--strict` 模式打开严格顺序检查；非 strict 模式下仅给出警告。

#### Scenario: 顺序正确
- **WHEN** 提示词按规范顺序出现三大段
- **THEN** 检查项 1 通过

#### Scenario: 顺序错乱
- **WHEN** 提示词先写"画面内容"再写"基础设定"
- **THEN** strict 模式返回非零退出码；非 strict 模式打印 `[!] 警告: 三大段顺序错乱，建议按 基础设定→氛围画质→画面内容 顺序`

### Requirement: pytest 单元测试

新增 `tests/test_validate_prompt.py`，至少覆盖：
- 9 大类规则的"全通过""全缺失""部分缺失"三态
- 三大段顺序正确 vs 错乱
- 参考图描述在/不在
- 中文字数 99 / 100 / 1500 / 1501 边界
- stdin 模式 (`-` 输入)
- 文件不存在 (退出码 2)

#### Scenario: 测试通过
- **WHEN** 开发者执行 `pytest tests/`
- **THEN** 全部测试通过

### Requirement: GitHub Actions CI

新增 `.github/workflows/ci.yml`，触发条件：push / pull_request。矩阵 Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13。步骤：checkout → setup-python → pip install pytest → pytest。

#### Scenario: PR 提交
- **WHEN** 提交 PR
- **THEN** 5 个 Python 版本 × 全测试 = CI 绿灯

### Requirement: 真实安装脚本

`install.sh` (bash) 与 `install.ps1` (PowerShell) 必须是仓库内可执行文件（不是 INSTALL.md 的占位）。接受一个可选参数：目标安装目录；默认 `~/.trae/skills/crafting-ai-video-shot-prompts/`。

#### Scenario: Linux 用户一键安装
- **WHEN** 用户在仓库根执行 `./install.sh`
- **THEN** skill 复制到 `~/.trae/skills/crafting-ai-video-shot-prompts/` 并打印确认

### Requirement: 5 套新风格预设

`templates/style-presets.md` 追加 5 套预设：

1. **机甲 / 机甲战** — 风格核心含 `机甲`、`机械义体`、`高机动`、`金属磨损`、`HUD 界面`
2. **古风 / 国风** — 风格核心含 `古风`、`青瓦白墙`、`红灯笼`、`油纸伞`、`工笔重彩`
3. **港片 / 霓虹九龙** — 风格核心含 `港片`、`九龙城寨`、`霓虹招牌`、`雨夜`、`复古怀旧`
4. **北欧冷调** — 风格核心含 `北欧冷调`、`极简`、`自然光`、`雪原`、`木屋`
5. **复古港片（80s）** — 风格核心含 `复古港片`、`80 年代`、`磁带质感`、`青黄调`、`单色光`

每套沿用现有 10 套的"风格核心 / 去 AI 味 / 限制词 / 视觉基调 / 氛围 / 色彩影调"6 字段结构。

#### Scenario: 复制预设
- **WHEN** 用户复制"机甲"预设到提示词
- **THEN** 6 字段齐全，可与三大部分框架对齐使用

### Requirement: SKILL.md frontmatter 双语

`SKILL.md` 的 frontmatter `description` 字段升级为中英双语（用 YAML 的 `>` 折叠块，< 1024 字符总长），中文在前，英文在后。`name` 保持 `crafting-ai-video-shot-prompts` 不变。

#### Scenario: 英文环境用户发现
- **WHEN** 英文用户搜索 "AI video prompt Chinese"
- **THEN** frontmatter 英文部分描述能命中

### Requirement: 提示词质量检查清单

新增 `references/prompt-quality-checklist.md`，包含 12 条勾选项，覆盖：
- 三大段是否齐全
- 顺序是否正确
- 参考图是否描述
- 声音限制是否声明
- 去 AI 味关键词是否齐
- 限制词是否 ≥ 3
- 景别 / 构图 / 运镜是否各选 1
- 故事内容是否用"怎么做/为什么/效果"三段式
- 是否有反模式（命令式、无"为什么"、武戏只写"打"）

#### Scenario: 写完后自检
- **WHEN** 用户用本清单逐条勾选
- **THEN** 至少 11/12 通过才视为可发布

## MODIFIED Requirements

### Requirement: validate_prompt.py 三大段别名收紧

原别名 `["基础设定", "设定"]`、`["氛围画质", "画质", "氛围"]`、`["画面内容", "画面", "内容"]` 过于宽松（"设定""氛围""画面"可匹配任意上下文）。改为精确匹配大节标题 `【基础设定】`、`【氛围画质】`、`【画面内容】`，并允许半角空格变体。

**BREAKING**：依赖宽松别名的旧提示词（无 `【】` 包裹的节标题）会从"通过"变"严重缺失"。需在 CHANGELOG v0.2.0 的 BREAKING CHANGES 段说明。

#### Scenario: 旧风格标题
- **WHEN** 提示词写"基础设定：xxx 氛围画质：xxx 画面内容：xxx"（无【】包裹）
- **THEN** 校验失败并提示"请用【基础设定】等中文方括号包裹节标题"

### Requirement: 参考图描述正则加固

原 `参考图.{0,8}[:：]` 假设冒号紧跟"参考图"，实际场景常写"参考图描述：..."或"参考图:..."。改为同时匹配 `参考图描述：`、`参考图：`、`参考图:`、`参考图 ` + 冒号/换行。

#### Scenario: 实际写法的参考图
- **WHEN** 提示词包含"参考图描述：金属机器人 3/4 侧视角"
- **THEN** 检查项 3 通过

## REMOVED Requirements

无删除项。

## 不在本次 spec 范围（推迟到后续）

- v0.3 分镜时长自动分配器（CHANGELOG 已声明）
- v0.4 LLM-as-judge 提示词质量评分（CHANGELOG 已声明）
- v1.0 与即梦/Vidu/可灵/Sora/Runway 的 API 对接（CHANGELOG 已声明）
- PyPI 包发布（`pip install video-prompt-validator`）
- 英文版 SKILL.md 全文翻译（本次只升级 frontmatter）
- 10 套现有风格预设的英文翻译
- Web 演示（Gradio/Streamlit）
- 多分镜提示词的 JSON Schema
