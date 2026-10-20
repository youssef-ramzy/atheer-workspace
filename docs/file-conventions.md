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
status: current
updated: "YYYY-MM-DD"
stale_after: "YYYY-MM-DDTHH:MM:SSZ"
sources: []
confidence: unknown
---
```

Recommended fields:

- `type`: broad kind of file, such as `project`, `study-plan`, `reference`, or
  `decision`.
- `status`: `draft`, `current`, `review`, or `archived`. The checker validates
  these Atheer values; they are not the OKF lifecycle values.
- `updated`: date of the latest meaningful content review, not an automatic
  modification timestamp. Use a valid `YYYY-MM-DD` date. In profile templates,
  the literal placeholder `YYYY-MM-DD` is allowed.
- `stale_after`: optional absolute ISO 8601 datetime with a timezone offset.
  The checker warns when the current time is at or after this instant. If
  omitted, it warns when `updated` is at least 180 days old.
- `sources`: optional list of links or paths that support the content. This
  simple Atheer convention is not the structured OKF v0.2 `sources` schema.
- `confidence`: `verified`, `inferred`, `unknown`, or `synthetic`. Use
  `synthetic` for intentionally fictional examples; it is an Atheer extension,
  not an OKF trust field. Explain important uncertainty in the body.

Do not add frontmatter to every file just to satisfy a schema. If a field is
unknown, say so; never fabricate sources, dates, or confidence.

Atheer's fields are not claimed to conform to OKF. See
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
