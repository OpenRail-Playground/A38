# Hack4Rail 2026 – FactSheet: Automatic Contract Analysis (Challenge 11)

## Slide 1 – Team

- **Challenge Title:** Automatic Contract Analysis
- **Challenge Owner:** SBB Infrastruktur
- **Team name:** TheConTextractors
- **Team Members:**
  - Simon Noelle (ÖBB)
  - Simon Engel (ÖBB)
  - Jens Grote (DB)

## Slide 2 – Challenge & Solution

### Description of the Challenge

SBB manages thousands of infrastructure contracts (crossing structures, financing agreements, station contracts, operations & usage). Contracts exist as PDFs – from handwritten documents dating back to 1926 to current financing agreements. Contract data must be manually captured in SAP/ContrAct: 13 fields + cost allocation per contract. This is time-consuming, error-prone, and does not scale.

### Description of the Solution or Idea

AI-powered extraction pipeline: PDF → markitdown (text extraction) → LLM (structured data extraction) → validated JSON. Each extracted field includes a confidence level (eindeutig/abgeleitet/fehlend) and source reference. Validated against a machine-readable contract taxonomy schema. Deterministic verification against a master reference file.

### Project Links

- **GitHub Repository:** https://github.com/OpenRail-Playground/A38
- **Demo:** Live extraction of a contract PDF → validated JSON output
- **Further Links:** –

## Slide 3 – Impact & Next Steps

### Who are the user groups?

SBB Infrastruktur (contract management), asset managers, finance departments, legal teams. Potentially applicable to DB, ÖBB, and other railways with similar contract portfolios.

### Are there any existing alternatives?

Manual data entry into SAP/ContrAct. Previous Claude-based extraction attempt (28 contracts, limited validation). No production-grade automated solution exists.

### What is the economic benefit?

~5,000 contracts to be digitised. Manual effort: estimated 30-60 min per contract. Automated extraction reduces this to minutes with human-in-the-loop verification for edge cases. Enables proactive contract management (expiry alerts, missing successors).

### Which alternatives are out of the question and why?

Pure OCR without LLM (cannot handle semantic extraction from complex legal text). Fully manual approach (does not scale to 5,000 contracts). Unvalidated LLM output without taxonomy schema (not auditable).

### What are the positive impacts on the rail system?

Better contract oversight reduces risk of missed obligations. Enables cross-company contract interoperability. Foundation for automated compliance checking (bridge to OSCAL4Rail).

### Are there any foreseeable risks, hurdles or dependencies?

Older contracts (pre-1990, handwritten) have lower extraction quality. Multi-language support (DE/FR/IT) needs tuning. LLM availability and cost for batch processing. Data privacy for contract parties.

### What is the maturity level of the technologies used?

LLM extraction: mature (Claude Sonnet 4, GPT-4). PDF parsing (markitdown): production-ready. JSON Schema validation: standard. Taxonomy model: prototype (Hack4Rail 2026).

### What are the next steps? What do you need?

A ready-to-use prototype has been delivered. The challenge owners can start further implementation as early as next week and complete the contract classification process within the next months.

1. Challenge owners continue with the prototype immediately
2. Extend extraction to all contract types (FinVer, Bahnhofverträge, Grundstücknutzung)
3. Batch processing of ~5,000 contracts with quality measurement
4. Multi-language support (FR/IT)
5. Human-in-the-loop workflow for low-confidence fields
6. SAP/ContrAct prefill integration

**Need:** LLM API budget for batch processing. SBB domain expertise for ongoing validation. Collaboration with SAP/ContrAct team for integration path.
