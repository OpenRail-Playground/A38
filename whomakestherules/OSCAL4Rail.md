# OSCAL4Rail

**Machine-readable railway regulations based on the NIST OSCAL standard.**

## What is OSCAL4Rail?

> Inspired by Arpad Vasarhelyi (Arpad.Vasarhelyi@deutschebahn.com)

OSCAL4Rail is a lightweight profile of the [NIST OSCAL](https://pages.nist.gov/OSCAL/) (Open Security Controls Assessment Language) standard, adapted for railway governance and regulations.

It enables:
- **Deterministic extraction** of rules from PDF/Word regulation documents into structured, machine-readable YAML
- **Schema validation** against the official NIST OSCAL JSON Schema
- **Cross-border interoperability** between railway companies (DB, SBB, ÖBB, SNCF, ...)
- **Change tracking** on rule level via Git versioning
- **Automated compliance checks** against regulation catalogs

## Why OSCAL?

| Requirement | OSCAL Feature |
|-------------|---------------|
| Hierarchical rule structure | Catalog → Groups → Controls |
| Machine-readable + human-readable | YAML/JSON/XML with prose fields |
| Validated against schema | Official JSON Schema from NIST |
| Extensible without breaking | `props` and `parts` for domain-specific data |
| Cross-referencing between regulations | Control Mapping model |
| Versioning & diff | Git + semantic change tracking |
| Multilingual support | Separate catalogs per language, linked via Control Mapping |

## Why not just JSON/YAML without OSCAL?

- No standard schema → every tool invents its own format
- No interoperability between organisations
- No existing tooling ecosystem
- No formal validation possible

OSCAL gives us all of this for free, while we only use the lightweight Catalog layer.

## OSCAL4Rail Catalog Format

Each regulation becomes an OSCAL Catalog. Each rule becomes a Control within that Catalog.

```yaml
catalog:
  uuid: "<UUIDv4>"
  metadata:
    title: "Regulation Title"
    version: "1.0"
    oscal-version: "1.1.3"
    props:
      - name: country
        value: "CH"
      - name: language
        value: "de"
  groups:
    - id: <regulation-prefix>-<chapter>
      title: "Chapter Title"
      controls:
        - id: <regulation-prefix>-<chapter.section>
          title: "Rule Title"
          parts:
            - name: statement
              prose: |
                «Verbatim quote from source document»
            - name: guidance
              prose: "Additional guidance (if available)"
          props:
            - name: source-chapter
              value: "2.1"
            - name: source-page
              value: "16"
            - name: applicability
              value: "verbindlich|empfohlen|nicht-relevant"
              class: "<channel>.<transport-mode>"
```

### Rail-specific extensions (via `props`)

| Property | Purpose | Example |
|----------|---------|---------|
| `source-chapter` | Chapter reference in source document | `"2.1"` |
| `source-page` | Page number in source PDF | `"16"` |
| `applicability` | Obligation level per channel × transport mode | `value: "verbindlich", class: "haltestelle.bahn"` |
| `country` | Country scope | `"CH"`, `"DE"`, `"AT"`, `"EU"` |
| `language` | Document language | `"de"`, `"fr"`, `"it"` |

### Applicability classes (channel.transport-mode)

**Channels:**
- `haltestelle` – Station/stop
- `fahrzeug-aussen.front` – Vehicle exterior front
- `fahrzeug-aussen.seite` – Vehicle exterior side
- `fahrzeug-aussen.heck` – Vehicle exterior rear
- `fahrzeug-innen` – Vehicle interior
- `daten.einlieferung` – Data delivery

**Transport modes:**
- `bahn` – Rail
- `bus-tram-metro` – Bus, Tram, Metro
- `schiff` – Ship/Ferry
- `seilbahn` – Cable car

### Obligation values

| Value | Meaning |
|-------|---------|
| `verbindlich` | Mandatory (v) |
| `empfohlen` | Recommended (e) |
| `nicht-relevant` | Not applicable (–) |

## Scope for Hack4Rail 2026

**First catalog:** Swiss "Branchenstandard Kundeninformation" (BS-KI)
- 44 rules across 6 channels and 4 transport modes
- Source: PDF (64 pages) + Excel matrix (ground truth)
- Deterministic extraction (no LLM required)

**Future catalogs:**
- TSI Telematics (EU 2026/253)
- DB Ril 420 ff.
- ÖBB equivalent regulations

## Validation

```bash
python3 validate.py rules/bs-ki-de.yaml
# ✅ rules/bs-ki-de.yaml: Valid OSCAL Catalog
```

## Project

- **Repository:** https://github.com/OpenRail-Playground/A38
- **Team:** A38 (DB, SBB, ÖBB)
- **Context:** [Hack4Rail 2026](https://hack4rail.org/) – Challenge 7 "Who Makes the Rules"
- **License:** Apache 2.0
