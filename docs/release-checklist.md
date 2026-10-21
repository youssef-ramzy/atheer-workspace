# Public Release Checklist

Use this checklist before sharing an Atheer workspace publicly. It is a
human-review aid, not a security certification.

## Review content

- Inspect every file that will be published, including hidden files and the
  staged Git file list.
- Confirm examples are synthetic or explicitly approved for publication.
- Check for credentials, personal data, confidential employer/client material,
  and machine-specific paths. A scanner can help but can miss secrets.
- Review ignore rules; they do not remove files already tracked or prevent an
  AI agent from reading them.
- Review repository history if sensitive material may have been committed.

## Verify behavior and documentation

- Run `python3 System/body/scripts/check-workspace.py`.
- Run `python3 tests/check-workspace-tests.py`.
- Check links, setup commands, metadata conventions, and claims about supported
  agents/editors against actual evidence.
- State clearly that Atheer is a workspace of files and guidance, not an AI
  model, agent runtime, search service, or security boundary.
- Do not claim universal compatibility or guaranteed privacy.
- Identify planned features as plans, not current capabilities.

## Prepare repository metadata

- Verify that the included LICENSE file matches the owner's intent.
- Set a concise repository description and relevant topics in the hosting UI.
- Create a release only after the owner confirms the contents, version, and
  release notes.

## Optional independent review

For a read-only review, share only the intended public repository/files and ask
the reviewer to stay within that scope. Do not upload private workspace data
unless you have checked the receiving service's data-handling terms and have
permission to share it.
