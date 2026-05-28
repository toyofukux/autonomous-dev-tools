#!/usr/bin/env python3
"""Static validator for the autonomous-dev-tools marketplace and its plugins.

Runs in CI (no Claude install needed) and locally before push:

    python3 scripts/validate.py

Exits 0 on success, 1 on any failure. Prints findings grouped by severity.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = ROOT / "plugins"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\s*\n", re.DOTALL)
SKILL_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
AGENT_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
AD_PREFIX_RE = re.compile(r"^ad-[a-z][a-z0-9-]*$")
LINK_REF_RE = re.compile(r"\[\[([a-z0-9-]+)\]\]")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def merge(self, other: "Report") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    def ok(self) -> bool:
        return not self.errors

    def print(self) -> None:
        if self.warnings:
            print("\nWarnings:")
            for w in self.warnings:
                print(f"  · {w}")
        if self.errors:
            print("\nErrors:")
            for e in self.errors:
                print(f"  ✗ {e}")
        if self.ok() and not self.warnings:
            print("All checks passed.")
        elif self.ok():
            print(f"\n{len(self.warnings)} warning(s), no errors.")
        else:
            print(f"\n{len(self.errors)} error(s), {len(self.warnings)} warning(s).")


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    """Return a flat string-only dict of YAML frontmatter fields, or None if absent.

    Intentionally simple: we only read top-level scalar `key: value` pairs.
    Multi-line values and nested mappings are not supported (and not used here).
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        return None  # caller will report missing file
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None
    body = m.group(1)
    fields: dict[str, str] = {}
    for line in body.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        fields[key] = value
    return fields


