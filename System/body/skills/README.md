# Skills and Workflows

A workflow is a concise Markdown procedure for a repeated work or study task.
It does not run by itself and is not automatically a slash command. The host
agent must be able to discover or be directed to the file.

## Adding one

1. Put the workflow in a clearly named Markdown file.
2. State when it applies and which context to load.
3. Give ordered steps, permission boundaries, and expected output.
4. Avoid duplicating rules already in `AGENTS.md`.
5. Test it with the agent/editor you intend to use and record host-specific
   requirements.

## Core workflows

| Workflow | Use it when |
|---|---|
| [Start a work session](start-session.md) | Beginning a task and loading its relevant context |
| [Prepare a context handoff](context-handoff.md) | Pausing, switching tools, or continuing elsewhere |
| [Wrap up a session](wrap-up-session.md) | Summarizing completed work and next steps |
| [Work on a development project](work-on-project.md) | Planning or progressing a project task |
| [Plan a study session](plan-study-session.md) | Choosing a focused learning session |

Keep procedures small and revise them when real use reveals ambiguity. Use
fictional examples; never include credentials, private notes, or
client/employer material in reusable procedures.
