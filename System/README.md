# System — Guidance and Workflows

`System/` mirrors AtheerOS's four conceptual layers. It describes how an AI
agent should work in this workspace. It is human-readable configuration, not
an AI model or runtime.

- `soul/` defines a generic assistant role, voice, values, and baseline
  boundaries. User overrides belong in ignored local files.
- `brain/` contains the master prompt and documented RAM, episodic, semantic,
  and procedural memory organization. It is not an automatic memory service.
- `body/` contains workflows, design preferences, scripts, a tools registry,
  and templates. Workflows are not automatically executable plugins.
- `hands/` documents the host integration boundary. It contains no active
  hooks or integrations by itself.

The host agent decides whether these files load automatically and what it can
read or edit. Start from the root [AGENTS.md](../AGENTS.md).
