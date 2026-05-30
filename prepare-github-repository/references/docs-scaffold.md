# Docs Scaffold

Covers desired-state items #10–#13. Operates on the repo's local working copy (clone first if
needed). Create-if-missing only — existing files are diffed and confirmed, never clobbered.

```text
CLAUDE.md            <- canonical agent instructions (you edit this)
AGENTS.md            <- byte-identical mirror of CLAUDE.md (generated)
.claude/rules/*.md   <- modular rules, referenced by CLAUDE.md
README.md            <- human entry point
```

## 1. README.md (#10)

Ensure present with the basics. If missing, scaffold:

```markdown
# {REPO_NAME}

> {DESCRIPTION}

## Install
{INSTALL_COMMAND}

## Usage
{USAGE_EXAMPLE}

## License
{LICENSE_TYPE}
```

If README.md exists, leave it — only flag missing required sections (H1, description, install,
usage, license) as a WARN. Do not rewrite a maintained README.

## 2. .claude/rules/*.md (#13)

Scaffold a starter rule set if `.claude/rules/` has no `*.md`. Copy the generic templates:

```bash
mkdir -p .claude/rules
cp <skill>/templates/rules/git-workflow.md   .claude/rules/git-workflow.md
cp <skill>/templates/rules/code-style.md     .claude/rules/code-style.md
cp <skill>/templates/rules/security.md       .claude/rules/security.md
cp <skill>/templates/rules/commit-privacy.md .claude/rules/commit-privacy.md
```

These are generic and placeholder-driven — adapt to the repo. The `git-workflow` rule intentionally
mirrors the repo settings this skill enforces (squash-only, PR-required, delete-on-merge); the
`commit-privacy` rule pairs with the email-privacy enforcement (#14/#15, see
[email-privacy.md](email-privacy.md)).

## 3. CLAUDE.md (#11)

Scaffold from `templates/CLAUDE.md`. It must reference every file under `.claude/rules/` so the
rules actually load. After copying rules, regenerate the reference list:

```bash
# List rule references for CLAUDE.md (one @-include per rule)
for f in .claude/rules/*.md; do echo "- @$f"; done
```

Fill placeholders ({REPO_NAME}, {DESCRIPTION}, {PRIMARY_BRANCH}, command placeholders) from the
actual repo. Do not assume a language/framework.

## 4. AGENTS.md — full content mirror (#12)

AGENTS.md must be **iso to CLAUDE.md** (byte-identical). It is generated, never hand-edited:

```bash
cp CLAUDE.md AGENTS.md
diff -q CLAUDE.md AGENTS.md && echo "mirror OK" || echo "MIRROR DRIFT"
```

CLAUDE.md is canonical (the maintainer edits it); AGENTS.md is the portable alias other agent tools
read. Re-run the `cp` whenever CLAUDE.md changes.

### Keep the mirror from drifting (recommended)

Offer to add a CI guard so a PR fails if the two diverge:

```yaml
# .github/workflows/agents-mirror.yml
name: agents-mirror
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: diff -q CLAUDE.md AGENTS.md
```

A local pre-commit hook (`diff -q CLAUDE.md AGENTS.md || cp CLAUDE.md AGENTS.md`) is an alternative.
Propose, don't auto-install hooks.

## Confirmation

- Show a diff for any file that already exists; write only on explicit confirmation.
- Never copy this skill repo's own description/topics/rules content as defaults — use placeholders.

## Verify

```bash
test -f README.md && test -f CLAUDE.md && test -f AGENTS.md && echo "docs present"
diff -q CLAUDE.md AGENTS.md && echo "mirror OK"
ls .claude/rules/*.md >/dev/null 2>&1 && echo "rules present"
```
