# Retrieval and Evidence

Atheer borrows practical ideas from RAG and personal wikis: retrieve relevant
material, follow links, preserve sources, and notice freshness. The foundation
does this through Markdown navigation and instructions; it does not implement
embeddings, semantic search, a vector store, or automated retrieval.

## Retrieval procedure for an agent

1. Read the root `AGENTS.md` and task-specific project instructions.
2. Identify the task domain: work, study, System guidance, or reference.
3. Follow that area's `_index.md` and open only likely relevant files.
4. Check `status`, `updated`, and source notes when present. Do not rely on
   archived, draft, or stale content as current without verification.
5. For significant factual claims, point to the file or source that supports
   the answer. Separate source-backed facts from assumptions.
6. If context conflicts or evidence is missing, say so and ask for clarification
   instead of filling gaps with invented personal facts.
7. Only broaden the search if the relevant files do not answer the request.

## Human curation

Indexes are a lightweight map, not a complete search engine. Keep them short,
update links when files move, and use meaningful headings and names. Add
automated indexing only if real retrieval tasks show navigation is not enough.

## Evaluation

Use [the retrieval scenarios](../evals/retrieval-scenarios.md) to check whether
an agent finds the right material, avoids unrelated/private files, grounds its
answer, and handles missing information honestly. Results apply only to the
agent and configuration tested.
