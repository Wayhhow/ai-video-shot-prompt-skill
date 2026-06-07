# PR：v0.2.0 — 5 new style presets + cross-platform scripts + pytest + CI

> 本文档为 `crafting-ai-video-shot-prompts` v0.2.0 收尾的 PR 描述。
> 真实环境创建 PR：
> ```bash
> gh pr create --title "feat: v0.2.0 — 5 new style presets + cross-platform scripts + pytest + CI" --body-file docs/PR_v0.2.0.md
> ```

## 动机 Motivation

v0.1 收尾后发现三大问题：

1. **macOS / Linux 不可用**：`assets/transcribe.py` 和 `assets/merge_text.py` 硬编码 Windows 路径 `c:\Users\wayhow\...`，跨平台直接 crash。
2. **零测试 / 零 CI**：v0.1 完全没有 `tests/`，无 `pytest`，无 GitHub Actions；`scripts/validate_prompt.py` 行为变化无保护。
3. **5 套预设缺位**：CHANGELOG `Planned` 段已声明 `v0.2 — More style presets`，但机甲 / 古风 / 港片 / 北欧冷调 / 复古港片 5 套未交付。

本 PR 一次性把上述 3 类问题修复/补齐，并把 10 套预设扩到 15 套（达成 v0.2.0 完整里程碑）。

## 改动列表 Changes

### Added

**预设与文档**：
- 5 套新风格预设（`templates/style-presets.md`）：机甲 / 机甲战、古风 / 国风、港片 / 霓虹九龙、北欧冷调、复古港片（80s）
- 关键词库 5 个新分类（`references/keyword-library.md`）
- `references/prompt-quality-checklist.md`：12 条可勾选质量清单
- `docs/verify-v0.2-log.md`：v0.2 验证日志

**工程化**：
- `install.sh` / `install.ps1`：跨平台一键安装脚本（替换 INSTALL.md 模板占位）
- `scripts/ci_local.sh`：本地一键复刻 CI（pytest + shellcheck + Python 语法 + 3 模板自检 + bash 语法）
- `tests/test_validate_prompt.py`：**27 个单元测试**覆盖 9 大类规则 + 边界 + CLI
- `tests/test_regression.py`：**14 个回归测试**对比 3 套模板 vs v0.1 baseline
- `tests/test_simulate_workflow.py`：**3 个端到端测试**模拟"写→检→修→检"循环
- `pyproject.toml`：最小化 pytest 配置
- `.github/workflows/ci.yml`：Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13 矩阵跑 pytest

**Frontmatter**：
- `SKILL.md` description 升级为中英双语（1005 字节 < 1024 上限）
- 新增 `keywords:` 字段（12 个英文关键词）

### Changed

- `scripts/validate_prompt.py` 升级到 v0.2：
  - 三大段标题必须用 `【】` 包裹（不再接受"基础设定：xxx"等无【】写法）
  - 新增三大段顺序校验（基础设定 → 氛围画质 → 画面内容）
  - 新增 `--strict` / `--min-chars` / `--max-chars` CLI 参数
  - 参考图描述正则加固
- `assets/transcribe.py` / `assets/merge_text.py` 改为 CLI 参数化 + 环境变量回退
- `templates/single-shot.md` 检验清单字数与脚本对齐
- `INSTALL.md` 改为引用真实脚本
- `README.md`：徽章加 CI；预设数 10→15；新增"本地复刻 CI"指引
- `INDEX.md`：统计数更新

### BREAKING CHANGES ⚠️

1. `scripts/validate_prompt.py` 不再接受"基础设定：xxx"等无【】大节标题
2. `assets/transcribe.py` 必须通过 `--audio` 或环境变量 `AUDIO` 显式传入
3. `assets/merge_text.py` 同上（`--src` / `--dst` / `MERGE_SRC` / `MERGE_DST`）

详见 [CHANGELOG.md](../../CHANGELOG.md) `[0.2.0]` 段。

### Docs

- `CHANGELOG.md` 新增 `[0.2.0] - 2026-06-07` 段，含 Added / Changed / BREAKING / Notes
- `README.md` 路线图 v0.1 / v0.2 标记为 `[x]`，并标注日期
- `INDEX.md` 统计段更新
- 新增 `docs/PR_v0.2.0.md`（本文件）+ `docs/NEXT_STEPS.md`（v0.3/0.4/1.0 设计草稿）

## 测试矩阵 Test Matrix

| 测试类型 | 用例数 | 命令 | 状态 |
| --- | --- | --- | --- |
| 单元测试（v0.2 行为） | 27 | `pytest tests/test_validate_prompt.py -v` | ✅ 全过 |
| 回归测试（3 模板 vs baseline） | 14 | `pytest tests/test_regression.py -v` | ✅ 全过 |
| 端到端模拟（写→检→修→检） | 3 | `pytest tests/test_simulate_workflow.py -v` | ✅ 全过 |
| 3 套提示词模板自检 | 3 | `python scripts/validate_prompt.py templates/*.md` | ✅ 全部 [OK]，issues = 0 |
| 本地 CI 复刻 | 8 步 | `bash scripts/ci_local.sh` | ✅ 8/8 |
| GitHub Actions CI | 矩阵 5×N | push 后自动跑 | 等待 push 后首次验证 |

