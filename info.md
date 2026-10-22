## 1. ONE-PARAGRAPH SUMMARY

Atheer is a folder of notes and instructions that helps developers give an AI agent useful context about their work and study goals. Instead of repeating preferences or project details in every conversation, a person can keep them in readable files and ask an agent to consult the relevant ones. Atheer provides a structure and guidance for doing that; the AI tool must still follow those instructions for the approach to work.

## 2. WHAT IS NOT INCLUDED

Atheer does not include an AI model, an agent runtime, a search engine, or automatic retrieval. “RAG” means retrieval-augmented generation: a system that searches for relevant information and provides it to a model. Atheer borrows the idea of using relevant sources, but does not implement that kind of search.

Atheer also does not include an automatic first-use interview, automatic profile writing, adaptive memory, or guaranteed support for particular AI tools. Its checker does not scan for secrets or prove that the workspace is safe. These limits are stated in `README.md`, `docs/retrieval-and-evidence.md`, and `docs/roadmap.md`.

## 3. FOLDER-BY-FOLDER TOUR

- `System/` contains agent instructions and reusable procedures. Important files include `System/README.md`, `System/brain/master-prompt.md`, `System/soul/identity.md`, and `System/body/design.md`. The “soul” and “design” files are templates; personal copies should use ignored `.local.md` names.
  - `System/body/skills/` contains written workflows, including `plan-study-session.md` and `work-on-project.md`. They are not automatically executable commands.
  - `System/body/scripts/` contains the checker, `check-workspace.py`, and its usage notes in `README.md`.
- `Knowledge/` is for reference notes and archived material. Its `README.md` and `_index.md` explain how to organize and find them.
- `Profile/` is for user-maintained work and study context. Its `README.md` explains privacy boundaries; `Profile/templates/` contains the developer profile, project, reference, and study-plan templates.
- `docs/` explains conventions and limits. Key files are `file-conventions.md`, `okf-mapping.md`, `privacy-and-safe-use.md`, and `release-checklist.md`.
- `evals/` contains manual scenarios for checking whether an agent finds and uses relevant notes. See `retrieval-scenarios.md`.
- `examples/` contains fictional retrieval examples, such as `developer-profile.md`, `project-orion.md`, and `study-plan.md`.
- `tests/` contains `check-workspace-tests.py`, the standard-library tests for the checker.
- Root files: `.gitignore` excludes selected local and sensitive file patterns from Git; `AGENTS.md` gives the agent entry rules; `README.md` introduces Atheer and explains setup; `_index.md` is the navigation page; `LICENSE` contains the MIT license.

## 4. HOW IT WORKS, STEP BY STEP

1. A person opens the folder in an AI tool that can read local files. Whether the tool loads instructions automatically depends on that tool.
2. The person asks, “Help me plan what to study next.” The agent is instructed to start with `AGENTS.md`, which points it to relevant indexes and tells it to load only needed context.
3. The agent follows the root `_index.md` to `Profile/`, then follows its study navigation and `Profile/study/README.md`. It should read only relevant study notes.
4. If a user has made one, the agent can consult `Profile/developer-profile.md` or a study plan to tailor the answer. These local files are ignored by Git by default. If no personal note exists, the agent can use a template as a format guide, but the blank placeholders are not user facts.
5. The agent may follow `plan-study-session.md` for a study-planning request. It should distinguish planned work from completed work and avoid saving a study log unless asked.
6. The agent answers using relevant notes and explains missing information. These steps are written instructions; Atheer cannot force an AI tool to load or obey them. Code enforcement is limited to checks performed when the person runs the checker.

## 5. THE CHECKER, EXPLAINED SIMPLY

The checker scans Markdown files it considers relevant. Inside Git, it skips ignored paths and `.local.md` files and checks that local overrides are not tracked. Outside Git, it prints a notice, skips Git checks, and still checks structure, metadata, and links.

It can report these errors and warnings:

