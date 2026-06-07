# 交付清单与使用说明

> ⚠️ **本文件是开发阶段的工作清单，不是 GitHub 仓库的正式文档。**
> 仓库上传 GitHub 时以 [README.md](README.md) + [CREDITS.md](CREDITS.md) + [LICENSE](LICENSE) 为准。
> 完整视频转录（`transcript.*`）和音频（`audio_*.wav`）已通过 [.gitignore](.gitignore) 排除，**不会进入仓库**。

## 📦 完整文件树（开发态）

```
ai-video-shot-prompt-skill/
├── SKILL.md                           # ⭐ 主入口：触发条件 + 工作流 + 三大部分速查
├── README.md                          # GitHub 仓库主页（含徽章、演示、致谢）
├── CREDITS.md                         # 致谢与引用列表（核心版权声明）
├── LICENSE                            # MIT + 第三方归属声明
├── CHANGELOG.md                       # 版本变更记录
├── INSTALL.md                         # 安装到 .trae/skills/ 的步骤
├── INDEX.md                           # 本文件：开发态交付清单
├── .gitignore                         # 排除 transcript 与 audio 产物
│
├── references/                        # 详细参考（按需加载）
│   ├── framework.md                   # 三大部分逐项详解
│   ├── keyword-library.md             # 风格/限制/设备/色调关键词库
│   ├── camera-and-composition.md      # 景别/构图/运镜完整清单
│   ├── workflow-and-storyboard.md     # 小云雀短剧 Agent 2.0 工作流
│   ├── post-production.md             # 后期剪辑技巧（动作匹配/调色/光影）
│   └── examples.md                    # 视频中的完整示例（鸵鸟/机器人/别墅）
│
├── templates/                         # 提示词模板
│   ├── single-shot.md                 # 单镜头模板
│   ├── multi-shot.md                  # 多分镜模板
│   ├── action-scene.md                # 动作场景模板（含完整机器人 vs 丧尸示例）
│   └── style-presets.md               # 15 种风格预设（原子朋克/赛博朋克/水墨/机甲/古风…）
│
├── scripts/
│   └── validate_prompt.py             # 提示词结构自检脚本
│
└── assets/                            # 工具脚本（不包含视频素材）
    ├── transcribe.py                  # faster-whisper 转录脚本（供用户自行从源视频生成）
    └── merge_text.py                  # 转录段落合并工具
```

## 🔒 排除的本地文件（不进 GitHub）

以下文件本地保留供开发调试，**通过 `.gitignore` 排除，仓库内不存在**：

| 文件 | 大小 | 说明 |
| --- | --- | --- |
| `assets/transcript.txt` | ~40 KB | 完整视频转录（带时间戳） |
| `assets/transcript.json` | ~104 KB | 转录 JSON |
| `assets/transcript.srt` | ~49 KB | 字幕文件 |
| `assets/transcript_纯文本.txt` | ~34 KB | 合并段落纯文本 |
| `assets/audio_16k_mono.wav` | ~82 MB | 提取的 16kHz 单声道音频 |

排除原因：见 [CREDITS.md](CREDITS.md) 的「本 skill **不**包含的内容」一节。

## 🚀 快速开始（GitHub 仓库用法）

### 阅读顺序

1. 打开 [README.md](README.md) 了解 skill 做什么
2. 看 [CREDITS.md](CREDITS.md) 了解版权与归属
3. 看 [SKILL.md](SKILL.md) 学习三大部分框架
4. 按 [INSTALL.md](INSTALL.md) 安装到 Trae / Claude Code

### 触发语（在 Trae 中）

- "帮我写一个 AI 视频提示词"
- "我要做一个原子朋克丧尸清道夫的镜头"
- "为即梦 / Vidu / 可灵写一段动作戏"
- "评审我这个 AI 视频提示词"
- "如何降低生成画面的 AI 味？"

### 自检提示词

```bash
python scripts/validate_prompt.py my_prompt.txt
```

## 🎯 视频技巧清单（已整合进 skill）

