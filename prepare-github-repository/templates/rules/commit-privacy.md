# Commit Privacy

Never leak a personal email through commit metadata. Every commit's author **and** committer email
must be the GitHub no-reply address — never a personal/work email.

- Allowed identity: `<id>+<login>@users.noreply.github.com`
  (resolve once: `gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'`).
- This repo is configured with `user.email` set to the no-reply. Do not override it with a personal
  email — not via `git commit --author`, not via `-c user.email=...`, not in CI.
- Before committing, confirm `git config user.email` resolves to the no-reply.
- Keep account protection on: "Keep my email addresses private" + "Block command line pushes that
  expose my email" at `https://github.com/settings/emails`.
- A pushed commit's email is **public and permanent**. If a personal email is exposed, treat it as
  already leaked and report it — do not silently rewrite pushed history.
- Never write a personal email into source, docs, examples, logs, or PR text. Use the no-reply or a
  placeholder.