def file_body(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        return content
    return content[m.end():]


def validate_json(path: Path, report: Report) -> dict | None:
    if not path.exists():
        report.error(f"missing: {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report.error(f"invalid JSON in {path.relative_to(ROOT)}: {e}")
        return None


def validate_marketplace(report: Report) -> dict | None:
    data = validate_json(MARKETPLACE_PATH, report)
    if data is None:
        return None
    for field_name in ("name", "owner", "plugins"):
        if field_name not in data:
            report.error(f"marketplace.json: missing required field '{field_name}'")
    owner = data.get("owner")
    if isinstance(owner, dict) and "name" not in owner:
        report.error("marketplace.json: owner.name is required")
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        report.error("marketplace.json: 'plugins' must be a list")
        return data
    if not plugins:
        report.warn("marketplace.json: no plugins listed")
    seen_names: set[str] = set()
    for i, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            report.error(f"marketplace.json: plugins[{i}] is not an object")
            continue
        name = plugin.get("name")
        if not name:
            report.error(f"marketplace.json: plugins[{i}] missing 'name'")
        elif name in seen_names:
            report.error(f"marketplace.json: duplicate plugin name '{name}'")
        else:
            seen_names.add(name)
        if "source" not in plugin:
            report.error(f"marketplace.json: plugins[{i}] ({name}) missing 'source'")
            continue
        src = plugin["source"]
        if isinstance(src, dict) and "source" in src and src["source"].startswith("./"):
            plugin_path = ROOT / src["source"].lstrip("./")
            if not (plugin_path / ".claude-plugin" / "plugin.json").exists():
                report.error(
                    f"marketplace.json: plugins[{i}] ({name}) points to {src['source']} "
                    "but no plugin.json found there"
                )
        if "version" not in plugin:
            report.warn(
                f"marketplace.json: plugins[{i}] ({name}) has no version "
                "(updates will trigger on every commit SHA)"
            )
    return data


def validate_plugin_manifest(plugin_dir: Path, report: Report) -> dict | None:
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    data = validate_json(manifest_path, report)
    if data is None:
        return None
    for field_name in ("name", "description"):
        if field_name not in data:
            report.error(f"{manifest_path.relative_to(ROOT)}: missing '{field_name}'")
    if "version" not in data:
        report.warn(f"{manifest_path.relative_to(ROOT)}: missing 'version'")
    return data


def validate_skill(skill_dir: Path, report: Report) -> str | None:
    """Validate one skill directory. Returns the skill name if valid."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        report.error(f"skill {skill_dir.relative_to(ROOT)} has no SKILL.md")
        return None
    fields = parse_frontmatter(skill_md)
    if fields is None:
        report.error(f"{skill_md.relative_to(ROOT)}: missing frontmatter block")
        return None
    if "description" not in fields:
        report.error(f"{skill_md.relative_to(ROOT)}: frontmatter missing 'description'")
    desc = fields.get("description", "")
    if desc and len(desc) < 20:
        report.warn(
            f"{skill_md.relative_to(ROOT)}: description is very short "
            f"({len(desc)} chars) — Claude uses this to decide when to invoke"
        )
    name = fields.get("name", skill_dir.name)
    if not SKILL_NAME_RE.match(name):
        report.error(
            f"{skill_md.relative_to(ROOT)}: name '{name}' must match {SKILL_NAME_RE.pattern}"
        )
    if name != skill_dir.name:
        report.error(
            f"{skill_md.relative_to(ROOT)}: name '{name}' does not match "
            f"directory name '{skill_dir.name}'"
        )
    return name


def validate_agent(agent_path: Path, report: Report) -> str | None:
    fields = parse_frontmatter(agent_path)
    if fields is None:
        report.error(f"{agent_path.relative_to(ROOT)}: missing frontmatter block")
        return None
    if "name" not in fields:
        report.error(f"{agent_path.relative_to(ROOT)}: frontmatter missing 'name'")
        return None
    if "description" not in fields:
        report.error(f"{agent_path.relative_to(ROOT)}: frontmatter missing 'description'")
    name = fields["name"]
    if not AGENT_NAME_RE.match(name):
        report.error(
            f"{agent_path.relative_to(ROOT)}: name '{name}' must match {AGENT_NAME_RE.pattern}"
        )
    expected_filename = f"{name}.md"
    if agent_path.name != expected_filename:
        report.error(
            f"{agent_path.relative_to(ROOT)}: filename should be '{expected_filename}' "
            f"to match frontmatter name"
        )
    return name


def collect_link_refs(text: str) -> set[str]:
    return set(LINK_REF_RE.findall(text))


def validate_autonomous_dev_loop(plugin_dir: Path, report: Report) -> None:
    """Plugin-specific checks for software-factory."""
    # All skills must use ad-* prefix.
    skills_dir = plugin_dir / "skills"
    skill_names: set[str] = set()
    if skills_dir.is_dir():
        for sd in sorted(skills_dir.iterdir()):
            if not sd.is_dir():
                continue
            if not AD_PREFIX_RE.match(sd.name):
                report.error(
                    f"plugin '{plugin_dir.name}': skill '{sd.name}' must match ad-*"
                )
            name = validate_skill(sd, report)
            if name:
                skill_names.add(name)

    agents_dir = plugin_dir / "agents"
    agent_names: set[str] = set()
    if agents_dir.is_dir():
        for ap in sorted(agents_dir.glob("*.md")):
            name = validate_agent(ap, report)
            if name:
                agent_names.add(name)

    # Cross-reference: [[ad-x]] in SKILL.md should resolve to an existing skill or agent.
    known = skill_names | agent_names
    if skills_dir.is_dir():
        for sd in skills_dir.iterdir():
            sm = sd / "SKILL.md"
            if not sm.exists():
                continue
            for ref in collect_link_refs(sm.read_text(encoding="utf-8")):
                if ref not in known and not ref.startswith("feedback"):
                    report.warn(
                        f"{sm.relative_to(ROOT)}: [[{ref}]] does not match any known "
                        "skill or agent name in this plugin"
                    )

    # Templates directory must contain the expected files.
    tpl_dir = plugin_dir / "templates"
    required_templates = [
        "SPEC.md.tmpl",
        "concept.md.tmpl",
        "arch.md.tmpl",
        "stories.md.tmpl",
        "decision-record.md.tmpl",
        "spec-iteration.md.tmpl",
        "CLAUDE.md.tmpl",
    ]
    for t in required_templates:
        if not (tpl_dir / t).exists():
            report.error(f"plugin '{plugin_dir.name}': missing template templates/{t}")
    guidelines_dir = tpl_dir / "guidelines"
    if guidelines_dir.is_dir():
        for g in guidelines_dir.glob("*.md"):
            if g.stat().st_size == 0:
                report.error(f"empty guideline: {g.relative_to(ROOT)}")

    # Hooks: pre-commit-secrets.json must be valid JSON if present.
    hook = plugin_dir / "hooks" / "pre-commit-secrets.json"
    if hook.exists():
        validate_json(hook, report)


def validate_no_forbidden_artifacts(report: Report) -> None:
    """Catch design-rule violations that earlier reviews said NOT to do."""
    # Forbidden: a unit-level spec.md template (the plugin explicitly opted out).
    # Use os.listdir for byte-exact comparison; .exists() is case-insensitive on macOS
    # and would false-match against SPEC.md.tmpl (the index, which IS allowed).
    tpl_dir = PLUGINS_DIR / "software-factory" / "templates"
    if tpl_dir.is_dir():
        entries = os.listdir(tpl_dir)
        if "spec.md.tmpl" in entries:
            report.error(
                "templates/spec.md.tmpl is forbidden by design — see docs/lifecycle.md"
            )
    # Forbidden: secrets-shaped files in the repo (defense in depth; pre-commit hook is primary).
    forbidden_globs = ["*.key", "*.pem", "secrets.json", "credentials.json"]
    for pattern in forbidden_globs:
        for hit in ROOT.rglob(pattern):
            if "/.git/" in str(hit) or "/node_modules/" in str(hit):
                continue
            report.error(f"forbidden file committed: {hit.relative_to(ROOT)}")


def iter_plugin_dirs() -> Iterable[Path]:
    if not PLUGINS_DIR.is_dir():
        return []
    for d in sorted(PLUGINS_DIR.iterdir()):
        if d.is_dir() and (d / ".claude-plugin" / "plugin.json").exists():
            yield d


def main() -> int:
    report = Report()
    print(f"Validating marketplace + plugins under {ROOT}\n")

    marketplace = validate_marketplace(report)

    plugin_names_in_marketplace: set[str] = set()
    if marketplace:
        plugin_names_in_marketplace = {
            p["name"] for p in marketplace.get("plugins", []) if isinstance(p, dict) and p.get("name")
        }

    for plugin_dir in iter_plugin_dirs():
        manifest = validate_plugin_manifest(plugin_dir, report)
        if manifest:
            mname = manifest.get("name")
            if mname and mname not in plugin_names_in_marketplace:
                report.warn(
                    f"plugin '{mname}' has a manifest but is not listed in marketplace.json"
                )
            if plugin_dir.name == "software-factory":
                validate_autonomous_dev_loop(plugin_dir, report)

    validate_no_forbidden_artifacts(report)

    report.print()
    return 0 if report.ok() else 1


if __name__ == "__main__":
    sys.exit(main())
