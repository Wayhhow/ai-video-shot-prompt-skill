# Contributing to Crafting AI Video Shot Prompts

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to this project. These are guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

---

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the [existing issues](../../issues) to see if the problem has already been reported. When you create a bug report, please include as many details as possible by using the [Bug Report template](../../issues/new?template=bug_report.yml).

**A good bug report should include:**
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, AI video platform used)
- Any relevant prompt text

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](../../issues). When creating an enhancement suggestion:

- Use a clear, descriptive title
- Describe the use case and why this enhancement would be useful
- Explain your proposed solution, if you have one
- List alternative solutions you've considered

Use the [Feature Request template](../../issues/new?template=feature_request.yml).

### Contributing New Style Presets (本项目特色)

One of the most valuable contributions is adding new style presets to `templates/style-presets.md`. A good preset should include:

1. **Style core** (3–5 keywords): Core aesthetic direction
2. **De-AI-flavor keywords** (2–3): Mandatory additions like `photorealistic, ultra-realistic`
3. **Constraint words** (3–5): Anti-patterns to eliminate, e.g., `eliminate game-CG feel`
4. **Base equipment** (1 device): e.g., `ARRI Alexa 65, 35mm lens`
5. **Atmosphere** (1 sentence): Contrast or mood description
6. **Color grade** (1 sentence): Grade description like `teal & orange contrast`

**Each preset should be tested against the self-check:**
```bash
python scripts/validate_prompt.md
```

### Improving Documentation

Documentation improvements are always welcome. This includes:
- Fixing typos or unclear explanations
- Adding more examples or use cases
- Translating documentation (see [Translation Guide](#translation-guide) below)
- Adding comments to scripts for clarity

### Pull Request Process

1. **Fork** the repo and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-preset
   # or
   git checkout -b fix/typo-in-framework
   ```

2. **Make your changes** and ensure they meet our quality standards:
   - New style presets must pass `validate_prompt.py`
   - New Python code must pass existing `pytest tests/`
   - Documentation updates should be checked for formatting consistency

3. **Update relevant files** if your changes affect:
   - Templates → ensure `CHANGELOG.md` is updated
   - Scripts → ensure `tests/` are updated accordingly
   - Documentation → mirror changes in both `README.md` and `README.en.md` if user-facing

4. **Commit your changes** with a clear commit message:
   ```
   preset: add Studio Ghibli animation style preset
   
   - 5 style core keywords: Ghibli, hand-drawn, pastoral, warm tones
   - De-AI: photorealistic, hand-drawn quality
   - Constraints: eliminate CGI feel, eliminate modern elements
   - Equipment: Arri Alexa with soft filters
   - Tested: validate_prompt.py passes
   ```

5. **Open a Pull Request** using our [PR template](.github/PULL_REQUEST_TEMPLATE.md). Fill out all sections.

6. **Address review feedback** — maintainers will review and may suggest changes.

---

## Development Setup

### Prerequisites

- Python 3.9+
- Git

### Getting Started

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-video-shot-prompt-skill.git
cd ai-video-shot-prompt-skill

# Run the self-check on example prompts
python scripts/validate_prompt.py references/examples.md

# Run tests
pytest tests/
```

### Running Validation

After making changes to templates or prompt examples:

```bash
# Single prompt validation
python scripts/validate_prompt.py templates/single-shot.md

# Strict mode (treats warnings as errors)
python scripts/validate_prompt.py templates/action-scene.md --strict

# Custom character range (for multi-shot)
python scripts/validate_prompt.py templates/multi-shot.md --min-chars 200 --max-chars 3000
```

### Local CI Reproduction

To verify your changes match CI expectations without pushing:

```bash
bash scripts/ci_local.sh
```

This runs 8 checks: pytest + shellcheck + Python syntax + 3 template self-checks + 2 bash syntax.

---

## Style Guides

### Markdown Style

- Use ATX-style headers (`#`, `##`, not underline style)
- Code blocks should specify the language: ` ```python `, ` ```bash `, ` ```text `
- Tables are preferred for structured comparisons
- One blank line before and after headers and lists
- Chinese text should use full-width punctuation

### File Naming

- Use lowercase with hyphens: `new-style-preset.md`
- Chinese filenames are acceptable for content files: `分镜示例.md`
- Scripts keep English names: `validate_prompt.py`

### Commit Messages (recommended format)

```
<type>: <description>

<optional body>
```

**Types:**
- `preset:` — New style preset added
- `template:` — Changes to prompt templates
- `fix:` — Bug fix
- `docs:` — Documentation only changes
- `test:` — Adding or updating tests
- `ci:` — CI configuration changes
- `refactor:` — Code refactoring without behavior change

**Language:** Commit messages are primarily in Chinese (中文) but English is also welcome.

### Python Style

- Follow PEP 8
- Maintain Python 3.9+ compatibility (avoid 3.10+ specific syntax)
- Use type hints where appropriate
- Docstrings for public functions

---

## Translation Guide

This project maintains bilingual documentation (Chinese + English). Chinese is the canonical version.

### Current Translation Status

| File | Chinese | English |
|------|---------|---------|
| README.md | Complete | :new: README.en.md |
| SKILL.md | Complete | Partial (frontmatter) |
| references/ | Complete | :x: Intentionally not translated |
| templates/ | Complete | :x: Intentionally not translated |
| CONTRIBUTING.md | :x: This file is English-only | Complete |
| INSTALL.md | Complete | :x: Pending |
| CHANGELOG.md | Complete | :x: Pending |

### How to Contribute Translations

1. Fork the repo and create a translation branch
2. Copy the source file to the target language version
3. Translate content, preserving formatting and structure
4. Add a note at the top: "This is a translation. The Chinese version is canonical."
5. Update this Translation Status table in CONTRIBUTING.md
6. Open a PR

---

## Project-Specific Contribution Areas (优先级排序)

We especially welcome contributions in these areas:

1. **More style presets** — Different genres (anime, watercolor, product ads, etc.)
2. **Multi-language prompt output** — Generating English prompts from the Chinese framework
3. **Card-draw statistics tool** — Track actual success rate of prompts generated by this skill
4. **Example gallery** — Links to finished videos made with this skill
5. **Web UI** — Interactive prompt builder
6. **Video platform integrations** — Templates for 即梦, Vidu, 可灵, Sora, Runway, etc.

---

## Recognition

Contributors who make significant additions will be listed in the project's README (with permission). Quality contributions include:

- New, well-tested style presets
- Bug fixes or script improvements
- Documentation improvements or translations
- Enthusiastic community participation

---

## Questions?

If you have questions, feel free to:
- Open a [Discussion](../../discussions)
- Open an issue with the "question" label

We're happy to help you get started!

---

*This contributing guide is adapted from best practices in the open-source community. Thank you for helping make this project better!*
