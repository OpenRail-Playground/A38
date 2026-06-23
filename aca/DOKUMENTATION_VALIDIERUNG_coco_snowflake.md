# Validierung: JSON-Extraktionen vs. Masterdatei H4R

## Zweck

Qualitätssicherung der automatischen Vertragsextraktion. Das Skript `validate_against_masterdatei.py` prüft, ob die vom LLM (llama3.1-70b) extrahierten Vertragsfelder mit den manuell in der Masterdatei erfassten Referenzwerten übereinstimmen.

---

## Eingabedaten

### Masterdatei H4R (3).xlsx

| Eigenschaft | Wert |
|-------------|------|
| Sheet | `Masterliste` |
| Header-Zeile | 3 (Spaltentitel) |
| Daten ab | Zeile 16 |
| Anzahl Verträge | 83 |
| Kontext | Brücken-/Kreuzungsbauwerk-Verträge SBB |

**Relevante Spalten:**

| Code | Spalte | Beschreibung |
|------|--------|--------------|
| A1 | Vertragsnummer | 8-stellig, beginnt mit 9 |
| — | Domino-Nr | Format `0600-YYYY-NNNN` |
| — | Alte Vertragsnummer | Legacy-Nummer |
| A2 | PDF Anlagen | Anlage/Bauwerk-Beschreibung |
| — | UUID (RIS Viewer) | Ingenieurbauten-Identifikator |
| A3 | Bahnlinie | 3-stellige Liniennummer |
| A4 | Kilometrierung von/bis | Streckenkilometer |
| A5 | Vertragspartner | Externer Partner (ohne SBB) |
| A6 | Vertragsart | z.B. "Kreuzungsbauwerk" |
| A7 | Dateiname | PDF-Dateiname |
| A8 | Vertragsbeginn | Jahr oder Datum |
| A9 | Vertragsende | Jahr oder Datum |
| A10 | Entschädigung | Periodische Ein-/Ausgaben |
| A13 | Gemeinde | Standortgemeinde |

### JSON-Extraktionsdateien

| Datei | Schema | Vertragsnr | Objekt |
|-------|--------|------------|--------|
| `extraction_results_balsberg.json` | alt (`felder.km_bereich`) | 90051045 | UEF Balsberg |
| `extraction_results_90004012.json` | neu (`felder.km_von`) | 90004012 | PI du Trabandan |

---

## Geprüfte Felder

| Feld | Vergleichslogik |
|------|-----------------|
| Vertragsnummer | Exakter String-Match |
| Domino-Nr | Exakter Match bzw. Substring-Suche in `alt_systemnummern` |
| Alte Vertragsnummer | Substring-Match in Liste |
| UUID | Regex-Extraktion aus mehrzeiligem Master-Feld |
| km_von | Numerisch, Toleranz ±0.01 |
| Vertragspartner | Teilmatch (Substring oder Wortüberlappung ≥2 Wörter) |
| Vertragsart | Substring-Vergleich (Extraktion spezifischer als Master) |
| Gemeinde | Normalisierter Textvergleich (case-insensitive) |
| Vertragsbeginn | Jahresvergleich (4-stellige Zahl) |
| Vertragsende | Jahresvergleich (4-stellige Zahl) |

---

## Bewertungslogik

| Symbol | Status | Bedeutung | Score-Gewicht |
|--------|--------|-----------|---------------|
| ✓ | MATCH | Exakte Übereinstimmung | 1.0 |
| ≈ | MATCH (≈) | Numerisch innerhalb Toleranz | 1.0 |
| ~ | TEILMATCH | Substring oder Wortüberlappung ≥50% | 0.5 |
| ~ | ÄHNLICH | Semantische Ähnlichkeit | 0.5 |
| ✗ | ABWEICHUNG | Keine Übereinstimmung | 0.0 |
| M | NUR_MASTER | Nur in Masterdatei vorhanden | nicht gewertet |
| E | NUR_EXTRAKTION | Nur in Extraktion vorhanden | nicht gewertet |
| - | BEIDE_LEER | Keine Seite hat einen Wert | nicht gewertet |

**Gesamtscore:**

```
Score = (Matches + 0.5 × Teilmatches) / (Matches + Teilmatches + Abweichungen) × 100%
```

---

## Ergebnisse (Stand 2026-06-23)

### Vertrag 90051045 (UEF Balsberg) — Score: 57%

