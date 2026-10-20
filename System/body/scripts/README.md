# Scripts — Local Helpers

Scripts are code and may read or modify files. Inspect source, scope, and
permissions before running. Do not assume an AI agent can execute scripts just
because they are present in this folder.

## Included

- `check-workspace.py` checks required starter files, supported frontmatter,
  stale dates, tracked `*.local.md` files, Git-ignored content, and supported
  relative Markdown links. It is read-only, uses Python's standard library,
  and makes no network calls. Run it inside a Git working tree.

Run from the workspace root:

```bash
python3 System/body/scripts/check-workspace.py
```

The checker skips `*.local.md` and Git-ignored paths while scanning, but fails
if a `*.local.md` file is tracked. It does not validate general YAML syntax,
privacy, secret absence, content accuracy, or agent compatibility. A clean
result is not a security guarantee. Stale findings are warnings and do not
fail the check.

## Adding automation later

Add scripts for demonstrated repeated tasks only. Document what they read,
write, and require. Prefer dry-run or preview behavior, require explicit
confirmation for destructive changes, and avoid network access by default.
Test failure cases and never silently delete, publish, upload, or commit data.
