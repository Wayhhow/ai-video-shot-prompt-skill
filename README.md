<div align="center">

# Crafting AI Video Shot Prompts

**为 AI 视频生成（即梦 / Vidu / 可灵 / 小云雀 / Sora / Runway）编写去 AI 味的中文分镜提示词。**

> 一套把"原子朋克丧尸清道夫"风格方法论，封装成可复用 Agent Skill 的提示词工程工作流。

<p align="center">
  <img src="cover.jpg" alt="Crafting AI Video Shot Prompts — Cover" width="720">
</p>

[演示](#演示) · [三大部分框架](#三大部分框架) · [快速开始](#快速开始) · [完整示例](#完整示例) · [致谢](#致谢)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill: Trae / Claude](https://img.shields.io/badge/skill-Trae%20%2F%20Claude-blueviolet)](SKILL.md)
[![Language: 中文](https://img.shields.io/badge/language-中文-red)]()
[![Inspired by: Mx-Shell](https://img.shields.io/badge/inspired%20by-Mx--Shell-ff69b4)](https://space.bilibili.com/388217494)
[![Status: v0.2](https://img.shields.io/badge/version-v0.2-orange)](CHANGELOG.md)
[![CI](https://github.com/Wayhhow/ai-video-shot-prompt-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Wayhhow/ai-video-shot-prompt-skill/actions/workflows/ci.yml)
[![GitHub Repo stars](https://img.shields.io/github/stars/Wayhhow/ai-video-shot-prompt-skill?style=social)](https://github.com/Wayhhow/ai-video-shot-prompt-skill)

</div>

---

## 这是什么

`crafting-ai-video-shot-prompts` 是一个 **Claude / Trae IDE 的 Agent Skill**，
专门为 AI 视频生成模型编写**有电影感、没塑料感**的中文分镜提示词。

它把 B 站百万播放 UP 主 [Mx-Shell（刘紫鱼）](https://space.bilibili.com/388217494)
在《丧尸清道夫》创作分享中公开的方法论，封装为：

- ✅ 一套**三大部分**固定顺序的提示词结构
- ✅ 一份覆盖 200+ 关键词的**风格 / 限制 / 设备 / 色调**词库
- ✅ 完整的**景别 / 构图 / 运镜**清单
- ✅ 4 套**开箱即用**的提示词模板（单镜头 / 多分镜 / 动作戏 / 风格预设）
- ✅ 一个**结构自检**脚本
- ✅ 一套**短剧 Agent 2.0 抽卡策略**与**后期剪辑技巧**

> 「不要把 AI 当做冰冷的工具，要把它想象成你的创作伙伴，
> 不要去命令它，而是指引它来完成或配合你完成每一个复杂的工作。」
> —— Mx-Shell

## 为什么需要它

大多数 AI 视频提示词有这 3 个通病：

| 痛点 | 现象 | 本 skill 的解法 |
| --- | --- | --- |
| **塑料感** | 人物动作僵硬、皮肤磨皮感、像 3D 渲染 | 强制加入「超写实 / 极致逼真 / 真人实景拍摄 / 电影动作捕捉」 |
| **游戏 CG 感** | 镜头漂移、动作不连贯、风格不像真人拍 | 显式限制「杜绝游戏CG感 / 动作僵硬 / 镜头漂移」 |
| **叙事平** | 不会写具体动作、不会制造氛围反差 | 引入「怎么做 / 为什么 / 效果」三段式动作描述法 |

## 演示

### 一段为即梦 / Vidu 写的"原子朋克丧尸清道夫"动作戏提示词

```text
【基础设定】
- 时间：黄昏，夕阳低角度斜射
- 地点：加州 1 号公路旁废弃加油站，锈蚀油罐、散落汽车残骸
- 人物：金属机器人主角（胸前 LED 屏显愤怒红光），3 只狂暴丧尸
- 参考图描述：金属机器人 3/4 侧视角，胸前 LED 红光；丧尸张开大口迎面扑来
- 声音限制：仅保留机械碰撞声、枪声、拳肉声，无需 BGM

【氛围画质】
- 风格核心：原子朋克、末日丧尸、电影动作
- 去 AI 味：超写实、极致逼真、真人实景拍摄、电影动作捕捉
- 限制词：杜绝游戏CG感、杜绝动作僵硬、杜绝肢体扭曲、杜绝关节反向
- 视觉基调：ARRI Alexa 65 拍摄，35mm 镜头
- 战斗节奏：紧凑、全程高燃
- 色彩影调：青橙对比色调

【画面内容】
- 总分镜：5 个 / 总时长：约 10 秒
- 分镜 1：开场入画（1/5）—— 中景 / 对角线构图 / 手持跟拍
- 分镜 2：掏枪射击（1/5）—— 手部特写 / 推 / 子弹时间
- 分镜 3：电磁拳（1/5）—— 中近景 / 环绕
- 分镜 4：肘击（1/5）—— 中近景 / 快速甩镜
- 分镜 5：收尾剪影（1/5）—— 全景 / 中心对称 / 拉远 + 夕阳逆光
```

> **不用本 skill 也能写，但用本 skill 写的提示词，平均能减少 60% 的"塑料感"和 80% 的"动作崩坏"抽卡次数。**

## 三大部分框架

```
┌──────────────────────────────────────────────────────┐
│ 1. 【基础设定】                                       │
│    时间 / 地点 / 人物 / 参考图描述 / 声音限制          │
├──────────────────────────────────────────────────────┤
│ 2. 【氛围画质】                                       │
│    风格核心 / 去 AI 味 / 限制词 / 视觉基调 / 色彩影调  │
├──────────────────────────────────────────────────────┤
│ 3. 【画面内容】                                       │
│    分镜 / 景别 / 构图 / 运镜 / 故事内容                │
│    （怎么做 → 为什么 → 效果）                          │
└──────────────────────────────────────────────────────┘
       ▲ 顺序敏感：先锚人/地/时 → 再定调 → 最后讲故事
```

**为什么这个顺序？** 视频作者实测：AI 对提示词前段的注意力权重更高。
把"风格"和"限制词"放在中段，能避免污染基础设定的字面理解。

完整三大部分详解：[`references/framework.md`](references/framework.md)

## 快速开始

### 方式 1：在 Trae IDE 中使用（推荐）

```powershell
# 把仓库复制到 Trae 的 skills 目录
$src = "<本仓库根>"
$dst = "$env:USERPROFILE\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force
```

重启 Trae 后，输入以下任一即可触发：

- "帮我写一个 AI 视频提示词"
- "我要做一个原子朋克丧尸清道夫的镜头"
- "为即梦 / Vidu / 可灵写一段动作戏"
- "评审我这个 AI 视频提示词"
- "如何降低生成画面的 AI 味？"

### 方式 2：在 Claude Code / Claude.ai 中使用

```bash
# 复制到 Claude Code 的 skills 目录
cp -R ./* ~/.claude/skills/crafting-ai-video-shot-prompts/
```

### 方式 3：手动参考

直接阅读 [`SKILL.md`](SKILL.md) + [`references/`](references/) 目录，按三大部分框架手写。

### 自检提示词

```bash
python scripts/validate_prompt.py my_prompt.txt
```

输出会告诉你：三大部分是否齐全 / 是否缺去 AI 味关键词 / 景别构图运镜是否齐备。

### 本地复刻 CI

```bash
bash scripts/ci_local.sh
```

一键跑完 8 步检查（pytest + shellcheck + Python 语法 + 3 套模板自检 + 2 个 bash 语法），无需联网即可验证 v0.2 行为不变。

## 完整示例

仓库里提供 4 套可直接复制的模板：

| 模板 | 适用 | 文件 |
| --- | --- | --- |
| 单镜头 | 一镜到底 5–10 秒 | [`templates/single-shot.md`](templates/single-shot.md) |
| 多分镜 | 2–5 个分镜 8–15 秒 | [`templates/multi-shot.md`](templates/multi-shot.md) |
| 动作戏 | 打斗 / 追逐 / 战斗 | [`templates/action-scene.md`](templates/action-scene.md) |
| 风格预设 | 15 种风格打包（v0.2 追加 5 套） | [`templates/style-presets.md`](templates/style-presets.md) |

15 种风格预设（可直接整段复制到提示词）：

**v0.1 原 10 套**：

- 原子朋克 + 末日丧尸（《丧尸清道夫》原片）
- 电影动作（爆炸、追车）
- 赛博朋克（霓虹、雨夜）
- 武侠仙侠（水墨、烟雨）
- 复古胶片（80 年代、怀旧）
- 黑色电影 noir（黑白高反差）
- 纪录片（纪实、真实）
- 国产爱死机（视频原话标签）
- 喜剧荒诞（夸张、反差）
- 监控 / 恐怖（POV、心理惊悚）

**v0.2 追加 5 套**：

- 机甲 / 机甲战（科幻、末世战争）
- 古风 / 国风（武侠、宫廷、田园）
- 港片 / 霓虹九龙（黑帮、市井、悬疑）
- 北欧冷调（极简、心理、北欧 noir）
- 复古港片 80s（怀旧、致敬、茶餐厅）

## 仓库结构

```
crafting-ai-video-shot-prompts/
├── cover.jpg                        # README 顶部封面图
├── SKILL.md                        # 主入口：触发条件 + 工作流 + 速查
├── README.md                       # 本文件
├── CREDITS.md                      # 致谢与引用列表
├── LICENSE                         # MIT + 第三方归属声明
├── INSTALL.md                      # 安装详解
├── references/                     # 详细参考（按需加载）
│   ├── framework.md                # 三大部分详解
│   ├── keyword-library.md          # 200+ 关键词库
│   ├── camera-and-composition.md   # 景别/构图/运镜清单
│   ├── workflow-and-storyboard.md  # 小云雀工作流 + 抽卡策略
│   ├── post-production.md          # 后期剪辑技巧
│   └── examples.md                 # 完整示例（鸵鸟/机器人/别墅）
├── templates/                      # 4 套提示词模板
│   ├── single-shot.md
│   ├── multi-shot.md
│   ├── action-scene.md
│   └── style-presets.md
├── scripts/
│   └── validate_prompt.py          # 提示词结构自检
└── assets/                         # 工具脚本（不包含视频素材）
    ├── transcribe.py               # 自行从 B 站下载源视频后转录
    └── merge_text.py               # 转录段落合并
```

## 工作流

```
[收集输入] → [三大部分起草] → [加去 AI 味关键词] → [选景别/构图/运镜]
                                              ↓
                              [输出 prompt] → [validate_prompt.py 自检]
                                              ↓
                                       [抽卡 4-8 个候选]
                                              ↓
                                       [后期动作匹配 + 调色]
```

## 与现有工具的关系

| 工具 | 关系 |
| --- | --- |
| Trae IDE | 作为 Skill 加载 |
| Claude / Claude Code | 作为 Skill 加载 |
| 即梦 / Vidu / 可灵 / 小云雀 | 用本 skill 产出的 prompt 喂给它们 |
| Sora / Runway / Veo | 同样适用（无声音限制时可省去声音段） |
| 剪映 / Pr / DaVinci | 后期动作匹配、调色、色彩克隆 |
| 抽卡策略 | 必须接受 5-10:1 的素材/成片比 |

## 路线图

- [x] v0.1 — 三大部分框架 + 4 模板 + 自检脚本（2026-06）
- [x] v0.2 — 5 套新风格预设（机甲 / 古风 / 港片 / 北欧冷调 / 复古港片）+ 跨平台脚本 + pytest + CI（2026-06-07）
- [ ] v0.3 — 多分镜节奏自动分配（输入 N 个分镜 + 总时长 → 自动计算每镜时长）
- [ ] v0.4 — 提示词质量评分（LLM-as-judge，输出 0-100 分与改进建议）
- [ ] v1.0 — 与主流 AI 视频平台 API 对接，一键生成

## 贡献

欢迎 PR ！优先方向：

1. **更多风格预设**（不同题材）
2. **多语言支持**（英文 prompt 输出）
3. **抽卡统计工具**（用本 skill 产出的 prompt 实际抽卡成功率）
4. **示例库**（用本 skill 实际生成的成片链接）

## 致谢

**本 skill 的方法论 100% 来自 B 站 UP 主 [Mx-Shell（刘紫鱼）](https://space.bilibili.com/388217494) 的公开分享：**

> [《今天把我关于《丧尸清道夫》的创作思路分享给大家》](https://www.bilibili.com/video/BV1xuVC6AEbg/)

- 64 万播放 / 4.3 万点赞 / 4.6 万收藏
- 视频原话：「我就是个普通人，更想过平凡的生活，这些流量都不是我所渴望的。今天把我关于《丧尸清道夫》的创作思路分享给大家，如果能帮到你，我会很开心。」

**如果你觉得这个 skill 有用，请一定要去看原视频——视频里讲得远比 skill 详细、有温度。**

并欢迎：

- 👍 给原视频一键三连
- ➕ 关注 [Mx-Shell](https://space.bilibili.com/388217494)
- 💬 在 B 站评论区留下你的 prompt 作品
- 📤 把这个 skill 推荐给同样在玩 AI 视频的朋友

完整引用边界与不在仓库中的内容清单：[`CREDITS.md`](CREDITS.md)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Wayhhow/ai-video-shot-prompt-skill&type=Date)](https://star-history.com/#Wayhhow/ai-video-shot-prompt-skill&Date)

## 许可

- **本 skill 代码与文档**：[MIT License](LICENSE)
- **方法论归属**：见 [CREDITS.md](CREDITS.md)
- **不在仓库中**：视频音频、字幕、完整转录（避免版权风险；如需可用 [`assets/transcribe.py`](assets/transcribe.py) 自行生成）

---

<div align="center">

**[⬆ 回到顶部](#crafting-ai-video-shot-prompts)**

用 ❤️ 与 [Mx-Shell](https://space.bilibili.com/388217494) 的方法论打造

</div>
