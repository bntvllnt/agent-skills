#!/usr/bin/env python3
"""Validate public Agent Skills repository invariants.

Checks:
- every top-level skill has parseable SKILL.md YAML frontmatter
- required frontmatter fields exist and `name` matches the skill folder
- local Markdown links resolve, excluding code blocks and template files
- llms.txt and llms-full.txt match deterministic generated content

Use `--write` to refresh llms.txt and llms-full.txt before validating.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    import yaml
except ImportError:  # pragma: no cover - exercised in environments missing PyYAML
    print("error: PyYAML is required. Install with: python -m pip install PyYAML", file=sys.stderr)
    sys.exit(2)


REQUIRED_FRONTMATTER_FIELDS = ("name", "description")
SKIP_DIRS = {".git", ".github", ".worktrees", "docs", "scripts"}
SKIP_MARKDOWN_DIRS = {"templates"}
ROOT_DOCS = ("README.md", "CONTRIBUTING.md", "CHANGELOG.md")
OPTIONAL_DOCS = ("SECURITY.md", "CODE_OF_CONDUCT.md", "LICENSE")
PROJECT_SUMMARY = "Collection of reusable AI agent skills — capabilities for any domain via skills.sh."
PROJECT_OVERVIEW = (
    "Agent Skills is a Markdown-based skill collection for AI coding agents. "
    "Each skill provides structured instructions that agents load on-demand to handle specific domains: "
    "code analysis, git workflows, GitHub operations, backend development, and more. "
    "Skills are agent-agnostic and work with Claude Code, OpenCode, Windsurf, Cursor, and any agent supporting SKILL.md."
)


@dataclass(frozen=True)
class Skill:
    name: str
    directory: Path
    skill_md: Path
    frontmatter: dict


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def display_name(skill_name: str) -> str:
    special = {"github": "GitHub", "oss-readiness": "OSS Readiness", "tmux": "tmux"}
    return special.get(skill_name, skill_name.replace("-", " ").title())


def compact_description(value: object) -> str:
    if not isinstance(value, str):
        return "Skill documentation"
    text = " ".join(line.strip() for line in value.strip().splitlines() if line.strip())
    return text.rstrip(".")


def split_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing closing YAML frontmatter delimiter")

    raw = text[4:end]
    body = text[end + len("\n---\n") :]
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML parse error: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("frontmatter must parse to a mapping")
    if not body.strip():
        raise ValueError("SKILL.md body is empty")
    return parsed, body


def find_skills(root: Path) -> tuple[list[Skill], list[str]]:
    skills: list[Skill] = []
    errors: list[str] = []

    for child in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS and not p.name.startswith(".")):
        skill_md = child / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            frontmatter, _body = split_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{rel(skill_md, root)}: {exc}")
            continue

        for field in REQUIRED_FRONTMATTER_FIELDS:
            value = frontmatter.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{rel(skill_md, root)}: missing or empty required field `{field}`")

        name = frontmatter.get("name")
        if isinstance(name, str) and name != child.name:
            errors.append(f"{rel(skill_md, root)}: frontmatter name `{name}` does not match folder `{child.name}`")

        description = frontmatter.get("description")
        if isinstance(description, str) and len(description) > 1024:
            errors.append(f"{rel(skill_md, root)}: description is {len(description)} chars; max is 1024")

        if isinstance(name, str):
            skills.append(Skill(name=name, directory=child, skill_md=skill_md, frontmatter=frontmatter))

    if not skills:
        errors.append("no top-level skills with SKILL.md found")
    return skills, errors


def strip_code(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in lines:
        stripped = line.lstrip()
        fence_match = re.match(r"(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[:3]
            elif marker.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            output.append("")
        elif in_fence:
            output.append("")
        else:
            # Remove inline-code spans too so examples like `[name](url)` do
            # not get mistaken for real repository links.
            output.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(output)


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        parts = set(path.relative_to(root).parts)
        if parts & SKIP_MARKDOWN_DIRS:
            continue
        if ".git" in parts or ".worktrees" in parts:
            continue
        files.append(path)

    # llms.txt and llms-full.txt are Markdown-formatted even though the
    # extension is .txt.
    for manifest in ("llms.txt", "llms-full.txt"):
        path = root / manifest
        if path.exists():
            files.append(path)
    return sorted(files)


def extract_markdown_links(markdown: str) -> list[str]:
    text = strip_code(markdown)
    links: list[str] = []

    # Inline links/images: [text](target) and ![alt](target)
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        links.append(match.group(1).strip())

    # Reference definitions: [id]: target
    for match in re.finditer(r"(?m)^\s{0,3}\[[^\]]+\]:\s+(\S+)", text):
        links.append(match.group(1).strip())

    return links


def should_skip_link(target: str) -> bool:
    if not target or target.startswith("#"):
        return True
    if any(ch in target for ch in ("{", "}", "<", ">")):
        return True
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return True
    if parsed.scheme and parsed.scheme not in {""}:
        return True
    return False


def validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for target in extract_markdown_links(text):
            if should_skip_link(target):
                continue
            parsed = urlparse(target)
            raw_path = unquote(parsed.path)
            if not raw_path:
                continue

            candidate = (path.parent / raw_path).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{rel(path, root)}: link `{target}` resolves outside repo")
                continue

            if not candidate.exists():
                errors.append(f"{rel(path, root)}: unresolved local link `{target}`")
                continue

            if parsed.fragment and candidate.is_file() and candidate.suffix.lower() in {".md", ".txt"}:
                if not has_anchor(candidate, parsed.fragment):
                    errors.append(f"{rel(path, root)}: unresolved anchor `{target}`")

    return errors


def slugify_heading(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"<[^>]+>", "", slug)
    slug = re.sub(r"[^a-z0-9 _-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug.strip("-")


def has_anchor(path: Path, fragment: str) -> bool:
    fragment = unquote(fragment).lower()
    if not fragment:
        return True
    text = path.read_text(encoding="utf-8")
    base_counts: dict[str, int] = {}
    anchors: set[str] = set()
    for match in re.finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", text):
        base = slugify_heading(match.group(1))
        if not base:
            continue
        count = base_counts.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        base_counts[base] = count + 1
    return fragment in anchors


def generate_llms_txt(root: Path, skills: list[Skill]) -> str:
    lines = [
        "# Agent Skills",
        "",
        f"> {PROJECT_SUMMARY}",
        "",
        PROJECT_OVERVIEW,
        "",
        "Install: `npx skills add bntvllnt/agent-skills`",
        "",
        "## Docs",
        "",
        "- [README](README.md): Project overview, installation, and usage guide",
        "- [Skills Overview](docs/skills-overview.md): All skills with descriptions and how they work",
        "- [Contributing](CONTRIBUTING.md): Contribution guidelines and skill structure conventions",
        "- [Changelog](CHANGELOG.md): Version history and release notes",
        "",
        "## Skills",
        "",
    ]
    for skill in skills:
        lines.append(f"- [{display_name(skill.name)}]({skill.name}/SKILL.md): {compact_description(skill.frontmatter.get('description'))}")

    lines.extend([
        "",
        "## Optional",
        "",
        "- [Security Policy](SECURITY.md): Vulnerability reporting and disclosure policy",
        "- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines",
        "- [License](LICENSE): MIT license",
        "",
    ])
    return "\n".join(lines)


def strip_trailing_whitespace(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines())


def rebase_markdown_target(target: str, source_dir: str) -> str:
    if not source_dir or should_skip_link(target):
        return target
    parsed = urlparse(target)
    if not parsed.path:
        return target
    if parsed.path.startswith("/"):
        return target

    rebased_path = (Path(source_dir) / unquote(parsed.path)).as_posix()
    while "/./" in rebased_path:
        rebased_path = rebased_path.replace("/./", "/")

    suffix = ""
    if parsed.query:
        suffix += f"?{parsed.query}"
    if parsed.fragment:
        suffix += f"#{parsed.fragment}"
    return rebased_path + suffix


def rebase_markdown_links(markdown: str, source_dir: str) -> str:
    """Rebase relative Markdown links from source_dir to repository root.

    llms-full.txt embeds content from files in nested skill folders. Relative
    links that are valid beside the original SKILL.md would be broken from the
    root-level manifest unless they are rewritten during generation.
    """

    def rewrite_segment(segment: str) -> str:
        def inline_repl(match: re.Match[str]) -> str:
            bang = match.group(1) or ""
            label = match.group(2)
            target = match.group(3)
            return f"{bang}[{label}]({rebase_markdown_target(target, source_dir)})"

        segment = re.sub(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", inline_repl, segment)

        def ref_repl(match: re.Match[str]) -> str:
            return f"{match.group(1)}{rebase_markdown_target(match.group(2), source_dir)}"

        return re.sub(r"(?m)^(\s{0,3}\[[^\]]+\]:\s+)(\S+)", ref_repl, segment)

    output: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in markdown.splitlines():
        stripped = line.lstrip()
        fence_match = re.match(r"(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[:3]
            elif marker.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue

        pieces = re.split(r"(`[^`]*`)", line)
        for index in range(0, len(pieces), 2):
            pieces[index] = rewrite_segment(pieces[index])
        output.append("".join(pieces))
    return "\n".join(output)


def read_text_if_exists(root: Path, relative_path: str) -> str | None:
    path = root / relative_path
    if not path.exists():
        return None
    return strip_trailing_whitespace(path.read_text(encoding="utf-8"))


def generate_llms_full_txt(root: Path, skills: list[Skill]) -> str:
    lines = [
        "# Agent Skills",
        "",
        f"> {PROJECT_SUMMARY}",
        "",
        PROJECT_OVERVIEW,
        "",
        "## Docs",
        "",
    ]

    for doc in ROOT_DOCS:
        content = read_text_if_exists(root, doc)
        if content is None:
            continue
        lines.extend([f"### {Path(doc).stem if doc != 'README.md' else 'README'}", f"Source: {doc}", "", content, ""])

    lines.extend(["## Skills", ""])
    for skill in skills:
        content = rebase_markdown_links(strip_trailing_whitespace(skill.skill_md.read_text(encoding="utf-8")), skill.name)
        lines.extend([f"### {display_name(skill.name)}", f"Source: {skill.name}/SKILL.md", "", content, ""])

    optional_written = False
    for doc in OPTIONAL_DOCS:
        content = read_text_if_exists(root, doc)
        if content is None:
            continue
        if not optional_written:
            lines.extend(["## Optional", ""])
            optional_written = True
        lines.extend([f"### {Path(doc).stem.replace('_', ' ').title()}", f"Source: {doc}", "", content, ""])

    return "\n".join(lines).rstrip() + "\n"


def validate_llms(root: Path, skills: list[Skill], write: bool) -> list[str]:
    expected = {
        "llms.txt": generate_llms_txt(root, skills),
        "llms-full.txt": generate_llms_full_txt(root, skills),
    }

    if write:
        for name, content in expected.items():
            (root / name).write_text(content, encoding="utf-8")
        return []

    errors: list[str] = []
    for name, expected_content in expected.items():
        path = root / name
        if not path.exists():
            errors.append(f"{name} is missing; run `python scripts/validate_repo.py --write`")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected_content:
            errors.append(f"{name} is stale; run `python scripts/validate_repo.py --write`")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skills repo invariants.")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--write", action="store_true", help="refresh llms.txt and llms-full.txt before validating")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    if not (root / ".git").exists():
        errors.append(f"{root}: not a git repository root")

    skills, skill_errors = find_skills(root)
    errors.extend(skill_errors)
    if skills:
        errors.extend(validate_llms(root, skills, args.write))
    errors.extend(validate_markdown_links(root))

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    suffix = " (manifests refreshed)" if args.write else ""
    print(f"Repository validation passed{suffix}: {len(skills)} skills, markdown links resolved, llms manifests synced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
