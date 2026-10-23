# Knowledge — References and Archive

`Knowledge/` is the portable equivalent of the AtheerOS `Database/` layer. It
separates active references in [`vault/`](vault/_index.md) from retained
historical material in [`archive/`](archive/_index.md). It is not an automatic
search index or database service.

- Add source-aware reference notes to the vault when a durable fact will be useful again.
- Keep the source, review date, and status visible when freshness matters.
- Load references on demand; do not assume the agent reads every file here.
- Move material to the archive deliberately and mark obsolete knowledge as
  deprecated so it is not confused with current guidance.
- When archiving a note, leave a brief historical pointer at its former active
  location. Do not revise archived material in place; restore it deliberately
  before changing it.
- Do not store material that should not be exposed to the selected AI agent.

See [file conventions](../docs/file-conventions.md) and
[retrieval guidance](../docs/retrieval-and-evidence.md).
