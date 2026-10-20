# System — Guidance and Workflows

`System/` describes how an AI agent should work in this workspace. It is
human-readable configuration, not an AI model or runtime.

- `brain/master-prompt.md` defines task-oriented navigation and evidence rules.
- `soul/identity.md` and `body/design.md` are generic templates. Keep personal
  copies in the ignored `identity.local.md` and `design.local.md` files.
- `body/skills/` contains short written workflows, not automatically executable
  plugins.
- `body/scripts/` contains optional local helpers that must be inspected before
  use.

The host agent decides whether these files load automatically and what it can
read or edit. Start from the root [AGENTS.md](../AGENTS.md).
