# A38 – Pitch Outline (Who Makes the Rules)

## Zeitrahmen
5 Minuten (Hack4Rail Standard)

---

## 1. Hook / Intro (60s)

**Aktion:** Simon bringt eine Kiste Druckerpapier auf die Bühne.

> "Here are the regulations. Read them. All of them. Now tell me: which rules apply to which channel and transport mode."

**Pause.**

**Aktion:** Simon holt die ZWEITE Kiste Papier.

> "Oh, and here's the new version. Compare it with the old one. Tell me what changed."

**Pause. Blick ins Publikum.**

> "This is what railway companies do today. With every regulation update. Manually. For hundreds of rules across multiple countries and languages."

---

## 2. The Idea: Machine-Readable First (60s)

**Folie:** PDF/Word → OSCAL Catalog (Umkehrung)

> "What if we flip the paradigm?"

> "Today: Regulations are written in Word, published as PDF, and humans extract what applies."

> "Our proposal: **Machine-readable first, PDF second.** The canonical source is structured data. The PDF is a generated view."

**Folie:** NIST OSCAL Logo + BSI reference

> "This is not a new idea. NIST publishes security controls as OSCAL – machine-readable governance. The German BSI adopted it. We bring it to rail."

> "We call it: **OSCAL4Rail**."

---

## 3. What is OSCAL4Rail? (60s)

**Folie:** OSCAL Catalog Structure

> "OSCAL4Rail is a lightweight profile of the NIST OSCAL standard, adapted for railway regulations."

```
Catalog → Groups → Controls
  │         │        │
  │         │        └─ One rule (verbatim text + applicability)
  │         └─ One chapter
  └─ One regulation (e.g. BS-KI Switzerland)
```

**Key features:**
- Validated against official NIST JSON Schema
- Verbatim rule text (no interpretation, no paraphrasing)
- Applicability matrix: which rule applies where (channel × transport mode)
- Versioned in Git → full changelog for free

---

## 4. Demo / Proof of Concept (60s)

**Folie:** BS-KI (Swiss Customer Information Standard)

> "We tested it with the Swiss 'Branchenstandard Kundeninformation' – 44 rules, 6 channels, 4 transport modes."

**What we did:**
- Excel matrix (ground truth) → parsed deterministically
- PDF (64 pages) → chapter-level text extraction
- Combined into one OSCAL Catalog YAML
- Validated against NIST JSON Schema ✅

**Folie:** Diff / Changelog

> "And here's the magic: because it's in Git, you get versioning and history for free. 'What changed between version 2024 and 2025?' becomes a `git diff`."

---

## 5. Ausblick: Next Steps (60s)

**Folie:** Roadmap

**Establishing the standard:**
> "OSCAL4Rail as the standard format for machine-readable rail governance."

**Adoption path – low friction, high value:**
1. Start with IT/ITS regulations (already structured, digital-native)
2. Web editor that **behaves like Word** (low learning curve for governance owners)
3. Import existing governance documents → validate → publish as OSCAL
4. Gradually expand: safety regulations, cross-border (TSI), operational rules

**Folie:** Word-like Editor → OSCAL → PDF + API

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ Web Editor   │ ──► │ OSCAL4Rail  │ ──► │ PDF (view)   │
│ (looks like  │     │ (canonical  │     │ API (machine)│
│  Word)       │     │  source)    │     │ Diff/Change  │
└──────────────┘     └─────────────┘     └──────────────┘
```

> "Governance owners keep writing like they always have. But the output is structured, versioned, and machine-readable. Little change in workflow, massive gain in usability."

---

## 6. Closing (30s)

> "Who makes the rules? Humans do. But how we publish, version, and compare them – that should be a machine's job."

> "OSCAL4Rail. Machine-readable governance for railways. Starting today."

---

## Folien-Bedarf

1. Two boxes of paper (physical prop)
2. PDF/Word → OSCAL flip diagram
3. NIST OSCAL + BSI reference
4. OSCAL Catalog structure (Catalog → Group → Control)
5. BS-KI example (44 rules, applicability matrix)
6. Git diff / changelog visualization
7. Roadmap (IT/ITS → Safety → Cross-border)
8. Word-like Editor → OSCAL → outputs diagram

## Requisiten

- 2 Kisten Druckerpapier (am besten mit bedruckten "Regelwerk"-Deckblättern)

---

*Erstellt: 23.06.2026, 15:25*
