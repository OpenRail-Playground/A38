# ConTextractors – Pitch Outline

## Zeitrahmen
5 Minuten (Hack4Rail Standard)

---

## 1. Hook / Intro (60s)

**Aktion:** 5 Aktenordner auf die Bühne tragen.

**Folie:** Screenshot der Vertragstyp-Ebenen-Matrix (aus Excel) einblenden.

**Sagen:**
> "Here are 5 paper contracts. And here is the classification schema – 4 levels, 15 building blocks, multiple languages. Now: please read these contracts and sort them according to this schema."

**Pause. Blick ins Publikum.**

> "This is what SBB does manually. For 5,000 contracts. In German, French, and Italian. Some handwritten. Some from 1926."

**Aktion:** Ordner wegtragen / zur Seite schieben.

> "Yeah, no. Not like this."

**Folie:** Screenshot Masterdatei (Excel mit 33 Spalten, manuell befüllt)

> "This is what humans did: they read 5,000 PDFs and filled in this spreadsheet. Manually. Column by column."

**Folie:** Unsere JSON-Extraktion (Ergebnis mit Qualitätskennzeichen)

> "This is what our AI does: same contract, structured output, with quality indicators and source references. In seconds."

**Folie:** Vergleichstabelle – und der Fehler

> "And here's the punchline: when we compared AI vs. human... the AI found an error in the manual data. The spreadsheet says 'Bahnübergang'. The contract clearly says 'Bahnbrücke'. The machine was right, the human was wrong."

---

## 2. Problem (30s)

- 5.000+ Infrastrukturverträge (PDF, Scans, handschriftlich)
- Manuelle Erfassung in SAP/ContrAct
- 13 Felder pro Vertrag + Kostenteiler + Abhängigkeiten
- Fehleranfällig: wir haben im Test einen Fehler in der Masterdatei gefunden
- Multilingual: DE / FR / IT

---

## 3. Lösung: Machine-Readable Taxonomy + LLM Extraction (90s)

**Folie:** Taxonomie-Baum (Ebene 1 → 2 → 3 → Baustein-Pools)

> "Step 1: We made the classification schema machine-readable."

```
taxonomy.yaml → 3 disjoint building-block pools
                 with allowed combinations per contract phase
```

**Folie:** Pipeline-Diagramm

> "Step 2: PDF in, structured JSON out."

```
PDF → markitdown (text extraction) → LLM + System Prompt → validated JSON
```

**Folie:** JSON-Ergebnis (90051045_v2.json, gekürzt)

> "Every field has a quality indicator: eindeutig, abgeleitet, fehlend. Every field has a source reference. The machine tells you WHERE it found the data."

---

## 4. Ergebnisse / Demo (60s)

**Folie:** Vergleichstabelle (Masterdatei vs. Extraktion)

> "7 out of 10 fields match. One field: our extraction is MORE CORRECT than the manual data. The master file says 'Bahnübergang' – the contract clearly says 'Bahnbrücke'."

**Folie:** Multi-LLM-Vergleich (Claude vs. Cortex)

> "Same prompt, same input, two different models. We can compare and validate."

**Key Messages:**
- Iterativer Ansatz: Iteration 1 → Fehler gefunden → Iteration 2 → korrekt
- Pipeline findet Fehler in Stammdaten
- Taxonomie-Validierung: nur erlaubte Kombinationen

---

## 5. Ausblick / Zukunft (60s)

**Folie:** Zukunftsvision

**Kurzfristig:**
- Batch-Verarbeitung aller 5.000 Verträge
- Human-in-the-Loop für unsichere Felder
- SAP/ContrAct Prefill

**Mittelfristig:**
- **Asset-Zuordnung:** Verträge automatisch den physischen Bauwerken zuordnen (UUID aus Brücken-Inventar → Vertragsnummer)
- Vertragsbeziehungsgraph (Dach → Objekt → Nachtrag)
- Anomalie-Erkennung (fehlende Laufzeiten, widersprüchliche Daten)

**Langfristig:**
- Cross-Bahn-Interoperabilität (DB/ÖBB/SBB)
- **Brücke zu Challenge 1:** Verträge gegen OSCAL4Rail-Regelwerke prüfen
- Automatische Vertragsentwürfe aus Templates

---

## 6. Closing (30s)

> "We turned 5 Aktenordner into structured, validated, machine-readable data. With source references. In minutes, not days. And we found errors that humans missed."

> "We are the **ConTextractors**."

---

## Folien-Bedarf

1. Vertragstyp-Ebenen-Matrix (Screenshot Excel)
2. Taxonomie-Baum (Ebene 1→2→3→Pools)
3. Pipeline-Diagramm (PDF → Text → LLM → JSON)
4. JSON-Ergebnis (gekürzt, mit Qualitätskennzeichen)
5. Vergleichstabelle (Masterdatei vs. Extraktion)
6. Multi-LLM-Vergleich (Claude vs. Cortex)
7. Zukunftsvision (Asset-Zuordnung, Graph, Cross-Bahn)

## Requisiten

- 5 Aktenordner (mit echten oder gedruckten Verträgen)
- Laptop für Live-Demo (optional)

---

*Erstellt: 23.06.2026, 14:48*