| Feld | Status | Detail |
|------|--------|--------|
| Vertragsnummer | ✓ MATCH | 90051045 |
| Domino-Nr | E NUR_EXTRAKTION | Extraktion: 0600-2003-0730, Master: leer |
| UUID | ✓ MATCH | b571f8ac-0a95-11e8-8b02-fb3b4701752b |
| km_von | ✓ MATCH | 8.68 |
| Vertragspartner | ✗ ABWEICHUNG | Extraktion listet SBB + ASTRA, Master nur ASTRA |
| Gemeinde | ✓ MATCH | Kloten |
| Vertragsbeginn | ✗ ABWEICHUNG | Extraktion: 2026, Master: 2023 |
| Vertragsende | ✗ ABWEICHUNG | Extraktion: 2126, Master: 2123 |

### Vertrag 90004012 (PI Trabandan, Lausanne) — Score: 86%

| Feld | Status | Detail |
|------|--------|--------|
| Vertragsnummer | ✓ MATCH | 90004012 |
| Alte Vertragsnr | ✓ MATCH | 18633 |
| Domino-Nr | M NUR_MASTER | Master: 0600-1956-0004 |
| km_von | ≈ MATCH (≈) | 1.31 ≈ 1.313 (Δ=0.003) |
| Vertragspartner | ✓ MATCH | Commune de Lausanne |
| Vertragsart | ~ TEILMATCH | "Kreuzungsbauwerk (Brücke)" ⊂ "Kreuzungsbauwerk" |
| Gemeinde | ~ TEILMATCH | "Lausanne" ⊂ "1000 LAUSANNE (VD)" |
| Vertragsbeginn | ✓ MATCH | 1956 |
| Vertragsende | - BEIDE_LEER | — |

### Gesamtergebnis

| Metrik | Wert |
|--------|------|
| Verträge geprüft | 2 |
| Felder total | 17 |
| Match | 9 |
| Teilmatch | 2 |
| Abweichung | 3 |
| Leer/Einseitig | 3 |
| **Gesamtscore** | **71%** |

---

## Erkannte Probleme

### 1. Datums-Abweichung Balsberg (kritisch)
Die Extraktion nennt 2026/2126 statt 2023/2123 — eine Verschiebung um exakt 3 Jahre. Mögliche Ursache: Das LLM interpretiert ein "Inkrafttreten" oder Nachtrag-Datum statt dem Original-Vertragsdatum.

### 2. Vertragspartner-Asymmetrie (systematisch)
Die Masterdatei listet nur den **externen** Vertragspartner (ohne SBB), während die Extraktion alle Parteien aufführt. Für den Vergleich muss SBB herausgefiltert werden.

### 3. Fehlende Domino-Nr (beidseitig)
- Balsberg: Extraktion findet 0600-2003-0730, Master hat keinen Eintrag
- Lausanne: Master hat 0600-1956-0004, Extraktion findet sie nicht im Text

---

## Bekannte Einschränkungen

- **Datumsvergleich:** Nur auf Jahresebene — exakte Tages-/Monats-Abweichungen werden nicht erkannt
- **Vertragspartner:** Kein semantischer Vergleich (z.B. "ASTRA" ≠ "Bundesamt für Strassen")
- **Schema-Varianten:** Zwei JSON-Schemata erfordern separate Validierungsfunktionen
- **Master-Datenqualität:** Obere Zeilen (1–15) enthalten Metadaten/Anweisungen, keine Vertragsdaten
- **Nur "PDF"-Spalten als Referenz:** Falls `PDF_*`-Spalten gefüllt sind, werden diese bevorzugt

---

## Usage

```bash
python validate_against_masterdatei.py
```

**Voraussetzungen:**
- Python 3.8+
- `openpyxl` (pip install openpyxl)
- Dateien im gleichen Verzeichnis:
  - `Masterdatei H4R (3).xlsx`
  - `extraction_results_balsberg.json`
  - `extraction_results_90004012.json`

**Ausgabe:**
- Konsolenbericht mit Validierungstabelle
- `validation_results_masterdatei.json` (maschinenlesbare Ergebnisse)

---

## Abgleich mit SBB-Brückeninventar (brucken.csv)

Zusätzlich zur Masterdatei-Validierung wurde geprüft, ob die extrahierten Anlagen im
offiziellen SBB-Brückeninventar (Open Data: `data.sbb.ch`, Dataset `brucken`) auffindbar sind.

