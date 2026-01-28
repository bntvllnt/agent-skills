# File Storage

Docs:

- File storage overview: https://docs.convex.dev/file-storage

## Core ideas

- Store files in Convex file storage via `ctx.storage`.
- Store references/metadata (e.g. `storageId`, content type, owner) in tables.
- Restrict access: validate the current user and ensure they own the file or have permission.

## Common patterns

- Upload flow:
  - client requests an upload URL (or upload token)
  - client uploads the file
  - backend stores `storageId` + metadata

- Download/serve flow:
  - backend checks permissions
  - backend returns a signed URL or serves via an HTTP action

## Safety

- Never log file contents.
- Treat file metadata as user-controlled unless validated.
- When deleting a record, decide whether to also delete the stored file.
