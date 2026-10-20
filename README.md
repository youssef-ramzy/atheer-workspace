# Atheer Workspace

Atheer is a customizable work-and-study workspace for developers and engineers
who use AI agents in their work and learning. It organizes human-readable
context, instructions, and reusable procedures so a file-capable AI agent can
help in a way that better fits the person's goals and workflow.

Atheer is a folder-and-file system, not an AI model, RAG service, agent
runtime, IDE plugin, or security product. It is designed to be usable from
different agents and IDEs that can read and, with permission, edit workspace
files. Instruction loading, file access, scripts, and integrations vary by
host and must be checked rather than assumed.

## Privacy first

**An AI agent that can read workspace files may send relevant content to its
provider.** Whether content leaves the device, how it is retained, and whether
it is used for training depend on the specific agent, provider, account,
settings, and tools. A local folder does not imply local-only AI processing.

Never place credentials, tokens, confidential employer/client material,
identity or financial records, or other sensitive information in an
AI-accessible workspace unless you have verified that use is allowed and
appropriate. Share the minimum needed, prefer redacted or summarized examples,
check provider and organizational policies, and limit agent permissions.
`.gitignore` can help prevent accidental Git tracking; it cannot stop an agent
from reading files. See [the privacy guide](docs/privacy-and-safe-use.md).

## The three areas

```text
System/    How the AI should navigate and work; preferences and workflows
Database/  Reference knowledge and archives, loaded when relevant
Profile/   The person's work, study, tools, skills, and goals
```

- **System** is the guidance layer: concise entry instructions, optional
  identity and design preferences, workflows, and scripts.
- **Database** keeps source-aware reference material. It is not a database
  engine or automatic search index.
- **Profile** describes the person's work and study context. Keep personal
  copies private and expose only appropriate details to the chosen agent.

Start at [AGENTS.md](AGENTS.md), then follow the relevant
[_index.md](./_index.md) navigation. Read the [System guide](System/README.md)
to understand the instruction and workflow layers.

## Quick start

1. Copy or fork this starter to a workspace you control.
2. Read [AGENTS.md](AGENTS.md) and the [privacy guide](docs/privacy-and-safe-use.md).
3. For local personalization, copy the generic templates to
   `System/soul/identity.local.md`, `System/body/design.local.md`, and
   `Profile/developer-profile.md`, then customize those local copies. The
   included `.gitignore` excludes these files and new work/study notes from Git
   by default; it does not prevent agent access or guarantee privacy.
4. Open the folder in an agent/IDE that can access workspace files. If it does
   not load instructions automatically, ask it to read `AGENTS.md` and follow
   the relevant index before acting.
5. Try a retrieval scenario in [evals/retrieval-scenarios.md](evals/retrieval-scenarios.md).
6. Run the local structure and link check:

   ```bash
   python3 System/body/scripts/check-workspace.py
   ```
7. Run the checker tests:

   ```bash
   python3 tests/check-workspace-tests.py
   ```

The included scenarios show intended behavior; they do not prove compatibility
with every agent. Check how your particular host handles instructions, file
permissions, and tool access. Reading context requires file-read access;
creating, editing, or deleting files requires corresponding host permissions.
Use version control or another backup/review process for changes.

## How the workspace helps an agent

Atheer uses deliberate, lightweight retrieval rather than requiring a vector
database:

1. Start from concise workspace instructions.
2. Follow indexes to the area relevant to the task.
3. Open only the needed work, study, or reference files.
4. Use source and status metadata to distinguish current material from drafts,
   assumptions, and archived notes.
5. Ground important answers in the files read, and state when evidence is
   missing or stale.

This is inspired by useful RAG and wiki principles—retrieval, links, sources,
and freshness—without claiming automated semantic search. See
[retrieval and evidence](docs/retrieval-and-evidence.md) and
[file conventions](docs/file-conventions.md).

## Personalization and customization

Use the templates under `Profile/templates/` to record only useful,
non-sensitive context such as role, learning goals, technologies, skill areas,
and preferred collaboration style. Keep personal copies at the local paths
above; keep the generic templates unchanged in a public repo. Use
`System/body/design.local.md` for coding, architecture, and visual-design
preferences. These are editable guidance, not permanent facts or instructions
an agent will automatically obey.

This foundation does **not** yet include an automated first-run interview,
personal `start` / `go-offline` commands, adaptive memory, agent-specific
integrations, or automatic script generation. Those are future possibilities
with explicit consent and safety criteria in [the roadmap](docs/roadmap.md).

## Scripts and safety

The foundation includes one standard-library Python checker. It only reads
workspace paths and reports missing essentials or broken local Markdown
links; it does not modify files or contact a network. It is not a secret
scanner or a security guarantee.

Every future automation should have a narrow scope, clear inputs and outputs,
and safe defaults. Preview changes before applying them; do not silently delete,
publish, upload, or commit user data.

## Before publishing a public copy

- Inspect every file and the staged Git file list; do not rely on ignore rules.
- Run the included check, an appropriate secret scan, and a human review.
- Keep examples fictional or clearly redacted.
- Choose and add a license intentionally.
- Do not claim universal compatibility, guaranteed privacy, or automatic
  execution of workflows.
- Use [the Claude review plan](claude-review-plan.md) for a read-only review
  restricted to this starter folder.
