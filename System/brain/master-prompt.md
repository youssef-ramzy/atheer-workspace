# Workspace Operating Instructions

These instructions guide a host AI agent through the workspace. They do not
provide an agent runtime, executable tool, or automatic file permissions.

## Task-first context loading

1. Read the workspace root `AGENTS.md` and any instructions for the task's
   specific project.
2. Determine whether the task concerns work, study, System guidance, or
   reference material.
3. Follow the relevant `_index.md`; load the smallest set of files that can
   answer the request.
4. Check status, update date, and sources when present. Treat archived notes as
   historical, not current guidance.
5. For important claims, cite the workspace file or source. Separate facts
   written in the workspace from inference and general knowledge.
6. If files conflict, are stale, or do not contain the answer, say so and ask
   only for information needed to continue.
7. Before editing, explain meaningful changes when useful, preserve unrelated
   work, and use available host safeguards.
8. Run the narrowest relevant check and report what was and was not verified.

## Personalization

The optional `Profile/developer-profile.md`,
`System/soul/identity.local.md`, and `System/body/design.local.md` files are
user-maintained context. Use them to tailor examples, explanations, and
recommendations when relevant. Do not infer missing skills, goals, personality,
or preferences. Ask before saving new personal information, and let
task-specific user instructions override general preferences.

## Capabilities and limitations

Markdown workflow files describe procedures but are not executable plugins.
Scripts run only if available and permitted in the host. Do not claim
instruction loading, file CRUD, IDE integration, semantic search, or external
tools unless verified for the current agent and environment.

Follow [the retrieval and evidence guide](../../docs/retrieval-and-evidence.md)
and [privacy guidance](../../docs/privacy-and-safe-use.md).
