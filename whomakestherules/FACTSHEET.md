# Hack4Rail 2026 – FactSheet: Who Makes the Rules (Challenge 7)

## Slide 1 – Team

- **Challenge Title:** Who Makes the Rules
- **Challenge Owner:** (Challenge Owner von oev-info/KKI)
- **Team name:** A38
- **Team Members:**
  - Simon Engel (ÖBB)
  - Jens Grote (DB)
  - Rebeca Perez (SBB)
  - Jonatha Wulf (DB)
  - Simon Freihart (SBB)
  - Simon Noelle (ÖBB)

## Slide 2 – Challenge & Solution

### Description of the Challenge

Railway regulations (safety rules, passenger information standards) are scattered across heterogeneous PDF/Word documents. Nobody can efficiently find the relevant rule. Changes between versions are invisible. Rules are free text – and worse: they are interpreted by individuals based on their personal context, leading to inconsistent, non-deterministic application across organisations and countries.

### Description of the Solution or Idea

OSCAL4Rail – a lightweight profile of the NIST OSCAL standard adapted for railway regulations. Deterministic extraction pipeline: PDF + Excel matrix → validated, machine-readable YAML catalog. Every rule is verbatim-quoted, schema-validated, and diffable across versions.

### Project Links

- **GitHub Repository:** https://github.com/OpenRail-Playground/A38
- **Demo:** `python3 validate.py` – validates the full catalog against NIST OSCAL schema
- **Further Links:** https://pages.nist.gov/OSCAL/

## Slide 3 – Impact & Next Steps

### Who are the user groups?

Standards bodies (KKI, BAV), railway companies (SBB, DB, ÖBB, SNCF), compliance teams, IT departments implementing passenger information systems.

### Are there any existing alternatives?

Manual PDF reading, proprietary compliance tools, no open standard for railway regulations exists.

### What is the economic benefit?

Reduced compliance effort: automated change tracking eliminates manual document comparison. Faster implementation of regulation updates across systems.

### Which alternatives are out of the question and why?

Proprietary formats (vendor lock-in), pure LLM extraction without validation (non-deterministic, not auditable).

### What are the positive impacts on the rail system?

Interoperability between railway companies. Faster adoption of new standards. Transparency for passengers (consistent information across borders).

### Are there any foreseeable risks, hurdles or dependencies?

Adoption requires buy-in from standards bodies. Regulations must keep stable chapter numbering. Multi-language support (DE/FR/IT) needs further work.

### What is the maturity level of the technologies used?

NIST OSCAL: mature (v1.1.3, used in US government). Our OSCAL4Rail profile: prototype (Hack4Rail 2026). Python tooling: production-ready libraries.

### What are the next steps? What do you need?

1. Manual verification of 42 extracted rules
2. Extend to other regulations (TSI, Ril 420)
3. Build diff/changelog tooling
4. Establish OSCAL4Rail as an official OpenRail Association open-source project – with full documentation, examples, OSS governance, release management, and a communication strategy for adoption across European railways

**Need:** Collaboration with standards bodies (KKI). Access to further regulation documents. Community feedback on the OSCAL4Rail format. OpenRail Association sponsorship for long-term maintenance and visibility.
