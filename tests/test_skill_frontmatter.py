"""Ensure SKILL.md stays compatible with the standard skill loader schema."""
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}


def _frontmatter():
    content = SKILL.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    assert match, "SKILL.md must contain YAML frontmatter"
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict)
    return data


def test_frontmatter_uses_only_standard_top_level_properties():
    data = _frontmatter()
    unexpected = set(data) - ALLOWED_PROPERTIES
    assert not unexpected, f"Unsupported top-level frontmatter keys: {sorted(unexpected)}"
    assert isinstance(data.get("name"), str) and data["name"]
    assert isinstance(data.get("description"), str) and data["description"]


def test_keywords_are_nested_in_metadata():
    data = _frontmatter()
    metadata = data.get("metadata")
    assert isinstance(metadata, dict)
    assert isinstance(metadata.get("keywords"), list)
    assert metadata["keywords"]
