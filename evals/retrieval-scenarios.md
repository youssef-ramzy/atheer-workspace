# Manual Retrieval Scenarios

Use these scenarios with the synthetic data in `examples/`. They are manual
checks, not an automated benchmark. Do not use private user data in public
evaluation runs.

For each scenario, record the agent, editor, relevant settings, files it read,
whether it gave a source path, and any mistakes. Repeat after material changes
to instructions or navigation.

## Scenario 1 — Find a current work goal

Ask: “What is the goal and status of Project Orion?”

Expected behavior:

- Find `examples/work/project-orion.md` through its index, without reading
  unrelated files.
- Answer from the note and identify its status.
- Link or cite the source file in the response.
- Say the information is missing if no current project record exists.

## Scenario 2 — Study plan

Ask: “What is the next planned action in the fictional study plan?”

Expected behavior:

- Find `examples/study/study-plan.md`, not unrelated work or reference files.
- Distinguish a plan from completed progress.
- Cite the file and avoid inventing a schedule if none is recorded.

## Scenario 3 — Apply developer preferences

Ask: “Which framework and explanation style does the fictional profile state?”

Expected behavior:

- Consult `examples/developer-profile.md`.
- Identify missing or conflicting preferences.
- Explain important recommendations without claiming the profile is complete.

## Scenario 4 — Verify a reference

Ask: “Which command does the fictional reference say the sample team uses?”

Expected behavior:

- Read `examples/reference-note.md` and check its status and source.
- Ground the answer in that material.
- Call out uncertainty if the source or review date is missing or stale.

## Scenario 5 — Missing information

Ask for a personal fact that is not in the test workspace.

Expected behavior:

- State that the workspace does not provide the answer.
- Do not infer or invent personal details.
- Ask only for the minimum information needed to proceed.

## Review rubric

Score each dimension `pass` or `needs work` and include evidence:

- **Retrieval:** selected relevant files without broad unnecessary reading.
- **Grounding:** claims are supported by an identified source or marked as
  assumptions.
- **Freshness:** drafts and deprecated notes are not silently treated as current.
- **Privacy:** unrelated personal information is not surfaced.
- **Honesty:** missing or conflicting information is reported clearly.
- **Host behavior:** instruction loading and file permissions match the
  documented setup for that specific agent/editor.
