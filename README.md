# Atheer Workspace

**A generic, file-first edition of the AtheerOS architecture for developers
who want to bring their own context and working preferences to AI-assisted
work.**

Status: v0.1, early foundation.

Atheer Workspace includes generic equivalents of AtheerOS's soul, brain, body,
hands, database, and profile areas. It organizes readable Markdown files so a
file-capable AI agent in an IDE can consult relevant project, learning,
knowledge, and preference notes when you ask. Its architecture is complete as
a reusable file-based blueprint; it does not include the runtime services that
would make an AI operating system execute automatically. See the
[architecture map](docs/architecture.md).

```text
atheer-workspace/
├── System/       Soul, brain, body, and host integration boundaries
├── Knowledge/    Database equivalent: active vault and archive
├── Profile/      Optional work, study, identity, goals, life, finance context
├── examples/     Fictional data for retrieval exercises
├── docs/         Conventions, privacy, retrieval, and roadmap
├── evals/        Manual retrieval scenarios
└── tests/        Standard-library checker tests
```

**Illustrative example only; these are not measured results.**

Fictional `Profile/developer-profile.md`:

```text
Role: junior Python developer
Goal: build reliable APIs
Current: comfortable with Python basics
Next project: small Flask service
Learning time: 4 hours each week
```

**Question:** “Help me plan what to study next”

| Generic answer | Grounded in the profile |
|---|---|
| Study a programming topic that interests you. | Study HTTP and REST basics, then build a small Flask API. Set aside one hour each week for focused practice. |

## What Atheer is—and is not

Atheer is a customizable folder-and-file workspace for developers and
engineers using AI agents for work and study. It is not an AI model, RAG
service, agent runtime, IDE plugin, or security product. It does not implement
semantic search or automatically make an agent read or obey these files.

Atheer is designed to be adaptable to file-capable agents and IDEs. Instruction
discovery, file access, edits, scripts, and integrations vary by host; verify
the behavior of your specific tool. Reading requires file-read access, and
creating or editing files requires corresponding permissions.

## Privacy first

**An AI agent that can read workspace files may send relevant content to its
provider.** Whether content leaves the device, how it is retained, and whether
it is used for training depend on the specific agent, provider, account,
settings, and tools. A local folder does not imply local-only AI processing.

Do not put credentials, tokens, confidential employer/client material,
identity or financial records, or other sensitive information in an
AI-accessible workspace unless you have verified that use is allowed and
appropriate. Share the minimum needed, prefer redacted or summarized examples,
check provider and organizational policies, and limit agent permissions.
`.gitignore` helps avoid accidental Git tracking; it cannot stop an agent from
reading files. See [the privacy guide](docs/privacy-and-safe-use.md).

## The three pillars and System layers

- **System** contains four layers: `soul/` (role and boundaries), `brain/`
  (instructions, external profile exports, and optional memory tiers),
  `body/` (workflows, scripts, templates, and tool registry), and `hands/`
  (host integration boundary).
- **Knowledge** is the Database equivalent, divided into an on-demand vault
  and a deliberate archive. It is not a database engine or automatic search
  index.
- **Profile** offers optional work, study, identity, goals, life, and finance
  areas. Add only context you choose to expose to your AI tool; sensitive
  information should usually stay out.

Start at [AGENTS.md](AGENTS.md), then follow the relevant
[_index.md](./_index.md) navigation. See the
[System guide](System/README.md) for how its files fit together.

## Quick start

1. Copy or fork this starter into a workspace you control.
2. Read [AGENTS.md](AGENTS.md) and the [privacy guide](docs/privacy-and-safe-use.md).
3. For local personalization, copy only the templates you need into the
   appropriate area of your own workspace.
   `.gitignore` excludes common personal profile, memory, and override files
   from Git by default, but does not prevent agent access or guarantee privacy.
4. Open the folder in an agent/IDE that can access workspace files. If it does
   not load instructions automatically, ask it to read `AGENTS.md` and follow
   relevant indexes before acting.
5. Try a scenario in [evals/retrieval-scenarios.md](evals/retrieval-scenarios.md).
6. Run the local structure, metadata, and link check:

   ```bash
   python3 System/body/scripts/check-workspace.py
   ```

7. Run the checker tests:

   ```bash
   python3 tests/check-workspace-tests.py
   ```

## Retrieval, metadata, and personalization

Atheer uses human-readable indexes and source notes to guide deliberate
retrieval: start from the task, follow the relevant index, read only needed
files, and identify evidence or uncertainty. This borrows ideas from RAG and
personal wikis, but it does not implement a search or indexing service. See
[retrieval and evidence](docs/retrieval-and-evidence.md) and
[file conventions](docs/file-conventions.md).

Use templates under `Profile/templates/` only for context you choose to share.
Each template explains its own privacy limits; finance and life context can be
sensitive even when summarized. Use `System/body/design.local.md` for
engineering and design preferences. The tracked
[design.md](System/body/design.md) is a generic template; copy it to
`design.local.md` before customizing. These are editable user guidance, not
permanent facts or instructions every agent will automatically obey.

An automated first-run interview, automatic profile writing, adaptive memory,
executable agent integrations, and automatic script generation are **not
implemented**. Session workflows are written procedures that must be invoked;
memory tiers are storage conventions, not an automatic memory service. See
[the roadmap](docs/roadmap.md).

## Scripts and release readiness

The included standard-library Python checker reads relevant non-ignored
Markdown files and reports missing essentials, invalid supported metadata,
stale notes, tracked local override files, and broken supported local links.
It does not scan secrets or prove that the workspace is safe.

Before a public release, review the complete staged file list, run the checks,
and inspect all content yourself. Use
[the release checklist](docs/release-checklist.md).

This starter is distributed under the MIT license (see [LICENSE](LICENSE)).
