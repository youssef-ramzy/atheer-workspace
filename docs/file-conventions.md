# File and Metadata Conventions

Atheer uses ordinary Markdown so people can edit files in a text editor or IDE
and file-capable agents can read them. Keep prose concise, use descriptive
lowercase kebab-case names, and link related material. Metadata is optional
unless a local workflow says otherwise.

## Optional YAML frontmatter

For notes where source, freshness, or lifecycle matters, use a small header:

```yaml
---
type: reference
status: current
updated: "YYYY-MM-DD"
sources: []
confidence: unknown
---
```

Recommended fields:

- `type`: broad kind of file, such as `project`, `study-plan`, `reference`, or
  `decision`.
- `status`: `draft`, `current`, `review`, or `archived`. Define local values
  consistently if you extend this set.
- `updated`: date of the latest meaningful content review, not an automatic
  modification timestamp.
- `sources`: links or paths that support the content. Use an empty list when
  no external source is relevant.
- `confidence`: evidence quality such as `verified`, `inferred`, or `unknown`.
  Explain uncertainty in the body when it matters.

Do not add frontmatter to every file just to satisfy a schema. If a field is
unknown, say so; never fabricate sources, dates, or confidence.

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
