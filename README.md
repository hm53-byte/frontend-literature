# frontend-literature

A machine-readable catalogue of frontend literature. 1,659 entries, 1,541
verified, with a schema, closed value sets, and tests that keep it usable.

```bash
python alat/query.py --category webgl-threejs-shaders --level expert --access free
python alat/query.py --search "view transitions" --gold
python alat/query.py --list-categories
```

---

## Dataset summary

Not a link list. Every entry carries type, category, level, access, tags and
one sentence on why it is worth reading, so it can be filtered by machine
instead of read top to bottom.

- **Size:** 1,659 entries; 1,541 in the verified subset
- **Format:** JSONL, one object per line, UTF-8
- **Schema:** [`katalog/schema.json`](katalog/schema.json), JSON Schema draft-07
- **Unique URLs:** 1,659, no duplicates
- **With DOI:** 161
- **Categories:** 55; the largest holds 2.7% of entries

## Composition

**By type**

| docs | article | paper | book | repo | tutorial | course | spec | interactive | video | newsletter |
|---|---|---|---|---|---|---|---|---|---|---|
| 418 | 311 | 195 | 179 | 140 | 114 | 93 | 87 | 57 | 44 | 21 |

**By level.** advanced 577, intermediate 576, expert 294, beginner 212.

**By access.** free 1,318, paid 283, freemium 58.

The range runs from living specifications to foundational papers in perception
and decision-making: Hick 1952, Fitts 1954, Miller 1956, Stevens 1957 sit next
to WHATWG and current tooling, because modern interface design leans on them
directly.

## Fields

Required: `id`, `title`, `type`, `category`, `level`, `access`, `url`.

Three fields have closed value sets, because they are what you filter on:

```json
"type":   ["book","docs","paper","course","tutorial","article",
           "video","spec","repo","newsletter","interactive"],
"level":  ["beginner","intermediate","advanced","expert"],
"access": ["free","paid","freemium"]
```

A value outside the set is not merely untidy: the filter would silently stop
returning that entry instead of raising. A test holds this, not a convention.

Two fields exist to keep two different things apart. `source` records **how the
entry was found** (`scholar`, `web`, `known`); `verified` records whether its
existence was checked. "I know of this" is not "I checked this".

## The verified subset

`frontend_literature_gold.jsonl` holds the verified entries. The relationship
between the two files is a test, not a promise: the gold file must be
**exactly** the entries carrying `verified: true`. If those diverge, one of two
statements about the catalogue is false and you cannot tell which.

## What the tests protect

16 tests. A catalogue without them rots quietly.

| Test | Why it exists |
|---|---|
| unique `id` | the same entry under two keys is worse than a missing entry |
| unique `url` | same source listed twice under different names |
| closed sets on 3 fields | filters must fail loudly, not silently |
| description not empty | the point is not having to open every link |
| papers carry DOI or venue | otherwise unverifiable |
| no category above 10% | keeps it a catalogue, not one topic under a broad name |

Two findings from writing those tests, both kept:

**Twelve duplicate identifiers.** URLs were unique, but twelve pairs shared a
key, so lookup by key depended on read order. Resolved by suffix, not deletion:
both entries are real and distinct sources.

**The first year bound was wrong, not the data.** I set the lower bound at 1960
and the test rejected four entries. All four are foundational papers the field
still cites. The bound moved to 1950, with the reason recorded in the test.

## Collection method

Entries were gathered from academic search, general web search, and prior
knowledge, then normalised into the schema. `verified` means the URL and the
existence of the work were checked. It does **not** mean the content was read
end to end, nor that the link is guaranteed live today.

## Limitations

- **Descriptions are in Croatian.** All other fields, including every closed
  set, are in English, so filtering and machine use are unaffected. Full
  international use would need the descriptions translated.
- **Link rot is not monitored.** There is no scheduled re-check.
- **Selection is one person's judgement.** The balance test only guarantees no
  single category dominates; it says nothing about what is missing.

## Reproduce the numbers

```bash
git clone https://github.com/hm53-byte/frontend-literature && cd frontend-literature
pip install pytest && python -m pytest testovi -q
python alat/query.py --list-categories
```

## Licensing

Apache-2.0 for the schema, tooling and tests. See [LICENSE](LICENSE).

The catalogue contains **metadata about other people's work**: title, author,
year, link and an original description. It contains no part of the works
themselves. Rights in the works belong to their holders, and a link is not a
licence to use them.
