# Automatic Contract Analysis (ACA) – Arbeitsplan

## Intent

**Problem:** Die SBB verwaltet tausende Infrastrukturverträge (Kreuzungsbauwerke, Finanzierungsvereinbarungen, Bahnhofverträge, Betrieb & Nutzung). Die Verträge liegen als PDFs vor – von handschriftlich ergänzten Dokumenten ab 1926 bis zu aktuellen Finanzierungsvereinbarungen. Die Vertragsdaten müssen manuell in SAP/ContrAct erfasst werden.

**Ziel:** Eine KI-gestützte Pipeline, die aus PDF-Verträgen automatisch strukturierte Daten extrahiert (13 Felder + Kostenteiler) – mit Qualitätskennzeichen und Quellenangaben pro Feld. Validiert gegen ein maschinenlesbares Taxonomie-Schema.

**Was wir NICHT tun:** Einen produktionsreifen SAP-Connector bauen. Wir zeigen den Weg vom PDF zum strukturierten, validierten Datensatz.

## Architektur-Idee: Taxonomie als Schema (analog OSCAL4Rail)

Wie bei Challenge 1 (Who Makes the Rules) das Regelwerk als OSCAL-Catalog maschinenlesbar wird, machen wir hier die **Vertragstyp-Taxonomie** maschinenlesbar:

```
OSCAL4Rail (Challenge 1)              Contract Taxonomy (Challenge 2)
─────────────────────────             ──────────────────────────────
Catalog → Group → Control             Ebene 1 → 2 → 3 → Baustein-Pool (Ebene 4)
Regelwerk strukturieren               Vertragskonstrukt strukturieren
LLM extrahiert Regeln                 LLM extrahiert Vertragsfelder
Validierung gegen OSCAL-Schema        Validierung gegen Taxonomie-Schema
```

### Taxonomie-Modell

```
Ebene 1: Infrastrukturverträge (fix)
│
├─ Ebene 2: Zusammenarbeit bei Anlagen
│  ├─ Ebene 3: Vorstudie (V1)           ─┐
│  ├─ Ebene 3: Projektierung (V2)        │
│  ├─ Ebene 3: Ausführung (V3)           ├─ Pool A (9 Bausteine, nicht alle überall)
│  ├─ Ebene 3: Ausf.+Betrieb (V3&4)     │
│  └─ Ebene 3: Betrieb/Unterhalt (V4)   ─┘  ← kein Multiprojekt
│
│  Pool A: Brücke, Bahnübergang, Verkehrswege, Bahnhof,
│          Bahntechnik, Naturrisiken, Durchleitung,
│          Rahmenvereinbarung, Multiprojekt
│
└─ Ebene 2: Grundstücknutzung
   ├─ Ebene 3: Nutzungsverträge     ── Pool B: Pflege, Fläche, Wand, Gebrauchsleihe
   └─ Ebene 3: Bauten Dritter       ── Pool C: Kleinbauten, Anker
```

**Kern-Prinzip:** Die drei Baustein-Pools (A, B, C) sind **disjunkt**. Ein Vertrag hat genau einen Pfad (Ebene 2 + Ebene 3) und daraus einen oder mehrere Bausteine des zugehörigen Pools.

→ Schema: [`taxonomy.yaml`](taxonomy.yaml)

## Datenquellen

| Datei | Inhalt | Rolle |
|-------|--------|-------|
| `PDF Dateien/` (216 PDFs) | Echte SBB-Verträge in DE/FR/IT, 4 Kategorien | **Eingabe** |
| `Masterdatei H4R.xlsx` (13 MB) | Master-Referenz aller Verträge | **Ground Truth** |
| `Grundlagen/2026-06-11 Export ALLE Verträge.XLSX` | SAP-Export aller Verträge | **Ist-Zustand** |
| `Grundlagen/Versuch Business mit AI-Claude/1_system_prompt_*.md` | Ausgearbeiteter System-Prompt v1.0 | **Extraktionslogik (fertig!)** |
| `Grundlagen/Versuch Business mit AI-Claude/3_*` | Erste Ergebnisse (28 Verträge) | **Baseline** |
| `Grundlagen/2026-03-25 Vertragstyp Ebenen.xlsx` | Vertragstyp-Taxonomie | → `taxonomy.yaml` |
| `Grundlagen/2026-06-11_SBB Linien.xlsx` | SBB-Linienverzeichnis | Referenz Feld 4 |
| `Grundlagen/2026-06-09_Gemeindestand.xlsx` | Gemeinderegister CH | Referenz Feld 12 |
| `Grundlagen/Inventarliste Brücken mit UUID.xlsx` | Brücken-Inventar | Objektzuordnung |

