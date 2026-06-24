# OSCAL4Rail – Architecture Documentation (arc42)

> **Version:** 0.1.0 (Hack4Rail 2026 – initial draft)
> **License:** CC0 1.0 Universal (public domain)
> **Inspired by:** Arpad Vasarhelyi (Arpad.Vasarhelyi@deutschebahn.com)

---

## Table of Contents

1. [Introduction and Goals](#1-introduction-and-goals)
2. [Architecture Constraints](#2-architecture-constraints)
3. [System Scope and Context](#3-system-scope-and-context)
4. [Solution Strategy](#4-solution-strategy)
5. [Building Block View](#5-building-block-view)
6. [Runtime View](#6-runtime-view)
7. [Deployment View](#7-deployment-view)
8. [Cross-cutting Concepts](#8-cross-cutting-concepts)
9. [Architecture Decisions](#9-architecture-decisions)
10. [Quality Requirements](#10-quality-requirements)
11. [Risks and Technical Debt](#11-risks-and-technical-debt)
12. [Glossary](#12-glossary)

---

## 1. Introduction and Goals

### 1.1 Purpose

OSCAL4Rail is a lightweight profile of the [NIST OSCAL](https://pages.nist.gov/OSCAL/) (Open Security Controls Assessment Language) standard, adapted for railway governance and regulations.

Railway regulations (safety rules, passenger information standards) are scattered across heterogeneous PDF/Word documents. Rules are free text – and worse: they are interpreted by individuals based on their personal context, leading to inconsistent, non-deterministic application across organisations and countries. Changes between versions are invisible.

OSCAL4Rail makes railway regulations **machine-readable, schema-validated, versionable, and diffable**.

### 1.2 Goals

| Priority | Goal |
|----------|------|
| G-1 | Deterministic extraction of rules from PDF/Excel sources into validated YAML |
| G-2 | Verbatim quoting of every rule from its source document |
| G-3 | Schema validation against official NIST OSCAL JSON Schema |
| G-4 | Stable identifiers for rules to enable diff and change tracking across versions |
| G-5 | Extensibility to any railway regulation (TSI, national standards, company rules) |
| G-6 | Multilingual support (DE/FR/IT/EN) |

### 1.3 Stakeholders

| Role | Organisation | Interest |
|------|-------------|----------|
| Standards bodies | KKI, BAV (CH), ERA (EU) | Publish regulations in machine-readable format |
| Railway companies | SBB, DB, ÖBB, SNCF, ... | Consume regulations, check compliance |
| IT departments | All railways | Implement passenger information systems |
| Compliance teams | All railways | Track regulatory changes |
| OpenRail Association | OpenRail | Host and maintain as OSS project |

---

## 2. Architecture Constraints

### 2.1 Technical Constraints

| ID | Constraint | Rationale |
|----|-----------|-----------|
| TC-1 | Output must be valid NIST OSCAL Catalog (JSON Schema v1.1.3) | Interoperability with existing OSCAL tooling |
| TC-2 | Rule text must be verbatim from source document | Auditability, no paraphrasing |
| TC-3 | Rule IDs derived from chapter numbers, not page numbers | Stability across document versions |
| TC-4 | No LLM required for extraction pipeline | Deterministic, reproducible results |
| TC-5 | Source files (PDF, Excel) remain canonical | OSCAL4Rail is derived, not authoritative |

### 2.2 Organisational Constraints

| ID | Constraint | Rationale |
|----|-----------|-----------|
| OC-1 | License: Apache 2.0 | OpenRail Association OSS standard |
| OC-2 | NIST OSCAL base: CC0 1.0 (public domain) | No license conflict |
| OC-3 | Language of catalogs follows source document | DE/FR/IT separate catalogs |

### 2.3 Conventions

- Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`)
- Semantic Versioning for catalog releases (Major.Minor.Patch)
- GitHub Flow (feature branch → PR → merge to main)

---

## 3. System Scope and Context

### 3.1 Business Context

```
┌─────────────────┐         ┌──────────────────────────────────────┐
│  Standards Body  │──PDF──▶│                                      │
│  (KKI, BAV, ERA) │──XLSX─▶│           OSCAL4Rail                 │
└─────────────────┘         │                                      │──YAML──▶  Railway IT Systems
                             │  Extraction + Validation Pipeline    │──JSON──▶  Compliance Tools
┌─────────────────┐         │                                      │──Diff──▶  Change Notifications
│  Previous        │──YAML─▶│                                      │
│  Catalog Version │         └──────────────────────────────────────┘
└─────────────────┘
```

### 3.2 Technical Context

| Interface | Direction | Format | Description |
|-----------|-----------|--------|-------------|
| PDF regulations | Input | PDF | Source regulation documents |
| Excel matrix | Input | XLSX | Applicability matrix (v/e/–) |
| OSCAL Catalog | Output | YAML | Machine-readable regulation catalog |
| NIST JSON Schema | Validation | JSON Schema | Official OSCAL schema v1.1.3 |
| Git repository | Storage | Git | Version control and diff |

---

## 4. Solution Strategy

### 4.1 Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Base standard | NIST OSCAL Catalog | Mature, public domain, existing tooling ecosystem |
| Extraction method | Deterministic (markitdown + openpyxl) | Reproducible, auditable, no LLM required |
| Rule identifier | Chapter number (e.g. `bs-ki-2.1`) | Stable across document versions |
| Applicability model | OSCAL `props` with `class` attribute | Schema-compliant, extensible |
| Version strategy | One file per regulation, Git history for diffs | Leverages existing tooling |
| Supplementary docs | `guidance` parts (ABs, Anhänge) + `back-matter` (Übergangsdokumente) | Keeps primary rule clean |

### 4.2 Quality Approach

- **Correctness:** Verbatim quotes, no paraphrasing
- **Completeness:** All matrix rows covered
- **Validity:** Continuous validation against NIST JSON Schema
- **Traceability:** Every rule references source chapter and document

---

## 5. Building Block View

### 5.1 Level 1 – System Overview

```
┌─────────────────────────────────────────────────────────┐
│                      OSCAL4Rail                          │
├───────────────┬──────────────────┬──────────────────────┤
│  Extraction   │  Catalog Builder │  Validation & Diff   │
│  Pipeline     │                  │                      │
│               │                  │                      │
│  parse_matrix │  build_catalog   │  validate.py         │
│  extract_pdf  │  (groups+controls│  diff_catalogs       │
│               │   +back-matter)  │  changelog_gen       │
└───────────────┴──────────────────┴──────────────────────┘
```

### 5.2 Level 2 – Extraction Pipeline

| Component | Responsibility | Technology |
|-----------|---------------|-----------|
| `parse_matrix` | Parse Excel Bewertungsmatrix → applicability per rule | openpyxl |
| `extract_pdf` | Extract verbatim text per chapter from regulation PDF | markitdown / pdfplumber |
| `build_catalog` | Merge matrix + PDF texts into OSCAL Catalog YAML | PyYAML |
| `validate` | Validate YAML against NIST OSCAL JSON Schema | jsonschema |
| `diff_catalogs` | Compare two catalog versions, categorise changes | PyYAML + difflib |

### 5.3 Catalog Structure

```
catalog:
  metadata:        # Regulation metadata (title, version, source)
  groups:          # Chapter hierarchy
    - group:       # e.g. "Allgemeine Informationsinhalte"
      controls:    # One control per regulation rule
        - control:
          parts:   # statement (verbatim), guidance (AB/Anhang)
          props:   # source-chapter, applicability per channel×transport
  back-matter:     # Linked resources (transition documents, supplements)
    resources:
```

---

## 6. Runtime View

### 6.1 Extraction Pipeline (new catalog version)

```
1. Download new PDF + XLSX from standards body
2. run: python3 extract.py --pdf BS-KI_DE.pdf --matrix Matrix_BS-KI_DE.xlsx
3. Output: rules/bs-ki-de.yaml
4. run: python3 validate.py rules/bs-ki-de.yaml  →  ✅ Valid OSCAL Catalog
5. git diff  →  shows changed rules at control level
6. run: python3 changelog.py  →  CHANGELOG.md
7. git commit -m "feat(bs-ki): update to v2.0"
8. git tag bs-ki/v2.0
```

### 6.2 Change Diff

```
old_catalog = load("history/bs-ki-de_v1.0.yaml")
new_catalog = load("rules/bs-ki-de.yaml")

for each control in new_catalog:
    old = find_by_id(old_catalog, control.id)
    if not old:           → NEW control
    elif old deleted:     → REMOVED control
    elif statement differs: → CHANGED (content)
    elif applicability differs: → CHANGED (obligation)
```

---

## 7. Deployment View

### 7.1 Current (Hack4Rail 2026)

```
Developer machine
├── rules/bs-ki-de.yaml     (OSCAL4Rail Catalog)
├── validate.py             (local validation)
└── GitHub repository       (version control + collaboration)
```

### 7.2 Target (OSS project)

```
GitHub (OpenRail-Playground/OSCAL4Rail)
├── .github/workflows/
│   └── validate.yml        (CI: validate all catalogs on every PR)
├── catalogs/
│   ├── bs-ki/de/           (CH passenger info standard)
│   ├── bs-ki/fr/
│   ├── tsi-tat/            (EU TSI Telematics)
│   └── ...
├── schema/
│   └── oscal-catalog.json  (NIST schema, pinned version)
├── tools/
│   ├── extract.py
│   ├── validate.py
│   └── diff.py
└── docs/
    └── arc42.md            (this document)
```

---

## 8. Cross-cutting Concepts

### 8.1 Verbatim Quoting

Every `statement` part in every control contains the **exact text** from the source document. No paraphrasing, no summarisation. This is a hard invariant.

### 8.2 Stable Identifiers

Control IDs are derived from the chapter number of the source document:

```
<regulation-prefix>-<chapter.section>[-<context>]

Examples:
  bs-ki-2.1                    # Aktuelle Uhrzeit (all contexts)
  bs-ki-3.6-fahrt              # Liniennummer in "Informationen zur Fahrt" context
```

Page numbers are NOT used as identifiers – they change with every reformatting.

### 8.3 Applicability Model

Every rule specifies its obligation per channel × transport mode as OSCAL `props`:

```yaml
- name: applicability
  value: verbindlich | empfohlen | nicht-relevant
  class: <channel>.<transport-mode>
  remarks: "optional: v e distinction abgeltungsberechtigt vs. eigenwirtschaftlich"
```

Channels: `haltestelle`, `fahrzeug-aussen.front/seite/heck`, `fahrzeug-innen`, `daten.einlieferung`
Transport modes: `bahn`, `bus-tram-metro`, `schiff`, `seilbahn`

### 8.4 Versioning

- One YAML file per regulation per language
- Old versions archived in `history/` before update
- Git diff shows changes at control level
- Tags: `<regulation>/<version>` (e.g. `bs-ki/v1.0`)

---

## 9. Architecture Decisions

### ADR-001: Use NIST OSCAL as base standard

**Status:** Accepted

**Context:** We need a machine-readable format for railway regulations that is interoperable, validatable, and extensible.

**Decision:** Use NIST OSCAL Catalog model as the base format.

**Consequences:** (+) Public domain, existing tooling, formal JSON Schema. (-) Originally designed for IT security controls, requires railway-specific extensions via `props`.

---

### ADR-002: Deterministic extraction without LLM

**Status:** Accepted

**Context:** Extraction of rules must be reproducible and auditable.

**Decision:** Use deterministic tools only: markitdown (PDF → text), openpyxl (Excel), regex (chapter detection). No LLM in the core pipeline.

**Consequences:** (+) Reproducible, auditable, no API costs. (-) Chapter structure detection requires manual mapping for edge cases.

---

### ADR-003: Chapter number as stable identifier

**Status:** Accepted

**Context:** Rule IDs must remain stable across document versions to enable semantic diff.

**Decision:** Derive control IDs from chapter numbers, not page numbers or document-internal IDs.

**Consequences:** (+) Stable across reformatting and minor updates. (-) Breaks if regulation authors renumber chapters (rare, but possible).

---

### ADR-004: One catalog file per regulation per language

**Status:** Accepted

**Context:** BS-KI exists in DE/FR/IT. TSI in EN + translations.

**Decision:** Separate YAML files per language. Cross-language linking via OSCAL Control Mapping (future).

**Consequences:** (+) Simple, independent validation per language. (-) No automatic cross-language consistency check yet.

---

## 10. Quality Requirements

### 10.1 Quality Tree

| Quality | Scenario | Measure |
|---------|----------|---------|
| Correctness | Every statement matches source PDF | Manual spot-check + verbatim quote |
| Completeness | All matrix rows covered | Automated: control count = matrix row count |
| Validity | Every catalog passes NIST schema | CI validation on every commit |
| Stability | IDs survive document reformatting | Chapter-based IDs, not page-based |
| Traceability | Every rule links to source | `source-chapter` + `source-document` props |
| Extensibility | New regulations added without breaking existing | Independent files, shared schema |

---

## 11. Risks and Technical Debt

| ID | Risk | Probability | Impact | Mitigation |
|----|------|------------|--------|------------|
| R-1 | Standards bodies renumber chapters | Low | High | Monitor chapter structure on each update |
| R-2 | PDF formatting breaks extraction | Medium | Medium | Manual review of extracted text |
| R-3 | OSCAL schema version update breaks validation | Low | Medium | Pin schema version, migrate on major OSCAL releases |
| R-4 | Adoption without standards body buy-in | Medium | High | OpenRail Association as sponsor, demonstrate value first |
| TD-1 | No automated cross-language consistency | – | Medium | Future: OSCAL Control Mapping |
| TD-2 | No CI/CD pipeline yet | – | Low | Add GitHub Actions workflow |

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| OSCAL | Open Security Controls Assessment Language (NIST standard) |
| OSCAL4Rail | Lightweight OSCAL Catalog profile for railway regulations |
| Control | A single regulation rule in OSCAL terminology |
| Group | A chapter or section grouping controls |
| Statement | The verbatim rule text (primary content of a control) |
| Guidance | Supplementary text (Ausführungsbestimmungen, Anhänge) |
| Back-matter | Linked resources (transition documents, supplements) |
| Applicability | Obligation level (verbindlich/empfohlen) per channel × transport mode |
| BS-KI | Branchenstandard Kundeninformation (Swiss passenger info standard) |
| TSI | Technical Specification for Interoperability (EU railway standard) |
| KKI | Nationale Kommission Kundeninformation (CH standards body) |
| BAV | Bundesamt für Verkehr (Swiss Federal Office of Transport) |
| ERA | European Union Agency for Railways |
| AB | Ausführungsbestimmung (implementing regulation) |
| Control Mapping | OSCAL model for cross-referencing between catalogs |
