# Product Roadmap

Atheer Workspace's goal is to give developers and engineers a generic,
understandable architecture for AI-assisted work and study. Personalization is
optional and user-controlled. This roadmap
separates the foundation that exists from future ideas. An item here is not an
implemented feature or delivery promise.

## Foundation in this starter

- AtheerOS-mapped structure: `System/` with soul, brain, body, and hands;
  `Knowledge/` as the Database equivalent; and optional `Profile/` areas.
- Cross-agent entry guidance for file-capable agents and IDEs, with host
  limitations stated explicitly.
- Lightweight indexes, optional metadata, source/freshness guidance, and a
  deliberate retrieval procedure.
- Generic profile and design-preference templates; no real personal data.
- Short example workflows, evaluation scenarios, and a read-only structural
  checker for supported links and metadata, ignored files, tracked local
  overrides, and stale notes.
- Generic start-session, context-handoff, wrap-up, work, and study workflows;
  blank RAM and memory templates; and separate episodic, semantic, and
  procedural memory guidance.
- Privacy and provider-boundary guidance.

## Later, only after the foundation is tested

1. **First-use setup:** an opt-in interview asking a few useful questions about
   role, goals, stack, current skill areas, and collaboration preferences.
   Preview the proposed profile, allow edits or skips, and write nothing until
   the person confirms. Do not ask for secrets or sensitive details by default.
2. **Host-specific workflow adapters:** document how verified hosts discover
   and invoke the existing start, handoff, and wrap-up procedures. Make
   continuity and storage behavior clear; never write session history without
   consent.
3. **Personal working profile:** editable tech stack, tools, skill levels,
   learning goals, and preferred explanation/collaboration style. Treat entries
   as user-maintained context, not inferred truth.
4. **Design and engineering preferences:** copy the generic `design.md`
   template to `design.local.md` for code,
   architecture, UI, and communication preferences. Explain how it applies and
   how to override it for an individual task.
5. **Careful adaptation:** suggest changes based on explicit corrections or
   repeated user-approved feedback. Show diffs, request approval, and keep a
   change history. Never silently rewrite identity, preferences, or plans.
6. **Repeated-task helpers:** add scripts only for demonstrated repetitive
   tasks. Keep them local and narrow, document inputs/outputs, preview
   destructive changes, avoid network access by default, and test edge cases.
7. **Workspace maintenance:** extend checks for stale indexes and other
   metadata issues. Report findings; do not auto-delete, auto-archive, or claim
   that a clean scan proves safety.
8. **Host guidance:** document verified setup for specific agents/editors as
   separate adapters. Keep a portable Markdown baseline and do not claim
   universal compatibility.
9. **RAG/search:** consider local or provider-backed semantic indexing only if
   retrieval scenarios demonstrate a need. Evaluate privacy, source tracing,
   freshness, rebuild behavior, and maintenance cost first.

## Readiness gates

Before adding personalization or automation, test the foundation with
fictional data and more than one host where available. For each host, document
what loads automatically, what requires a prompt, what file operations are
available, and which permissions can be restricted. A future feature should
have an owner-controlled opt-in, clear failure behavior, and tests.