## MVP (24h Hackathon)

### Was wir liefern

1. **Taxonomie-Schema** (`taxonomy.yaml`) – maschinenlesbar, validierbar
2. **Extraction Pipeline** – PDF → markitdown → LLM → JSON
3. **Validierung** – JSON gegen Taxonomie + JSON-Schema prüfen
4. **Qualitätsmessung** – Ergebnisse gegen Masterdatei vergleichen
5. **Demo** – live ein PDF reinschieben, validiertes JSON rausholen

### Was NICHT im Scope

- Kein SAP-Connector
- Kein Produktiv-Deployment
- Keine vollständige Batch-Verarbeitung aller 216 PDFs
- Kein Multi-Model-Benchmark

## Phasen

### Phase 1: Grundlagen (1–2h) ✅
- [x] Taxonomie-Schema erstellen (`taxonomy.yaml`)
- [x] System-Prompt v1.0 reviewen (liegt fertig vor)
- [ ] JSON-Schema aus System-Prompt Abschnitt 8 ableiten
- [ ] Masterdatei-Header lesen → Zielstruktur verstehen

### Phase 2: Walking Skeleton – 1 Vertrag End-to-End (2–3h) ✅
- [x] PDF gewählt: 90051045 (KBW/DE, ASTRA/SBB Brücke Balsberg)
- [x] `markitdown` → Text-Extraktion (2727 Zeilen, davon 880 Vertragstext)
- [x] LLM-Extraktion mit System-Prompt v1.0
- [x] Iteration 1: gekürzt (380 Zeilen) → Betriebskosten fehlen
- [x] Iteration 2: vollständig (880 Zeilen) → alle Kosten korrekt
- [x] Taxonomie-Validierung bestanden
- [x] Manuelle Verifikation durch Team → Betriebskosten-Fehler in v1 identifiziert, in v2 behoben
- [ ] **Ergebnis gegen Masterdatei `Masterdatei H4R.xlsx` prüfen** (Vertrag 90051045 suchen)

### Phase 3: Weitere Vertragstypen testen (offen)
- [ ] **Grundstücknutzung** – z.B. aus `PDF Dateien/KBW/DE/90051158` (Wandbemalung/Graffiti)
- [ ] **FinVer** (Finanzierungsvereinbarung) – z.B. aus `PDF Dateien/FinVer/DE/`
- [ ] **Bahnhofvertrag** – z.B. aus `PDF Dateien/Bahnhofverträge/DE/`
- [ ] **Älterer Vertrag** (handschriftlich, vor 1990) – z.B. `PDF Dateien/KBW/DE/90004096`
- [ ] **Französisch** – z.B. aus `PDF Dateien/KBW/FR/`
- [ ] **Italienisch** – z.B. aus `PDF Dateien/KBW/IT/`
- [ ] Ergebnisse jeweils gegen Masterdatei prüfen

### Phase 4: Automatische Qualitätsmessung (offen)
- [ ] Masterdatei-Spalten auf JSON-Felder mappen
- [ ] Automatischer Vergleich: extrahierte Werte vs. Masterdatei
- [ ] Metriken: Accuracy pro Feld, eindeutig/abgeleitet/fehlend
- [ ] HTML-Report mit Ergebnissen

### Phase 5: Demo (offen)
- [ ] One-Pager / Pitch
- [ ] Live-Demo: PDF → validiertes JSON
- [ ] Zukunftsvision

## Verifikationsdaten

Für den manuellen und automatisierten Abgleich stehen zwei Quellen bereit:

