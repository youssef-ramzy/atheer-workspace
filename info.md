# Atheer Workspace — Agent Overview

Atheer Workspace is the generic, portable blueprint for the AtheerOS
architecture. It provides Markdown instructions, navigation, workflows,
templates, and a checker for developers using file-capable AI agents.

## Architecture

- `System/soul/` — generic identity, persona, values, and boundaries.
- `System/brain/` — operating instructions, optional memory tiers, a RAM
  template, and guidance for external AI profile exports.
- `System/body/` — written workflows, scripts, tools registry, preferences,
  and reusable project templates.
- `System/hands/` — host integration and execution boundary.
- `Knowledge/` — active reference vault and deliberate archive; the portable
  equivalent of AtheerOS `Database/`.
- `Profile/` — optional work, study, identity, goals, life, and finance areas.

The [architecture map](docs/architecture.md) explains this correspondence.
Tracked starter material is generic; personal files are optional and excluded
from Git where configured.

## Usage model

An agent reads the root `AGENTS.md`, follows relevant indexes, loads only
task-relevant context, then uses an applicable written workflow. The user
controls whether personal information is added or memory is saved. Workflows
and memory folders are conventions; they do not run automatically.

## Limits and privacy

The workspace does not include an AI model, runtime, automatic retrieval,
persistent memory service, permissions engine, or active integrations. Host
behavior must be verified. `.gitignore` controls Git tracking, not whether an
AI host can read or transmit accessible files. Review provider settings and
organizational requirements before sharing sensitive context.

## Validation

Run `python3 System/body/scripts/check-workspace.py` from the workspace root to
check required starter paths, supported metadata, selected Git ignore rules,
and supported local Markdown links. The checker does not scan for secrets,
prove privacy, verify factual accuracy, or establish host compatibility. The
standard-library tests are in `tests/check-workspace-tests.py` and can be run
separately.
