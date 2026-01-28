# Commit Workflow

Goal: one intent per commit, no secrets, staged diff reviewed.

Requires confirmation before any `git add`/`git commit`.

## Flow

1. Inspect

```bash
git status
git diff
```

2. Stage intentionally (preferred: path-based)

```bash
git add <paths...>
```

3. Review staged

```bash
git diff --cached
```

4. Write message

Format: `<type>(<scope>): <why>`

Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `ci`

5. Commit

```bash
git commit -m "<type>(<scope>): <why>"
```

6. Verify

```bash
git status
```

## Notes

- Avoid `git add .` unless user explicitly asks.
- If hooks modify files after commit, stage the changes and create a follow-up commit (no amend unless requested).

## Commit Best Practices

- Atomic: one intent per commit; avoid mixing refactors + features.
- Explain why: the title states reason/impact, not a file list.
- Review what you ship: always read `git diff --cached` before committing.
- Prefer small commits: easier review and safer rollback.
- No WIP on shared branches: avoid `wip:` unless explicitly requested.
- Tests: if behavior changes, add/update tests in the same PR (ideally same commit or adjacent).
- Sensitive files: do not commit `.env*`, keys, credentials, or generated secrets.

### Message Examples

```text
feat(auth): add password reset flow
fix(api): handle nil token on refresh
refactor(db): extract query builder for reuse
docs(readme): clarify install instructions
```