**Datenquelle:** `brucken.csv` (4'057 Brücken)

| Spalte | Beschreibung |
|--------|--------------|
| Linie | Bahnnummer (3-stellig) |
| KM | Streckenkilometer |
| Name | Brückenname |
| Anzahl Baueinheit | Anzahl Baueinheiten |
| Kanton | Standortkanton |
| UUID | Inventar-Identifikator |
| Geoposition | Lat, Lon |

### Suchstrategien

1. **UUID-Match:** Exakte Suche nach der in der Extraktion genannten UUID
2. **Linie + km:** Suche auf der Bahnlinie mit km-Toleranz ±0.5
3. **Textsuche:** Namensabgleich (Substring)

---

### Ergebnis: Vertrag 90051045 (UEF Balsberg)

| Strategie | Ergebnis |
|-----------|----------|
| UUID `b571f8ac-0a95-11e8-8b02-fb3b4701752b` | **Nicht gefunden** — UUID existiert nicht im Inventar |
| Linie 752, km 8.68 ±0.5 | 3 Kandidaten |

**Kandidaten auf Linie 752:**

| km | Name | UUID | Δ km |
|----|------|------|------|
| 8.213 | U Riethofstrasse | bfc8e95c-... | -0.467 |
| 8.563 | SU Platten | fe8f4e0c-... | -0.117 |
| **8.886** | **PU Balsberg** | **b4185b58-0a95-11e8-8b02-fb3b4701752b** | **+0.206** |

**Bewertung:**
- Bester Treffer: **"PU Balsberg"** (Namensübereinstimmung "Balsberg")
- UUID-Diskrepanz: Inventar hat `b4185b58-...`, Extraktion nennt `b571f8ac-...`
- km-Abweichung: 8.886 vs 8.68 (Δ = 0.206 km)
- Mögliche Ursache: Die extrahierte UUID stammt aus dem RIS Viewer (Ingenieurbauten-System), das einen anderen Identifikator verwendet als das Open-Data-Inventar. Das Objekt "Überführung UEF" (Strassenbrücke über Bahn) kann im Brückeninventar als "PU" (Passage unter) geführt werden.

---

### Ergebnis: Vertrag 90004012 (PI du Trabandan, Lausanne)

| Strategie | Ergebnis |
|-----------|----------|
| Linie 250, km 1.31 ±0.5 | **Exakter Treffer** |
| Textsuche "Trabandan" | **1 Treffer** |

**Gefundener Eintrag:**

| Feld | Wert |
|------|------|
| Linie | 250 |
| KM | 1.311 |
| Name | **PI du Trabandan** |
| UUID | **6432b8e4-0a95-11e8-8b02-fb3b4701752b** |
| Kanton | Vaud |
| Geoposition | 46.514°N, 6.644°E |

**Bewertung:**
- Name: Exakter Match ("PI du Trabandan" = "Passage inférieur du Trabandan")
- km: Exakter Match (1.311 vs. extrahiert 1.31, Δ = 0.001)
- UUID `6432b8e4-...` war bisher **nicht in der Extraktion enthalten** und kann ergänzt werden

---

### Zusammenfassung Inventar-Abgleich

| Vertrag | Anlage gefunden? | Match-Qualität | UUID-Status |
|---------|-----------------|----------------|-------------|
| 90051045 (Balsberg) | Ja (per Name) | Mittel (km Δ=0.2, UUID ≠) | Diskrepanz: RIS-UUID ≠ Inventar-UUID |
| 90004012 (Trabandan) | Ja (exakt) | Hoch (Name + km exakt) | Neu: UUID aus Inventar ergänzbar |

### Offene Fragen

1. **UUID-Systeme:** Warum unterscheidet sich die RIS-Viewer-UUID von der Inventar-UUID bei Balsberg?
   - Hypothese: RIS Viewer identifiziert die "Überführung" (Gesamtobjekt), das Brückeninventar die einzelne "Passage" (Bauteil)
2. **km-Differenz Balsberg:** 8.68 (Vertrag) vs 8.886 (Inventar) — evtl. Bezugspunkt Mitte vs. Anfang des Bauwerks
3. **Fehlende UUID Trabandan:** Die Extraktion aus dem Vertrag 90004012 enthält keine UUID — diese kann nun aus dem Inventar (`6432b8e4-...`) nachgetragen werden
