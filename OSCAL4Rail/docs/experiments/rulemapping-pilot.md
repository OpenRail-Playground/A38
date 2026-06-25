# Experiment: Rulemapping Builder Pilot – BS-KI 2.1

> **Date:** 2026-06-25
> **Status:** Planned
> **Goal:** Evaluate whether the Rulemapping methodology and Builder tool can complement OSCAL4Rail's applicability model with decision logic.

---

## Context

OSCAL4Rail captures **what** is required (verbatim rule text) and **how binding** it is (verbindlich/empfohlen per channel × transport mode). It does **not** capture the **decision logic** — i.e. under which conditions a rule applies or can be waived.

The Rulemapping Group's Builder ([builder.rulemapping.org](https://builder.rulemapping.org)) provides a visual tool for modeling decision trees from legal text. This experiment tests whether it can model the applicability logic of a BS-KI control.

See [ADR-005](../adr/ADR-005-law-as-code-relationship.md) for the strategic relationship between OSCAL4Rail and Law-as-Code initiatives.

---

## Test Subject: BS-KI 2.1 – Aktuelle Uhrzeit

### Source Text (verbatim from BS-KI v1.0, Chapter 2.1)

> „Bei Haltestellen mit weniger als 800 Ein- und Aussteigern pro Tag kann auf die Angabe der Uhrzeit verzichtet werden. Die aktuelle Uhrzeit ist für die Kundschaft ein zentrales Element zur Orientierung."

### Applicability (from OSCAL4Rail catalog)

| Channel | Transport Mode | Obligation |
|---------|---------------|------------|
| Haltestelle | Bahn | verbindlich |
| Haltestelle | Bus/Tram/Metro | empfohlen |
| Fahrzeug innen | alle | empfohlen |
| Fahrzeug außen | alle | nicht relevant |
| Daten (Einlieferung) | alle | nicht relevant |

### Decision Logic (not yet captured in OSCAL4Rail)

The rule contains an explicit threshold condition: stations with fewer than 800 daily passengers may waive the requirement. This is decision logic that goes beyond the simple applicability matrix.

---

## Expected Decision Tree

```
[Muss die aktuelle Uhrzeit angezeigt werden?]
│
├── Kanal = Haltestelle?
│   ├── JA → Verkehrsträger = Bahn?
│   │   ├── JA → ≥ 800 Ein-/Aussteiger pro Tag?
│   │   │   ├── JA → VERBINDLICH: Uhrzeit anzeigen
│   │   │   └── NEIN → KANN VERZICHTET WERDEN
│   │   └── NEIN (Bus/Tram/Metro)
│   │       └── EMPFOHLEN: Uhrzeit anzeigen
│   └── NEIN →
│       ├── Kanal = Fahrzeug innen?
│       │   └── EMPFOHLEN: Uhrzeit anzeigen
│       └── Kanal = Fahrzeug außen / Daten?
│           └── NICHT RELEVANT
```

---

## Steps to Execute

1. **Open** [builder.rulemapping.org](https://builder.rulemapping.org) and create a free account
2. **Create new Rulemap** with title: `BS-KI 2.1 – Aktuelle Uhrzeit`
3. **Model the decision tree** as described above
4. **Export** the result (RUML/JSON — whatever the Builder offers)
5. **Document** the export format and contents below
6. **Evaluate** against the questions in the evaluation matrix

---

## Evaluation Matrix

| # | Question | Answer | Notes |
|---|----------|--------|-------|
| 1 | Does the Builder support threshold/quantitative conditions (≥ 800)? | | |
| 2 | Does the Builder support multi-dimensional branching (channel × transport)? | | |
| 3 | Can the source regulation text be attached/referenced? | | |
| 4 | What export format does the Builder produce? | | |
| 5 | Can the export be referenced from an OSCAL4Rail control (e.g. as `link` or `back-matter` resource)? | | |
| 6 | Does the exported format contain stable identifiers for nodes? | | |
| 7 | Is the export machine-readable and schema-validated? | | |
| 8 | Could an AI agent traverse the decision tree programmatically? | | |
| 9 | How does the Builder handle the "kann verzichtet werden" case (permission, not prohibition)? | | |
| 10 | Is the RUML format documented enough to write a parser/converter? | | |

---

## Results

> **To be filled after executing the experiment.**

### Export Format

```
(paste exported RUML/JSON here)
```

### Screenshots

(add screenshots of the decision tree in the Builder)

### Findings

| Finding | Impact on OSCAL4Rail |
|---------|---------------------|
| | |

---

## Conclusion & Next Steps

> To be written after experiment execution.

Possible outcomes:
- **Positive:** Rulemapping complements OSCAL4Rail → define integration pattern (e.g. link RUML from OSCAL control)
- **Neutral:** Interesting methodology but export format incompatible → document as adjacent approach
- **Negative:** Builder cannot model railway-specific logic → document limitations, consider Catala or custom approach
