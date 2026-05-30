# Code Style

Generic defaults — replace with the repo's real conventions.

- Match surrounding code: naming, structure, comment density, idioms.
- Follow an established pattern when 3+ files already do (don't introduce a 4th variant).
- Prefer the smallest change that works; delete dead code you create.
- Run `{LINT_COMMAND}` and `{FORMAT_COMMAND}` before opening a PR; fix issues, don't suppress them.
- Public APIs: explicit types/signatures and a short doc comment.
- No secrets, tokens, or environment-specific values in source.
