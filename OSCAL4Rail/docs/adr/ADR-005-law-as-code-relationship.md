# ADR-005: Relationship to Law-as-Code Initiatives

**Status:** Accepted

**Date:** 2026-06-25

**Context:**

The German Federal Agency for Disruptive Innovation (SPRIND) has launched a strategic initiative "Law as Code" with the goal of making all German legislation machine-readable and executable by 2028. The initiative defines five foundational elements: (1) definition of a legal code format, (2) open-source editing tools, (3) AI-powered translation processes, (4) a central repository of official legal code, and (5) training and capacity building.

Separately, the Rulemapping Group provides a methodology for translating legal text into visual decision trees (Rulemaps) that capture the decision logic of regulations — validated by SPRIND as "weltweit einzigartig".

Railway operations are governed by a deep regulatory cascade:
- EU level: TSIs, ERA regulations, Railway Safety Directive
- National level: AEG, ERegG, EBO, BSKG
- Industry level: BS-KI, national implementation standards
- Company level: Ril-Werke (DB), internal guidelines

OSCAL4Rail addresses the same fundamental problem as Law-as-Code — making regulations machine-readable — but does so bottom-up and domain-specific rather than top-down and generic.

**Decision:**

OSCAL4Rail positions itself as a **sectoral Law-as-Code implementation for the railway domain**. It does not compete with SPRIND/Rulemapping but complements them:

1. **OSCAL4Rail models requirements** (what must be fulfilled, by whom, how binding)
2. **Rulemapping models decision logic** (under which conditions does a requirement apply)
3. **Law-as-Code provides the political/institutional framework** for official publication

The relationship is layered:

```
Law-as-Code (SPRIND)          = political initiative, format definition
  └── Rulemapping             = methodology for decision logic
        └── OSCAL4Rail        = domain-specific catalog format for railways
              └── AI Agents   = consume catalogs for compliance checking
```

**Alignment with SPRIND's 5 Foundational Elements:**

| SPRIND Element | OSCAL4Rail Coverage |
|----------------|---------------------|
| 1. Definition of a legal code | ✅ NIST OSCAL Catalog (JSON Schema validated) |
| 2. Open-source editing tools | ✅ extract.py, validate.py, diff.py (Apache 2.0) |
| 3. AI-powered translation | ⚡ Planned: Agents query catalogs; extraction remains deterministic |
| 4. Central repository | ✅ Git-based catalog repository with CI validation |
| 5. Training & capacity building | 🔜 Tutorials and how-tos exist; formal training not yet |

**Interfaces to clarify (future work):**

- Format compatibility: Can SPRIND's legal code format produce/consume OSCAL Catalogs?
- Regulatory hierarchy: How does Law-as-Code map the cascade (Gesetz → Verordnung → Branchenstandard → Unternehmensweisung)? OSCAL's Profile model (Catalog → Profile → Component) already supports this.
- Identifier scheme: OSCAL4Rail uses chapter-based IDs. Law-as-Code may define a national identifier scheme (URN:LEX or similar).
- Applicability vs. decision logic: OSCAL4Rail's `props` model captures obligation level; Rulemapping's decision trees capture the conditions. These are complementary, not redundant.

**Consequences:**

- (+) OSCAL4Rail gains political legitimacy and institutional backing
- (+) Future catalogs may be derived from official Legal Code instead of parsing PDFs
- (+) Rulemapping can enrich the applicability model with decision logic
- (+) OSCAL4Rail serves as a concrete reference implementation for SPRIND
- (-) Dependency on external initiative timelines (mitigated: OSCAL4Rail works independently)
- (-) Potential format divergence if SPRIND defines an incompatible legal code format (mitigated: monitor and participate in standardization)

**Actions:**

1. Extend Incubation Proposal with Law-as-Code references (Phase 0)
2. Contact SPRIND initiative (Phase 2, Aug–Sep 2026)
3. Pilot Rulemapping methodology on one BS-KI control (Phase 3, Q4 2026)
4. Engage EBA/ERA through OpenRail channels (Phase 3)
