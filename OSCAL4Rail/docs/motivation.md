# Motivation – Why OSCAL4Rail?

## The Problem

### Regulations are stuck in PDFs

European railway operations are governed by hundreds of regulations: EU Technical Specifications for Interoperability (TSIs), national standards (BS-KI, Ril 420), company guidelines, and local agreements. Almost all of them live as PDF or Word documents.

This creates a fundamental problem: **regulations are human-readable but not machine-readable.**

### Rules are interpreted, not enforced

When a regulation says "the line number must be displayed at the station", every organisation interprets this individually:
- What exactly is a "line number"?
- Which stations? All of them? Only those with more than X passengers?
- What if the station has no display?

Because rules are free text, they are filtered through the **personal context** of the reader. Two engineers at different companies reading the same paragraph will implement different things. The result is inconsistent passenger information across borders and operators — despite theoretically following the same standard.

### Change is invisible

When a new version of a regulation is published, nobody knows exactly what changed. The only option is to read the entire document again, or rely on a change log (if one exists). There is no way to automatically detect: "Rule 2.1 now says X instead of Y."

At the rule level, version management does not exist.

### The scale of the problem

- SBB alone manages 10,000+ infrastructure contracts spanning 150 years
- The Swiss BS-KI standard covers 42 distinct rules across 6 channels and 4 transport modes
- The EU TSI Telematics regulation applies to all 27 member states
- DB, ÖBB, SBB, SNCF, and dozens of other operators must all comply — each interpreting the same text

## The Solution: OSCAL4Rail

### Machine-readable by design

OSCAL4Rail converts regulations into **NIST OSCAL Catalog** format — a structured YAML/JSON/XML format originally developed for IT security compliance (used by the US government). Every rule becomes a `control` with:

- **Verbatim quote** of the original rule text (`statement` part)
- **Applicability matrix** per channel × transport mode (`props`)
- **Stable identifier** derived from the chapter number
- **Supplementary guidance** from implementing regulations and annexes

### Why NIST OSCAL?

OSCAL was chosen because:
1. **Public domain (CC0)** — no license restrictions
2. **Formal JSON Schema** — validated, not just well-formed
3. **Existing tooling ecosystem** — IBM Trestle, OSCAL-CLI, and many more
4. **Layered model** — Catalog → Profile → Assessment matches the regulation hierarchy
5. **Proven at scale** — used across US federal agencies for FedRAMP compliance

### Deterministic, not AI-generated

The extraction pipeline is **fully deterministic**: PDF text extraction + Excel matrix parsing → OSCAL YAML. No LLM is used in the extraction itself. This means:
- Same input always produces same output
- Results are auditable
- No hallucination risk in the regulation content

LLMs can then *query* the resulting machine-readable catalog — but they do not *create* it.

### Semantic diff across versions

When a new version of BS-KI is published, OSCAL4Rail can automatically detect:
- Which rules changed their text (content change)
- Which rules changed their applicability (obligation tightened or relaxed)
- Which rules are new (added)
- Which rules were removed (deleted)

This gives compliance teams a precise, actionable changelog — not "the document was updated".

## Regulatory Context: Law-as-Code and the Railway Sector

OSCAL4Rail does not exist in isolation. Across Europe, a fundamental shift is underway: regulations should no longer be published only as text, but simultaneously as machine-readable, executable code.

### SPRIND "Law as Code" Initiative

The German Federal Agency for Disruptive Innovation (SPRIND) has launched a strategic initiative to make all German legislation hybrid-publishable (text + code) by 2028. The initiative defines five foundational elements: a legal code format definition, open-source editors, AI-assisted translation, a central repository, and training programs.

OSCAL4Rail is a **sectoral implementation of this vision** — applied specifically to railway regulations. Where SPRIND works top-down (legislator publishes code), OSCAL4Rail works bottom-up (railway companies extract and validate existing regulations). Both approaches converge toward the same goal: deterministic, machine-verifiable rules.

### Rulemapping Methodology

The Rulemapping Group provides a methodology for translating legal text into visual decision trees that capture application logic: "Under which conditions does this rule apply? What exceptions exist?" This complements OSCAL4Rail's applicability model, which captures *what* is required and *how binding* it is, but not the full decision logic of *when* it applies.

### Layered Relationship

```
Law-as-Code (SPRIND)          = political framework, format standardization
  └── Rulemapping             = methodology for decision logic extraction
        └── OSCAL4Rail        = domain-specific catalog format for railways
              └── AI Agents   = consume catalogs for compliance verification
```

### Future Convergence

Once regulatory bodies (EBA, ERA, BAV) publish regulations as official legal code, OSCAL4Rail can consume these directly — replacing the current PDF extraction pipeline with a validated upstream source. Until then, OSCAL4Rail provides the railway sector with machine-readable regulations *today*, without waiting for institutional change.

See [ADR-005](adr/ADR-005-law-as-code-relationship.md) for detailed technical alignment.

---

## Vision

OSCAL4Rail should become the **open standard for machine-readable railway regulations** under the OpenRail Association — enabling:

1. **Standards bodies** to publish regulations directly in OSCAL4Rail format
2. **Railway companies** to consume and diff catalogs automatically
3. **AI agents** to query regulations and verify IT system compliance
4. **Cross-border interoperability** through a shared, validated format
5. **Regulatory change management** as a standard engineering practice