- `could not inspect directory {filename}: {error}` — the folder scan failed.
- `could not inspect tracked files: {error}` — Git could not list tracked files.
- `tracked local override file: {path}` — a `.local.md` file is tracked.
- `missing directory: {name}` / `missing file: {name}` — a required starter path is absent.
- `could not check Git ignore status for {path}: {error}` — Git could not check whether a path is ignored.
- `non-portable absolute link at {file}:{line}: {target}` — a Markdown link uses an absolute local path.
- `link escapes workspace at {file}:{line}: {target}` — a link points outside the workspace.
- `broken local link at {file}:{line}: {target}` — the linked local path does not exist.
- `unclosed YAML frontmatter: {file}:1` — a metadata block starting with `---` has no closing marker.
- `unsupported frontmatter syntax at {file}:{line}` — a line is outside the checker’s supported YAML subset.
- `invalid sources at ...`, `invalid sources record at ...`, `invalid sources field at ...`, or `invalid sources indentation at ...` — a source list is not in the supported form.
- `missing type in frontmatter: {file} ...` / `empty type at ...` — a metadata block lacks a non-empty `type`.
- `status 'current' is no longer valid; use 'stable'` (and corresponding messages for `archived` or `review`) — an old status value needs migration.
- `invalid status {value} ...` — status is not `draft`, `stable`, or `deprecated`.
- `invalid confidence {value} ...` — confidence is not `verified`, `inferred`, `unknown`, or `synthetic`.
- `invalid updated date at ...` — the value is not a valid date in `YYYY-MM-DD` form.
- `invalid stale_after at ...` — the value is not a date-time with a timezone offset.
- `stale: {file} (stale_after reached)` — the stale deadline has arrived.
- `stale: {file} (updated is at least 180 days ago)` — the review date is at least 180 days old and no `stale_after` overrides it.

The program also prints a failure heading if errors exist, a no-Git notice when relevant, and a pass message when checks succeed.

The 20 tests prove that the checker:

1. Reports missing required paths.
2. Accepts an existing relative Markdown link.
3. Requires `type` only when frontmatter exists.
4. Reports broken links but ignores code examples.
5. Rejects links that escape the workspace.
6. Fails when a local Markdown file is tracked.
7. Skips local and Git-ignored Markdown.
8. Continues in a non-Git directory and skips `.local.md` files there.
9. Rejects an unknown status.
10. Accepts the three supported statuses.
11. Gives migration advice for each legacy status.
12. Accepts structured source records.
13. Accepts `sources: []`.
14. Rejects three invalid source shapes.
15. Rejects an impossible update date.
16. Accepts `synthetic` confidence.
17. Warns about an old review date.
18. Lets `stale_after` override the old-date warning.
19. Warns after a stale deadline.
20. Rejects a stale deadline with no timezone offset.

## 6. THE METADATA RULES

Frontmatter is a small metadata block at the top of a Markdown note, between `---` lines. When it is present, `type` must be non-empty. `status` may be `draft`, `stable`, or `deprecated`; if omitted, it means `stable`. `updated` is an Atheer-only review date in `YYYY-MM-DD` format. `stale_after` is a date and time with an explicit timezone offset. `sources` is a list of records with required `resource` and optional `id` and `title`. `confidence` may be `verified`, `inferred`, `unknown`, or `synthetic`; it is also an Atheer-only field.

Valid example:

```yaml
---
type: reference
status: stable
updated: "2026-10-01"
stale_after: "2026-12-31T00:00:00Z"
sources:
  - resource: docs/file-conventions.md
    title: Metadata guidance
confidence: verified
---
```

Invalid example:

```yaml
---
type: reference
status: current
---
```

The checker reports: `status 'current' is no longer valid; use 'stable'`.

The repository compares some field meanings with Google’s OKF v0.2, the Open Knowledge Format. It says `status`, `sources`, and `stale_after` use the same field semantics, while the checker accepts only a restricted subset of `sources` records. `updated` and `confidence` are Atheer extensions, not OKF fields. The repository does not claim OKF conformance or compatibility: OKF v0.2 requires frontmatter with non-empty `type` on every non-reserved Markdown file, while Atheer makes frontmatter optional and uses `_index.md` and `README.md` for navigation. It also does not implement all OKF fields or requirements. The comparison is pinned to v0.2; newer upstream versions have not been checked.

## 7. PRIVACY AND SAFETY DESIGN

The repository gives users practical privacy guidance, recommends sharing only necessary and redacted information, and warns that an AI provider may process files the agent can read. `.gitignore` excludes selected credentials, private folders, work/study notes, and local personalization files from Git by default. The checker also reports tracked `.local.md` files.

