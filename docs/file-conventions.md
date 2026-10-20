# File and Metadata Conventions

Atheer uses ordinary Markdown so people can edit files in a text editor or IDE
and file-capable agents can read them. Keep prose concise, use descriptive
lowercase kebab-case names for files and subfolders inside the three top-level
pillars. The pillar names `System/`, `Knowledge/`, and `Profile/` are
intentional capitalized exceptions. Link related material. Metadata is optional
unless a local workflow says otherwise.

## Optional YAML frontmatter

For notes where source, freshness, or lifecycle matters, use a small header:

```yaml
---
type: reference
status: stable
updated: "YYYY-MM-DD"
stale_after: "YYYY-MM-DDTHH:MM:SSZ"
sources: []
confidence: unknown
---
```

Recommended fields:

- `type`: broad kind of file, such as `project`, `study-plan`, `reference`, or
  `decision`.
- `status`: `draft`, `stable`, or `deprecated`; absent means `stable`, matching
  OKF v0.2 semantics. Existing values migrated as `current` → `stable`,
  `archived` → `deprecated`, and `review` → `draft`.
- `updated`: date of the latest meaningful content review, not an automatic
  modification timestamp. Use a valid `YYYY-MM-DD` date. In profile templates,
  the literal placeholder `YYYY-MM-DD` is allowed.
- `stale_after`: optional absolute ISO 8601 datetime with an explicit UTC
  offset, matching OKF v0.2. A date or datetime without an offset is invalid.
  The checker warns when the current time is at or after this instant. If
  omitted, it warns when `updated` is at least 180 days old.
- `sources`: optional list of records, each with required `resource` and
  optional `id` and `title`, matching the restricted OKF v0.2 field shape.
  `resource` may be a URL, bundle-relative path, or scope descriptor.
- `confidence`: `verified`, `inferred`, `unknown`, or `synthetic`. Use
  `synthetic` for intentionally fictional examples; it is an Atheer extension,
  not an OKF field. `updated` is also an Atheer extension: a date-only review
  date and not an OKF field. Explain important uncertainty in the body.

The checker parses only this documented restricted YAML subset: simple scalar
fields, `sources: []`, or `sources` records containing `resource` and optional
`id` and `title`. It is not a general YAML parser.

Do not add frontmatter to every file just to satisfy a schema. If a field is
unknown, say so; never fabricate sources, dates, or confidence.

**Conformance:** OKF v0.2 §11 requires every non-reserved `.md` file to have
frontmatter with a non-empty `type`; it reserves `index.md` and `log.md` for
navigation and history (with optional `okf_version` on the bundle-root
`index.md`). Atheer makes frontmatter optional and uses `_index.md` and
`README.md` for navigation. This is another reason Atheer makes no OKF
conformance claim. See
[the OKF v0.2 mapping](okf-mapping.md) for exact overlap and differences.

## Durable knowledge and activity

- **Reference/knowledge**: durable facts or guidance with sources and review
  status.
- **Plans**: intended future actions, with a timeframe or state if useful.
- **Activity/logs**: dated events or progress; do not treat these as current
  facts without checking.
- **Archive**: retained historical material that should not guide current work
  unless explicitly requested.

Use clear filenames and headings to make the purpose visible. Move outdated
material to an archive only deliberately; mark it so an agent can recognize it
as historical.

## Source notes

For important claims, add a source path or URL and enough context to identify
what it supports. Distinguish owner-provided information from independently
verified reference material. A model's confidence is not evidence. If
verification has not happened, mark the claim as unverified or unknown.
