# Release Strategy (MANDATORY)

Strict release management. Every release must be well-documented, consistently formatted, and traceable to file-level changes.

## Versioning: Semantic Versioning (SemVer)

Format: `vMAJOR.MINOR.PATCH`

| Bump | When | Example |
|------|------|---------|
| MAJOR | Breaking changes, removed skills, renamed files that consumers depend on | v1.0.0 → v2.0.0 |
| MINOR | New skill, new reference file, new feature added to existing skill | v1.0.0 → v1.1.0 |
| PATCH | Fix typo, expand existing docs, fix YAML frontmatter, small content updates | v1.1.0 → v1.1.1 |

Rules:
- Tag format: `vX.Y.Z` (always prefixed with `v`)
- Create git tag BEFORE creating GitHub release
- Use `--verify-tag` on every `gh release create`
- Never skip versions

## Release Title Prerequisites (ENFORCED)

Before writing a release title, confirm all of these:

- **Stable scope**: the merged diff is settled; do not title from an outdated PR description
- **Dominant change identified**: pick the main user-facing change, not the most recent internal task
- **Audience identified**: know whether the release is mainly for users, contributors, or operators
- **Title/body alignment**: the first lines of the release notes reinforce the same story as the title
- **Truthfulness**: the title is strong but not inflated beyond what the release actually changed
- **Social-card awareness**: assume the title and opening lines may appear alone on GitHub release cards or preview images

## Release Title Format (ENFORCED)

```
vX.Y.Z — {Short Description}
```

Examples:
- `v1.0.0 — Analyze skill`
- `v1.13.1 — Code review, supercharged`
- `v1.14.0 — Portable review specs`

Weak examples:
- `v1.3.1 — GitHub PR Workflow Improvements`
- `v1.3.1 — Updates`
- `v1.3.1 — Misc fixes`

Rules:
- Use em dash `—` (not `-` or `–`)
- Title ≤ 70 characters
- Lead with the dominant outcome, not the implementation detail
- Be specific enough that the reader can infer what changed in one glance
- Prefer user-facing capability over internal process wording
- Avoid filler like `updates`, `improvements`, `misc`, `cleanup`, `refactors`
- If two candidates exist, choose the one that better survives being seen without context on a release card

Practical title heuristic:

```text
vX.Y.Z — {specific outcome}
```

Good:
- `v1.13.1 — Code review, supercharged`
- `v0.8.0 — Faster local inference`
- `v2.4.0 — Rules discovery everywhere`

Bad:
- `v1.13.1 — Workflow changes`
- `v0.8.0 — Performance updates`
- `v2.4.0 — Internal improvements`

## Release Description Format (ENFORCED)

Every release description MUST follow this exact structure:

```markdown
{1-3 sentence summary of what changed and why}

### New Files

| File | Description |
|------|-------------|
| `{path}` | {What this file is — purpose, key content} |

### Changed Files

| File | Change |
|------|--------|
| `{path}` | {What specifically changed — bold key changes, use → for before/after} |

### Summary

- {Bullet point per notable change — active voice, past tense, no period at end}
```

### Section Rules

| Section | When to Include | When to Omit |
|---------|-----------------|--------------|
| Summary paragraph | Always | Never |
| New Files | Release adds files | No new files (omit entire section) |
| Changed Files | Release modifies files | No changed files (omit entire section) |
| Summary bullets | MAJOR or MINOR releases | PATCH releases (summary paragraph + tables are enough) |

### Writing Style

- **Active voice, past tense**: "Added rate limiting" not "Rate limiting was added"
- **No periods** at end of bullet points or table cells
- **Bold key changes** in Changed Files: `**Action count**: 7 → 8`
- **Use `→`** for before/after: `old format → new format`
- **File paths in backticks**: always wrap paths in `` ` ``
- **No filler**: no "various improvements", "minor updates", "miscellaneous changes"
- Every file listed must have a specific, meaningful description
- Group related changes when describing (e.g., "Updated routing table, references section, and output template links")

### Opening Lines / Preview Rules

Assume the release title plus the opening summary / first bullets may be the only text visible in:

- GitHub release cards
- Open Graph preview images
- link unfurls in chat tools
- social post screenshots

Therefore:

- The opening summary must reinforce the title immediately
- The first bullet should restate the dominant change in concrete terms
- Do not lead with internal maintenance work if the release is mainly about a user-facing capability
- Do not bury the dominant change below less important items

### Changed Files Detail Level by Bump

| Bump | Detail Level |
|------|-------------|
| PATCH | One-line description per file |
| MINOR | 1-2 sentences per file, bold key changes |
| MAJOR | Full paragraph per file, before/after comparisons, migration notes |

## Release Description Generation Protocol

When creating or updating a release description, follow this exact process:

### Step 1: Identify Changes

```bash
# For first release
git ls-tree -r --name-only vX.Y.Z

# For subsequent releases
git diff --stat vPREVIOUS..vX.Y.Z
git log --oneline vPREVIOUS..vX.Y.Z
```

### Step 2: Analyze Each File

For every file in the diff:

1. Read the actual diff: `git diff vPREVIOUS..vX.Y.Z -- path/to/file`
2. Summarize what changed specifically (not "updated file")
3. For new files: describe purpose and key content
4. For changed files: describe what was added/removed/modified

### Step 3: Write Description

Follow the enforced format above. No shortcuts.

### Step 4: Verify

Before publishing, check:

- [ ] Title follows `vX.Y.Z — {Description}` format
- [ ] Title is specific, outcome-first, and brief
- [ ] Title matches the dominant user-facing change in the merged diff
- [ ] Summary paragraph is present and specific
- [ ] Opening lines reinforce the same story as the title
- [ ] Every new file is listed with description
- [ ] Every changed file is listed with specific change details
- [ ] No vague descriptions ("minor updates", "various fixes")
- [ ] File paths are in backticks
- [ ] Active voice, past tense throughout
- [ ] Key changes are bolded in Changed Files table

## Batch Update Protocol

When updating descriptions for multiple releases at once:

1. Process releases in chronological order (oldest first)
2. Use `git diff vPREVIOUS..vCURRENT` for each pair
3. Read actual diffs — never guess what changed
4. Apply the same format to every release
5. Verify each before publishing

```bash
# Update a release
gh release edit vX.Y.Z --title "vX.Y.Z — {Title}" --notes "$(cat <<'EOF'
{description}
EOF
)"
```

## Anti-Patterns (NEVER)

- NEVER use auto-generated notes without manual review and reformatting
- NEVER write "updated X" without saying WHAT changed in X
- NEVER skip files in the diff — every file gets documented
- NEVER use `--generate-notes` as the final description (use as starting point only)
- NEVER publish a release without the New Files / Changed Files tables
- NEVER mix description styles across releases — consistency is mandatory
- NEVER use passive voice ("was added", "has been updated")
- NEVER leave the description empty or use placeholder text

## Sources

Format based on:
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Auto-Generated Release Notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
- [GitHub Release Note Content Type](https://docs.github.com/en/contributing/style-guide-and-content-model/release-note-content-type)