These controls do not stop an AI tool from reading ignored files, prevent a person from force-adding ignored files to Git, remove data already committed, or determine how a provider handles data. The checker does not scan for secrets. Users must keep sensitive information out of agent-accessible files unless they have checked their provider and organizational rules, and review files and history before publishing.

The prompt-injection rule says to treat reference notes, copied web pages, and tool output as data, and not follow instructions inside them unless the person confirms. This is guidance for an AI agent; the checker does not enforce it.

## 8. HOW A NEW USER CUSTOMIZES IT

1. Copy `System/soul/identity.md` to `System/soul/identity.local.md`. Add only role guidance or preferences you want the agent and its provider to see.
2. Copy `System/body/design.md` to `System/body/design.local.md`. Add useful technical, visual, and collaboration preferences.
3. Copy `Profile/templates/developer-profile.md` to `Profile/developer-profile.md`. Add relevant goals, tools, self-described skills, and collaboration preferences.
4. If useful, copy `Profile/templates/study-plan.md` or `Profile/templates/project.md` into the appropriate study or work area and fill in only relevant information. For references, use `Profile/templates/reference-note.md` and record source records in the documented format.
5. Do not add credentials, tokens, confidential employer/client details, financial or identity records, or other sensitive information by default. These files are ignored by Git where the patterns apply, but they remain readable by the AI tool.
6. Open the folder in a file-capable agent. If it does not load instructions automatically, ask it to read `AGENTS.md`. Run `python3 System/body/scripts/check-workspace.py` and `python3 tests/check-workspace-tests.py`.

## 9. PROBLEMS AND RISKS I FOUND

| Severity | File and line                                | What is wrong                                                                                                                        | Suggested fix                                                                  |
| -------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Medium   | `docs/retrieval-and-evidence.md:14`          | It uses “archived” as a note status, while the current status value is `deprecated`.                                                 | Replace that status reference with `deprecated`.                               |
| Low      | `System/body/scripts/check-workspace.py:275` | Repeated top-level metadata keys silently overwrite earlier values, which can hide conflicting metadata.                             | Detect duplicate keys and report an error.                                     |
| Low      | `docs/release-checklist.md:30`               | It says to add a chosen license, though the repository already includes an MIT license and describes itself as distributed under it. | Tell reviewers to verify that the included license matches the owner’s intent. |
| Low      | `LICENSE:3`                                  | Personal data present; value withheld.                                                                                               | Confirm the copyright attribution is intentional.                              |

No machine paths or personal email matches were found in the tracked-file search. No secrets were identified during this read-through.

## 10. TEN HARD QUESTIONS AND HONEST ANSWERS

1. **How is this different from writing a README?** It provides a folder structure, templates, navigation, reusable instructions, and a checker alongside its introductory README.
2. **How do you know agents follow it?** You do not know from the repository alone. The evaluation scenarios are manual and results depend on the agent and its settings.
3. **Does it search my files automatically?** No. It provides navigation and tells an agent to open relevant files.
4. **Does it include an AI model?** No. It is a set of files for use with a separate file-capable AI tool.
5. **Will ignored profile files stay private?** No such guarantee. `.gitignore` affects Git tracking, not what an agent or other software can read.
6. **Does a passing checker prove the repository is safe?** No. It checks selected structure, metadata, and links. It does not scan for secrets or verify factual accuracy.
7. **Does it follow OKF?** The repository makes no conformance or compatibility claim. It shares some field semantics but differs in frontmatter requirements and navigation.
8. **Are the retrieval examples real results?** No. They are explicitly fictional and the README calls its comparison illustrative, not measured.
9. **Can the workflows run as slash commands?** Not by themselves. They are Markdown procedures; host support varies.
10. **How should someone use it without exposing sensitive work?** Add only relevant, approved context, redact when possible, check provider and workplace rules, and limit the AI tool’s access.

## 11. WHAT I DID NOT CHECK

I did not inspect untracked files or any `.local.md` files. I did not verify behavior in specific AI tools, provider data handling, the live GitHub page, or the truth of any external source. I did not use the network.

Checker output:

```text
Atheer Workspace check passed: structure, metadata, Git ignores, and links.
```

Test output:

```text
....................
----------------------------------------------------------------------
Ran 20 tests in 0.028s

OK
```

Tracked files: **45**.

No files were modified.
