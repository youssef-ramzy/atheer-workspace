# Brain — Instructions and Memory

The brain layer describes how an agent should reason with workspace context.
It includes the master prompt and an optional memory organization inspired by
AtheerOS.

- `master-prompt.md` is task and navigation guidance.
- `memory/episodic/` is for dated events, `semantic/` for durable concepts,
  and `procedural/` for reusable methods.
- `profiles/` is a reserved location for user-controlled exports from external
  AI profiles; review them before use and do not import them automatically.
- `templates/` contains blank starting points for user-controlled notes.

These are file conventions. They do not implement automatic memory, guarantee
that a host reads every file, or authorize saving personal information.