| Datei | Inhalt | Nutzung |
|-------|--------|---------|
| `Masterdatei H4R.xlsx` (13 MB) | Alle Verträge mit Soll-Werten für die 13 Felder | **Ground Truth** – extrahierte JSONs dagegen prüfen |
| `Grundlagen/2026-06-11 Export ALLE Verträge.XLSX` (8.5 MB) | SAP-Export aller Verträge (Ist-Zustand) | **Ist-Stand** – was heute im System steht |
| `Grundlagen/Versuch Business mit AI-Claude/3_Hack4Rail_Extraktion_Resultate_EXCEL.xlsx` | Bisherige Claude-Extraktion (28 Verträge) | **Baseline** – Vergleich mit unserer Pipeline |

### Verifikations-Workflow

```
Extrahiertes JSON (results/<nr>.json)
       │
       ├─► vs. Masterdatei H4R.xlsx     → Feld-für-Feld-Vergleich (Soll)
       ├─► vs. SAP-Export               → Abgleich mit bestehendem System
       └─► vs. Bisherige Ergebnisse     → Delta zur Claude-Baseline
```

## Zukunftsvision

### Kurzfristig (3–6 Monate)
- Batch aller ~5.000 Verträge
- Human-in-the-Loop für `abgeleitet`/`fehlend`
- SAP/ContrAct Prefill
- Multi-Language (FR/IT)

### Mittelfristig (6–12 Monate)
- Vertragsbeziehungsgraph (Dach → Objekt → Nachtrag)
- Anomalie-Erkennung (fehlende Laufzeit, widersprüchliche Daten)
- Proaktive Alerts (Ablauf, fehlender Nachfolger)

### Langfristig (>12 Monate)
- Template-basierte Vertragserzeugung
- Cross-Bahn-Interoperabilität (DB/ÖBB/SBB)
- **Brücke zu Challenge 1:** Verträge gegen OSCAL4Rail-Regelwerke prüfen (Compliance)

## Output-Struktur

```
aca/
├── PLAN.md                          # Dieser Plan
├── taxonomy.yaml                    # Vertragstyp-Taxonomie (Baustein-Pool-Modell)
├── schema/
│   └── contract-extraction.json     # JSON-Schema (aus System-Prompt Abschnitt 8)
├── extract.py                       # Extraction Pipeline
├── validate.py                      # Validierung (Schema + Taxonomie)
├── compare.py                       # Vergleich mit Masterdatei
├── results/
│   └── <vertragsnummer>.json        # Extrahierte Daten
├── reports/
│   └── quality-report.html          # Qualitäts-Dashboard
├── Masterdatei H4R.xlsx
├── Grundlagen/
└── PDF Dateien/
```

## Tools

- `markitdown` – PDF → Text (`~/Library/Python/3.14/bin/markitdown`)
- `openpyxl` – Excel parsen
- Python 3.14
- LLM-API (Claude)
- `jsonschema` – Validierung

## Bisherige Ergebnisse (Stand 23.06.2026, 11:50)

### Getestete Verträge

| Nr. | Vertrag | Typ | Iteration | Ergebnis |
|-----|---------|-----|-----------|----------|
| 1 | 90051045 (ASTRA/SBB Brücke Balsberg) | Zusammenarbeit › V3&4 › KBW Brücke | v1 (gekürzt) | 6 eindeutig, Betriebskosten fehlen |
| 1 | 90051045 | | v2 (vollständig) | **8 eindeutig**, alle Kosten korrekt |

### Learnings (Pipeline)

1. **Pre-Processing:** Bauwerksplan-Anhänge abschneiden bei letzter "Seite N/N"-Markierung
2. **Volltext:** Immer kompletten Vertragstext übergeben (nie willkürlich kürzen)
3. **Handschrift:** Vertragsbeginn (Unterschriftsdatum) bleibt `fehlend` – ist erwartetes Verhalten
4. **Iteratives Feedback:** Verifikation nach Iteration 1 führt zu gezielter Verbesserung

## Offene Entscheidungen

- [ ] **LLM:** Claude API? Lokal? Was ist verfügbar?
- [ ] **Scope PDFs:** Alle 216 oder Untermenge (nur DE, nur KBW)?
- [ ] **Masterdatei-Mapping:** Welche Spalten → welche JSON-Felder?
- [ ] **Demo-Format:** Live, Slides, oder beides?

---

*Erstellt: 23.06.2026, 10:44 | Letzte Aktualisierung: 11:50*
