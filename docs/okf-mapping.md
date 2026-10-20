# Atheer Metadata and OKF v0.2

This note compares Atheer's lightweight frontmatter conventions with the
official [Open Knowledge Format v0.2 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/04624f4fb69caadd7bead187ec467f111f80ad8b/okf/SPEC.md).
It describes partial overlap only. **Atheer does not claim OKF conformance or
compatibility.**

## OKF v0.2 fields relevant to this comparison

The spec requires only top-level `type`. It recommends optional `title`,
`description`, `resource`, and `tags`. Additional producer-defined fields are
allowed. The v0.2 spec also defines these optional field families:

- **Provenance — `sources`:** a list of source records from which the concept
  derives. Each source record requires `resource`; optional fields include
  `id`, `title`, `author`, `usage_count`, and `last_modified`. Optional
  top-level `usage_window` gives the `{from, to}` datetime range for usage
  counts.
- **Trust — `generated` and `verified`:** `generated` records who produced
  content and when (`by` required within the mapping; `at` is an ISO 8601
  datetime). `verified` records one or more `{by, at}` verification events.
  Consumers derive `unverified`, `machine-confirmed`, or `human-reviewed`
  tiers from verification actors; these tiers are advisory, not access control.
- **Lifecycle — `status`:** values are `draft`, `stable`, or `deprecated`;
  omitted status means `stable`.
- **Lifecycle — `stale_after`:** optional absolute ISO 8601 instant. The
  concept is stale when `now >= stale_after`.
- **Computation:** the spec also defines fields for attested computation
  concepts. Atheer does not currently define or implement that family.

See the specification's §§4–5 and §§10–11 for its field definitions and
conformance rules.

## Field-by-field comparison

| Atheer convention | Relationship to OKF v0.2 | Difference |
|---|---|---|
| `type` | Same field name; OKF also makes it the only always-required field. | Atheer does not claim to implement all OKF consumer/producer requirements. |
| `status` | Same field name. | Atheer currently allows `draft`, `current`, `review`, `archived`; OKF defines `draft`, `stable`, `deprecated`, with omitted meaning `stable`. Values and lifecycle semantics differ. |
| `updated` | Both convey freshness-related information. | Atheer uses a date-only `YYYY-MM-DD` for last meaningful review. OKF v0.2 uses `generated.at` for when the concept content was last meaningfully changed, as an ISO 8601 datetime with producer identity in `generated.by`. They are not interchangeable. |
| `stale_after` | Same field name and absolute-instant stale-on-or-after meaning as OKF. | Atheer documents and validates an ISO 8601 datetime with timezone offset, but its other metadata rules remain Atheer-specific. |
| `sources` | Same top-level field name and broad provenance purpose. | Atheer's simple list of links/paths is not the OKF structured list of source records. It does not require each source entry's `resource` or model OKF source fields and credibility signals. |
| `confidence` | No equivalent OKF field. | Atheer uses `verified`, `inferred`, `unknown`, or `synthetic`. OKF does not define this scalar; it derives trust tiers from `generated` and `verified`. `synthetic` labels fictional fixtures in Atheer. |
| `title` | OKF-recommended field. | Not currently part of Atheer's defined metadata convention. |
| `description` | OKF-recommended field. | Not currently part of Atheer's defined metadata convention. |
| `resource` | OKF-recommended canonical URI for an underlying asset. | Not currently part of Atheer's defined metadata convention; Atheer's `sources` should not be substituted for it. |
| `tags` | OKF-recommended cross-cutting labels. | Not currently part of Atheer's defined metadata convention. |
| `generated`, `verified`, `usage_window` | Optional OKF provenance/trust fields. | Not currently part of Atheer's defined metadata convention. |

Atheer's fields are optional except where its checker validates a field that is
present. Its metadata guidance is a small local convention, not an OKF schema.
The shared Markdown/YAML representation and a few field names do not establish
format compatibility.
