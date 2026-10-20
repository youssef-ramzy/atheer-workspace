# Atheer Metadata and OKF v0.2

This note compares Atheer's lightweight frontmatter conventions with the
official [Open Knowledge Format v0.2 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/04624f4fb69caadd7bead187ec467f111f80ad8b/okf/SPEC.md).
The spec pinned here is v0.2; newer upstream versions have not been checked.
It describes field semantics only. **Atheer does not claim OKF conformance or
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
| `status` | Same field name and semantics. | Allowed values are `draft`, `stable`, `deprecated`; absent means `stable`. |
| `sources` | Same field name and source record semantics. | Atheer's checker accepts a restricted subset: required `resource`, optional `id` and `title`; other OKF source fields are not implemented. |
| `stale_after` | Same field name and stale-on-or-after absolute instant semantics. | Requires an ISO 8601 datetime with explicit UTC offset, as required for timestamp-valued OKF keys. |
| `updated` | Atheer extension; not an OKF field. | Date-only `YYYY-MM-DD` review date. OKF uses `generated.at` for content generation time; they are not interchangeable. |
| `confidence` | Atheer extension; not an OKF field. | Values are `verified`, `inferred`, `unknown`, or `synthetic`; OKF derives trust tiers from `generated` and `verified`. |
| `title`, `description`, `resource`, `tags`, `generated`, `verified` | Not defined by Atheer. | OKF recommends the first four and defines the latter two. |

Atheer validates its restricted subset when supported metadata is present. Its
frontmatter remains optional, unlike OKF v0.2 §11, which requires every
non-reserved `.md` concept to have frontmatter with non-empty `type`. OKF
reserves `index.md` and `log.md` (allowing `okf_version` only on bundle-root
`index.md`); Atheer instead uses `_index.md` and `README.md` for navigation and
allows optional frontmatter. This is another reason Atheer makes no conformance
claim. The checker parses only the documented restricted YAML subset, not
general YAML.
The shared Markdown/YAML representation and a few field names do not establish
format compatibility.
