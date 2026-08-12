<div align="center">

# Crafting AI Video Shot Prompts

**[中文](README.md) | [English](README-en.md)**

**Write de-AI-flavored Chinese shot-list prompts for AI video generators (即梦 / Vidu / 可灵 / 小云雀 / Sora / Runway).**

> A prompt-engineering workflow that encapsulates the "Atomic Punk Zombie Scavenger" methodology into a reusable Agent Skill.

<p align="center">
  <img src="cover.jpg" alt="Crafting AI Video Shot Prompts — Cover" width="720">
</p>

[Demo](#demo) · [Three-Part Framework](#three-part-framework) · [Quick Start](#quick-start) · [Full Examples](#full-examples) · [Credits](#credits)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skill: Trae / Claude](https://img.shields.io/badge/skill-Trae%20%2F%20Claude-blueviolet)](SKILL.md)
[![Language: 中文 / English](https://img.shields.io/badge/language-中文%20%2F%20English-red)]()
[![Inspired by: Mx-Shell](https://img.shields.io/badge/inspired%20by-Mx--Shell-ff69b4)](https://space.bilibili.com/388217494)
[![Status: v0.2](https://img.shields.io/badge/version-v0.2-orange)](CHANGELOG.md)
[![CI](https://github.com/Wayhhow/ai-video-shot-prompt-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/Wayhhow/ai-video-shot-prompt-skill/actions/workflows/ci.yml)
[![GitHub Repo stars](https://img.shields.io/github/stars/Wayhhow/ai-video-shot-prompt-skill?style=social)](https://github.com/Wayhhow/ai-video-shot-prompt-skill)

</div>

---

> **Note:** This English translation is provided for international readers. The Chinese documentation is the canonical version and may be more up-to-date. Core methodology files (`references/`, `templates/`) remain in Chinese as the keyword library is designed for Chinese-language prompts.

---

## What is it

`crafting-ai-video-shot-prompts` is an **Agent Skill for Claude / Trae IDE**, designed to write **cinematic, non-plastic-looking** Chinese shot-list prompts for AI video generation models.

It encapsulates the methodology publicly shared by Bilibili creator [Mx-Shell](https://space.bilibili.com/388217494) (640K+ views) during the "Zombie Scavenger" creation breakdown:

- A **fixed-order three-part** prompt structure
- A **200+ keyword** library covering style / constraints / equipment / color tone
- Complete **shot size / composition / camera movement** checklists
- **4 ready-to-use** prompt templates (single-shot / multi-shot / action / style presets)
- A **structural self-check** script
- A complete **short-drama Agent 2.0 card-drawing strategy** and **post-production techniques**

> "Don't treat AI as a cold tool; imagine it as your creative partner. Don't command it — guide it to accomplish or collaborate with you on every complex task."
> — Mx-Shell

## Why you need it

Most AI video prompts suffer from 3 common problems:

| Pain Point | Symptom | How this skill solves it |
| --- | --- | --- |
| **Plastic look** | Stiff character motion, airbrushed skin, 3D-render feel | Mandates "photorealistic / ultra-realistic / live-action / cinematic motion capture" |
| **Game-CG feel** | Floating camera, incoherent motion, unrealistic style | Explicit constraints "eliminate game-CG feel / stiff motion / camera drift" |
| **Flat narrative** | No specific actions, no atmospheric contrast | Introduces "how / why / effect" three-part action description |

## Demo

### An action scene prompt written for 即梦 / Vidu — "Atomic Punk Zombie Scavenger"

```text
[Basic Setup]
- Time: Dusk, low-angle sunset light
- Location: Abandoned gas station off California Highway 1, rusted oil tanks, scattered car wreckage
- Characters: Metal robot protagonist (chest LED screen showing angry red), 3 feral zombies
- Reference image description: Metal robot in 3/4 side view, chest LED red; zombies mouth-wide charging
- Sound constraints: Keep only mechanical collision, gunshots, flesh-impact sounds; no BGM

[Atmosphere & Quality]
- Style core: Atomic punk, zombie apocalypse, cinematic action
- De-AI-flavor: Photorealistic, ultra-realistic, live-action, cinematic motion capture
- Constraints: Eliminate game-CG feel, eliminate stiff motion, eliminate limb twisting, eliminate reverse joints
- Visual base: Shot on ARRI Alexa 65, 35mm lens
- Pacing: Tense, high-energy throughout
- Color: Teal & orange contrast

[Visual Content]
- Total shots: 5 / Total duration: ~10 seconds
- Shot 1: Opening entry (1/5) — Medium shot / Diagonal composition / Handheld tracking
- Shot 2: Draw & fire (1/5) — Hand detail / Push-in / Bullet time
- Shot 3: Electro-fist (1/5) — Medium close-up / Orbit
- Shot 4: Elbow strike (1/5) — Medium close-up / Whip pan
- Shot 5: Closing silhouette (1/5) — Wide / Center symmetric / Pull back + sunset backlight
```

> **You can write these without this skill, but using it reduces "plastic look" card-draws by ~60% and "motion breakage" by ~80% on average.**

## Three-Part Framework

```
┌──────────────────────────────────────────────────────┐
│ 1. [Basic Setup]                                       │
│    Time / Location / Characters / Reference / Sound    │
├──────────────────────────────────────────────────────┤
│ 2. [Atmosphere & Quality]                              │
│    Style core / De-AI / Constraints / Visual / Color   │
├──────────────────────────────────────────────────────┤
│ 3. [Visual Content]                                    │
│    Shots / Size / Composition / Movement / Story       │
│    (How → Why → Effect)                                │
└──────────────────────────────────────────────────────┘
      ▲ Order-sensitive: anchor people/place/time → set tone → tell story
```

**Why this order?** The creator's tests confirm: AI assigns higher attention weight to earlier prompt sections.
Placing "style" and "constraints" in the middle avoids polluting the literal understanding of the basic setup.

Full framework breakdown: [`references/framework.md`](references/framework.md) (Chinese)

## Quick Start

### Option 1: Use in Trae IDE (Recommended)

```powershell
# Copy repo to Trae's skills directory
$src = "<repo-root>"
$dst = "$env:USERPROFILE\.trae\skills\crafting-ai-video-shot-prompts"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item -Path "$src\*" -Destination $dst -Recurse -Force
```

Restart Trae, then type any of these triggers:

- "Help me write an AI video prompt"
- "I want to make an atomic punk zombie scavenger shot"
- "Write an action scene for 即梦 / Vidu / 可灵"
- "Review my AI video prompt"
- "How to reduce AI flavor in generated footage?"

### Option 2: Use in Claude Code / Claude.ai

```bash
# Copy to Claude Code's skills directory
cp -R ./* ~/.claude/skills/crafting-ai-video-shot-prompts/
```

### Option 3: Manual reference

Read [`SKILL.md`](SKILL.md) + [`references/`](references/) directory directly and write prompts by hand following the three-part framework.

### Self-check script

```bash
python scripts/validate_prompt.py my_prompt.txt
```

Reports: whether all three sections are present / missing de-AI keywords / shot size, composition, camera movement completeness.

### Reproduce CI locally

```bash
bash scripts/ci_local.sh
```

One command runs 8 checks (pytest + shellcheck + Python syntax + 3 template self-checks + 2 bash syntax). Verifies v0.2 behavior without internet.

## Full Examples

4 ready-to-copy templates in this repo:

| Template | Use Case | File |
| --- | --- | --- |
| Single Shot | One-take, 5–10 seconds | [`templates/single-shot.md`](templates/single-shot.md) |
| Multi-Shot | 2–5 shots, 8–15 seconds | [`templates/multi-shot.md`](templates/multi-shot.md) |
| Action Scene | Fight / chase / combat | [`templates/action-scene.md`](templates/action-scene.md) |
| Style Presets | 15 packed styles (v0.2 adds 5) | [`templates/style-presets.md`](templates/style-presets.md) |

15 style presets (copy-paste ready for your prompts):

**v0.1 original 10 presets:**

| # | Preset | Best For |
|---|--------|----------|
| 1 | Atomic Punk + Zombie Apocalypse | Wasteland, zombies, mecha, retro-futurism |
| 2 | Cinematic Action | Action, war, police-explosion scenes |
| 3 | Cyberpunk | Future cities, cybernetics, hackers |
| 4 | Wuxia / Xianxia | Martial arts, Eastern aesthetics |
| 5 | Retro Film | Nostalgia, 80s–90s, retro HK |
| 6 | Film Noir | Detective, mystery, crime, B&W high-contrast |
| 7 | Documentary | Documentary, pseudo-documentary |
| 8 | Chinese Love Death & Robots | Short drama, fantasy, Eastern spectacle |
| 9 | Comedy / Absurdist | Comedy, contrast humor |
| 10 | Surveillance / Horror | Horror, thriller, POV |

**v0.2 adds 5 presets:**

| # | Preset | Best For |
|---|--------|----------|
| 11 | Mecha / Mecha Combat | Sci-fi action, mecha vs. mecha, wasteland war |
| 12 | Ancient Chinese / Guofeng | Wuxia, court, countryside |
| 13 | HK / Neon Kowloon | Gangsters, noir, street life |
| 14 | Nordic Cold Tone | Minimalism, psychological, Nordic noir |
| 15 | 80s Retro HK | Nostalgia, 80s homage |

## Project Structure

```
crafting-ai-video-shot-prompts/
├── cover.jpg                        # Cover image
├── SKILL.md                         # Entry: triggers + workflow + quick ref
├── README.md                        # Chinese readme (canonical)
├── README.en.md                     # This file — English readme
├── CREDITS.md                       # Credits and attribution
├── LICENSE                          # MIT + third-party attribution
├── CONTRIBUTING.md                  # How to contribute
├── CODE_OF_CONDUCT.md               # Community code of conduct
├── INSTALL.md                       # Detailed installation
├── references/                      # Detailed reference (Chinese, loaded on demand)
│   ├── framework.md                 # Three-part framework deep-dive
│   ├── keyword-library.md           # 200+ keyword library
│   ├── camera-and-composition.md    # Shot / composition / movement checklist
│   ├── workflow-and-storyboard.md   # 即梦 workflow + card-draw strategy
│   ├── post-production.md           # Post-production: edit, grade, consistency
│   └── examples.md                  # Full examples (ostrich / robot / villa)
├── templates/                       # 4 prompt templates (Chinese, keyword-native)
│   ├── single-shot.md
│   ├── multi-shot.md
│   ├── action-scene.md
│   └── style-presets.md
├── scripts/
│   └── validate_prompt.py           # Prompt structure self-check
├── .github/
│   ├── workflows/ci.yml             # CI: pytest across Python 3.9–3.13
│   ├── ISSUE_TEMPLATE/              # Bug report / feature request templates
│   └── PULL_REQUEST_TEMPLATE.md     # PR template
└── assets/                          # Utility scripts
    ├── transcribe.py                # Transcribe source Bilibili video
    └── merge_text.py                # Merge transcript paragraphs
```

## Workflow

```
[Gather Input] → [Draft Three Parts] → [Add De-AI Keywords] → [Pick Shot/Composition/Movement]
                                              ↓
                               [Output prompt] → [validate_prompt.py self-check]
                                              ↓
                                      [Draw 4–8 candidates]
                                              ↓
                                      [Post: motion match + grade]
```

## Relationship with Other Tools

| Tool | Relationship |
| --- | --- |
| Trae IDE | Loaded as Skill |
| Claude / Claude Code | Loaded as Skill |
| 即梦 / Vidu / 可灵 / 小云雀 | Feed output prompts to these |
| Sora / Runway / Veo | Same prompts apply (omit sound segment if no auto-BGM) |
| 剪映 / Pr / DaVinci | Post: motion matching, grading, color cloning |
| Card-draw strategy | Accept 5–10:1 source-to-final ratio |

## Roadmap

- [x] v0.1 — Three-part framework + 4 templates + self-check (2026-06)
- [x] v0.2 — 5 new style presets + cross-platform scripts + pytest + CI (2026-06-07)
- [ ] v0.3 — Multi-shot auto timing allocator (input N shots + total duration → auto-calculate per-shot duration)
- [ ] v0.4 — Prompt quality scoring (LLM-as-judge, output 0–100 + suggestions)
- [ ] v1.0 — Integration with mainstream AI video platform APIs, one-click generation

## Contributing

We welcome PRs! Priority areas:

1. **More style presets** (different genres)
2. **Multilingual prompt output** (e.g., English prompt generation)
3. **Card-draw statistics tool** (actual success rate tracking)
4. **Example gallery** (links to finished videos made with this skill)

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution guidelines.

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Credits

**This skill's methodology is 100% derived from Bilibili creator [Mx-Shell](https://space.bilibili.com/388217494)'s public sharing:**

> [《今天把我关于《丧尸清道夫》的创作思路分享给大家》](https://www.bilibili.com/video/BV1xuVC6AEbg/)

- 640K plays / 43K likes / 46K favorites

**If you find this skill useful, please watch the original video — it covers far more detail, with warmth, than any text can convey.**

Also welcome:

- Upvote the original video
- Follow [Mx-Shell](https://space.bilibili.com/388217494)
- Share your prompt works in the comments
- Recommend this skill to fellow AI video creators

Full attribution boundaries and excluded content: [CREDITS.md](CREDITS.md)

## Star History

[![Star History Chart](https://api.star-history.com/chart?repos=Wayhhow%2Fai-video-shot-prompt-skill&type=date&legend=top-left)](https://www.star-history.com/?repos=Wayhhow%2Fai-video-shot-prompt-skill&type=date&legend=top-left)

## License

- **Code and documentation:** [MIT License](LICENSE)
- **Methodology attribution:** See [CREDITS.md](CREDITS.md)
- **Not in this repo:** Video audio, subtitles, full transcript (to avoid copyright risk; generate your own via `assets/transcribe.py`)

---

<div align="center">

**[Back to Top](#crafting-ai-video-shot-prompts)**

Built with love from [Mx-Shell](https://space.bilibili.com/388217494)'s methodology

</div>