**总计**：47 个测试 + 8 步本地检查 + 5 个 Python 版本 CI 矩阵。

## 风险与回滚 Risk & Rollback

### 风险 1：BIGGEST — validate_prompt.py 三大段别名收紧（BREAKING）

**影响面**：使用 v0.1 时若提示词用 `基础设定：` 而非 `【基础设定】`，v0.2 会判为"基础设定缺失"。

**回滚方案**：单 PR revert `scripts/validate_prompt.py` 到 v0.1 版本即可恢复（无其他文件依赖变更）。PR：`git revert <this-pr-sha>`。

**降低风险**：
- CHANGELOG 明确标记 BREAKING
- 本 PR 升级指引（见下）含 sed 一键迁移命令
- 升级用户的 3 套仓库内模板已迁好

### 风险 2：transcribe.py 入口变更（BREAKING）

**影响面**：直接 `python assets/transcribe.py` 不再"自动"指向桌面某路径，而是直接 ERROR 退出。

**回滚方案**：同风险 1。

**降低风险**：
- 错误信息明确指引 `--audio` 用法
- 同步支持 `AUDIO` 环境变量

### 风险 3：CI 首次跑矩阵慢

**影响**：Python 3.9 / 3.10 / 3.11 / 3.12 / 3.13 × pytest 完整跑 ≈ 3-5 分钟。

**回滚**：把 `.github/workflows/ci.yml` 的矩阵改为 `["3.11", "3.12"]` 即可。

## 升级指引 Upgrade Guide（v0.1 → v0.2）

> 任何 v0.1 用户升级到 v0.2.0 必须执行以下 3 步：

### Step 1: 迁移大节标题（最重要）

把提示词中的大节标题从无【】写法改为【】包裹：

```bash
# 仓库内一键迁移（GNU sed）：
find . -name "*.md" -type f -exec sed -i \
  -e 's/^基础设定：$/【基础设定】/g' \
  -e 's/^氛围画质：$/【氛围画质】/g' \
  -e 's/^画面内容：$/【画面内容】/g' \
  {} \;

# macOS 用户（BSD sed）：
find . -name "*.md" -type f -exec sed -i '' \
  -e 's/^基础设定：$/【基础设定】/g' \
  -e 's/^氛围画质：$/【氛围画质】/g' \
  -e 's/^画面内容：$/【画面内容】/g' \
  {} \;
```

### Step 2: 修正 transcribe.py 入口

```bash
# v0.1（不再支持）：
python assets/transcribe.py    # ❌ 退出码 2

# v0.2（推荐）：
python assets/transcribe.py --audio /path/to/audio.wav    # ✅
# 或
AUDIO=/path/to/audio.wav python assets/transcribe.py      # ✅
```

### Step 3: 跑新测试验证

```bash
pip install pytest
pytest tests/ -v
# 期望：47 passed
```

## 验收 Checklist

- [x] v0.2 既有 27 个单元测试全过
- [x] 14 个回归测试全过（3 套模板 vs baseline）
- [x] 3 个端到端测试全过
- [x] `bash scripts/ci_local.sh` 8 步全过
- [x] 3 套仓库内提示词模板在 v0.2 自检下仍 [OK]
- [x] BREAKING 段在 CHANGELOG 明确标注
- [x] Upgrade Guide 三步迁移可一键执行
- [x] CREDITS.md / 三大段方法论 / 关键词库 / 模板原 10 套风格预设 未改

详细核查见 [.trae/specs/audit-and-roadmap/checklist.md](../.trae/specs/audit-and-roadmap/checklist.md) 与 [.trae/specs/verify-and-pr/checklist.md](../.trae/specs/verify-and-pr/checklist.md)。

## 下一步 Next Steps

- v0.3 — 多分镜节奏自动分配（见 [NEXT_STEPS.md](NEXT_STEPS.md)）
- v0.4 — 提示词质量评分（LLM-as-judge）
- v1.0 — 平台 API 对接（即梦 / Vidu / 可灵 / Sora / Runway）

## 创建 PR 命令

```bash
# 提交并推送
git add .
git commit -m "release: v0.2.0 — 5 new style presets + cross-platform scripts + pytest + CI"
git push origin v0.2.0

# 创建 PR（使用本文件作为 body）
gh pr create \
  --title "feat: v0.2.0 — 5 new style presets + cross-platform scripts + pytest + CI" \
  --body-file docs/PR_v0.2.0.md \
  --base main
```