### 核心方法论
- ✅ **三大部分框架**：基础设定 + 氛围画质 + 画面内容（顺序敏感）
- ✅ **去 AI 味三件套**：超写实 + 极致逼真 + 真人实景拍摄
- ✅ **限制词反向约束**：杜绝游戏CG感、动作僵硬、塑料皮肤、镜头漂移
- ✅ **怎么做 / 为什么 / 效果** 三段式动作描述

### 创作流程
- ✅ **5 步工作流**：收集输入 → 三大部分起草 → 去 AI 味 → 选景别/构图/运镜 → 输出+自检
- ✅ **多轮迭代**：AI 出初版 → 人工细化分镜 → 补首尾 → 加限制
- ✅ **抽卡常态**：5-10:1 的素材/成片比，200+ 候选 vs 最终使用
- ✅ **AI 当伙伴**：不命令而指引，给"为什么"建立因果链

### 技术要点
- ✅ **参考图必描述**：上传参考图前用 1-2 句描述内容
- ✅ **声音限制**：C-Dance 类自动配乐平台必须显式禁用 BGM
- ✅ **景别/构图/运镜**：完整清单与适用场景
- ✅ **多分镜时长比重**：用分数（如 1/5）而非绝对秒数
- ✅ **武戏具体化**：把"打"改成"左拳摆击头部 + 右腿横扫膝盖"

### 后期制作
- ✅ **字幕不被遮挡**：人物图层在字幕之上
- ✅ **动作匹配转场**：跨镜头人物动作方向一致
- ✅ **运镜方向一致**：所有镜头统一推拉方向
- ✅ **空间一致性**：太阳/光影方向、旗杆/标志物
- ✅ **速度微调**：动作戏 +0.1-0.2 倍
- ✅ **调色统一**：色彩克隆 + 细微调整
- ✅ **发光效果**：Bloom / Glow 提升电影感

## 📊 统计

| 指标 | 数值 |
| --- | --- |
| 文件总数（开发态） | 31 |
| 仓库实际文件（上传 GitHub 后） | 27 |
| 总大小（开发态） | ~520 KB |
| 仓库实际大小 | ~325 KB |
| Markdown 文档 | 16 |
| Python 脚本 | 3（validate_prompt / transcribe / merge_text） |
| 单元测试 | 27 个（`tests/test_validate_prompt.py`） |
| 源数据（开发态，不上传） | 5 |
| 视频时长（源） | 42 分 53 秒 |
| 视频转录字数（仅本地） | ~12,000 中文字 |
| 视频转录段数（仅本地） | 371 |
| 风格预设数 | 15（v0.1 原 10 + v0.2 追加 5） |
| 提示词模板数 | 4（含完整示例） |
| 自检规则数 | 9 大类 / 100+ 关键词 |

## ✅ 完成状态

- [x] 系统搜索并分析 skill 标准结构（Anthropic 官方 + claudeskills.info 最佳实践）
- [x] 整合视频中所有技巧
- [x] 创建 `crafting-ai-video-shot-prompts` skill
- [x] 包含完整工作流 + 三大部分框架 + 关键词库 + 模板 + 自检脚本
- [x] 自检脚本通过测试（10/10 项）
- [x] 版权风险评估：完整转录排除 + .gitignore 过滤
- [x] CREDITS.md / LICENSE / CHANGELOG / .gitignore 全部就位
- [x] README.md 重写为 GitHub 仓库风格（专业 + 蹭热度）
- [x] 所有内容放入工作区新文件夹 `ai-video-shot-prompt-skill/`

## 🔗 引用

- **原始视频**：[BV1xuVC6AEbg](https://www.bilibili.com/video/BV1xuVC6AEbg/) — Mx-Shell《丧尸清道夫》创作思路分享
- **UP 主主页**：[space.bilibili.com/388217494](https://space.bilibili.com/388217494)
- **Skill 设计参考**：[Anthropic Agent Skills 官方文档](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)、[The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)、[claudeskills.info 最佳实践](https://claudeskills.info/blog/agent-skills-best-practices/)
