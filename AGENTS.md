# Atheer Workspace — Agent Entry Instructions

Atheer is a work-and-study workspace for developers and engineers. It provides
organized files and human-readable guidance; it is not an AI model, agent
runtime, or security boundary.

## Working in this workspace

1. Read this entry file, then use `_index.md` files to locate relevant context.
2. Load only files relevant to the request. Do not scan all of `Profile/` or
   `Database/` by default.
3. Treat `System/body/skills/` as written procedures. Follow one only when
   relevant; do not assume it is a plugin, slash command, or executable tool.
4. When present, use `Profile/developer-profile.md`,
   `System/soul/identity.local.md`, and `System/body/design.local.md` as the
   person's current profile and preferences—not as unchangeable truth. If
   information is missing, ask or state the assumption.
5. Ground important claims in the files read. Distinguish stated facts from
   inference, and identify stale or conflicting information.
6. Before changing files, use the host's available permissions and safeguards.
   Explain meaningful edits and run the narrowest relevant check.
7. Ask before external actions, publishing, installing tools, deleting data,
   or saving new personal preferences.

## Privacy and provider boundary

A file accessible to an AI agent may be included in prompts, tool calls,
provider processing, or logs. Data handling depends on the agent, provider,
account, settings, and enabled tools. Local files are not necessarily
processed locally.

- Do not expose credentials, tokens, confidential employer/client information,
  identity or financial records, or sensitive personal details without checking
  applicable provider and organizational policies.
- Share only the minimum context necessary. Redact or summarize where possible.
- Limit file, terminal, network, and integration permissions when the host
  allows it.
- `.gitignore` affects Git tracking, not what an AI agent can read.
- Never copy private profile information into a public example or repository.

## Host compatibility

Atheer is intended for file-capable AI agents and IDEs, but instruction
discovery, editing, terminal access, integrations, and permission controls are
host-specific. If instructions are not loaded automatically, explicitly direct
the agent to this file. Verify the host's behavior; do not promise that every
agent or IDE will work identically. Reading requires file-read access; creating,
editing, or deleting files requires the corresponding write permissions.
