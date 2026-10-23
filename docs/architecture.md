# Atheer Workspace Architecture

Atheer Workspace is the generic, portable blueprint for the AtheerOS
architecture. It preserves the same responsibilities while replacing
Youssef-specific identity, values, profile data, and memory with neutral
guidance and optional blank templates.

| AtheerOS | Workspace equivalent | Responsibility |
|---|---|---|
| `System/soul/` | `System/soul/` | Generic assistant identity, persona, values, and boundaries |
| `System/brain/` | `System/brain/` | Operating instructions, RAM template, external profile-export boundary, and optional episodic, semantic, and procedural memory conventions |
| `System/body/` | `System/body/` | Session and task workflows, scripts, verified-tools registry, preferences, and reusable project templates |
| `System/hands/` | `System/hands/` | Host integration and execution boundary; no integration is activated by files alone |
| `Database/` | `Knowledge/` | On-demand reference vault and deliberate archive |
| `Profile/` | `Profile/` | Optional user-maintained work, study, identity, goals, life, and finance context |

The folder names differ for the knowledge pillar to keep the starter's
human-readable naming, but its responsibilities map to AtheerOS `Database/`.
The profile areas are blank and optional; the structure does not imply that
users should fill every category.

## Runtime boundary

This is architectural parity at the file-and-guidance level, not a running AI
operating system. Workspace files do not provide a model, agent runtime,
automatic retrieval, persistent memory service, permissions engine, or active
integrations. Workflows are written procedures, not commands or hooks. Those
capabilities depend on the host and must be verified separately.

## Personalization boundary

The tracked files describe generic defaults and fictional examples. Users may
copy only the templates they need into their own workspace. Personal files are
excluded from Git by default where patterns apply, but `.gitignore` does not
prevent an AI host from reading or transmitting accessible files. Do not add
real user data to examples or tracked starter files.

## Using OKF

OKF can inform metadata on durable knowledge concepts, especially source,
verification, lifecycle, and freshness fields. It does not replace the Atheer
architecture, profile, workflows, or host integration layer. See the
[OKF mapping](okf-mapping.md) for compatibility limits.
