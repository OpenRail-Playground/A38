# ACA Testdokumentation – Erste Verprobing

## Testdatum
2026-06-23, 11:00 Uhr

## Testgegenstand
Vertrag Nr. **90051045** – Vereinbarung SBB/ASTRA betreffend Bau und Bauwerkserhaltung «U N20 (A51)» / Überführung UEF SBB Balsberg, Opfikon-Kloten.

## Pipeline

```
PDF (14 Seiten + Situationsplan)
  │
  ▼  markitdown (~/Library/Python/3.14/bin/markitdown)
  │
Text (2727 Zeilen, davon ~380 Vertragstext, Rest = OCR aus Bauwerksplan)
  │
  ▼  Subagent (Claude Sonnet 4) + System-Prompt v1.0
  │
JSON (results/90051045.json)
```

## Ergebnisse

### Feld-Extraktion (13 Felder)

| Feld | Qualität | Extrahierter Wert | Korrekt? |
|------|----------|-------------------|----------|
| 1. Vertragsnummer | ✅ eindeutig | 90051045 | ✓ |
| 2. Vertragstyp | ⚠️ abgeleitet | Zusammenarbeit › Ausf.+Betrieb (V3&4) › Brücke | ✓ plausibel |
| 3. Anlage | ✅ eindeutig | Bahnbrücke «U N20 (A51)» ... | ✓ |
| 4. Bahnlinie | ✅ eindeutig | Linie 752 (Opfikon - Kloten Balsberg) | ✓ |
| 5. km von | ✅ eindeutig | 8.68 | ✓ |
| 6. km bis | ✅ eindeutig | 8.68 (Punktobjekt) | ✓ |
| 7. Vertragspartner | ✅ eindeutig | ASTRA (Bund/ASTRA) | ✓ |
| 8. Vertragsbeginn | ❌ fehlend | null | Korrekt: Unterschriften waren nicht im OCR |
| 9. Vertragsende | ⚠️ abgeleitet | 100 Jahre ab Bau | ✓ (aus Ziff. 4) |
| 10. Period. Einnahmen | ✅ eindeutig | CHF 7.8 Mio. (ASTRA-Anteil) | ✓ |
| 11. Period. Ausgaben | ⚠️ abgeleitet | CHF 8.0 Mio. (SBB-Eigenanteil) + Betrieb qualitativ | ✓ |
| 12. Gemeinde | ✅/⚠️ | Kloten (eindeutig), Opfikon (abgeleitet) | ✓ |
| 13. Quellenangaben | ✅ | Konsistent mit Einzelfeldern | ✓ |

### Kostenteiler

| Position | Gesamtkosten | SBB | ASTRA | Korrekt? |
|----------|-------------|-----|-------|----------|
| Neubau Brücke | CHF 15.8 Mio. (±10%) | CHF 8.0 Mio. (intern) | CHF 7.8 Mio. (an SBB) | ✓ |

### Qualitätskennzeichen

- **Eindeutig:** 6 Felder
- **Abgeleitet:** 4 Felder
- **Fehlend:** 1 Feld (Vertragsbeginn)
- **Manuelle Prüfung empfohlen:** Ja (fehlende Seiten 7-14 im OCR)

### Vertragsbeziehungen

- Querverweis auf separate Finanzierungsvereinbarung Glattalautobahn erkannt ✓
- Korrekt als `im_bestand: false` markiert ✓

## Manuelle Verifikation (Team, 23.06.2026 11:30)

### Vertragsbeginn (Feld 8)
- **Extraktion:** `fehlend`
- **Realität:** Datum steht bei den Unterschriften (letzte Unterschrift zählt), ist aber **handschriftlich/Bild** im PDF
- **Vertragsreferenz:** Ziff. 29, S. 12: *„Diese Vereinbarung [...] tritt mit der Unterzeichnung durch alle Parteien in Kraft."* – Unterschriftsseite S. 13 (Zürich, Bern, Winterthur) – Daten handschriftlich eingetragen, nicht im OCR lesbar.
- **Masterdatei:** 2023-06-14 (manuell in Spalte "PDF Vertragsbeginn" erfasst)
- **Bewertung:** `fehlend` ist korrekt – markitdown kann Handschrift/Bilder nicht lesen
- **Fazit:** Erwartetes Verhalten, kein Fehler der Pipeline. Für diese Felder braucht es OCR mit Handschrift-Erkennung oder Human-in-the-Loop.

### Kosten (Felder 10/11) – ❌ FALSCH EXTRAHIERT

**Ist (Extraktion):**
- Einnahmen SBB: CHF 7.8 Mio. (ASTRA-Anteil, einmalig)
- Ausgaben SBB: CHF 8.0 Mio. (SBB-Eigenanteil, einmalig) + Betrieb qualitativ

**Soll (aus Vertrag):**
- **Investitionskosten (einmalig):** SBB CHF 8.0 Mio. / ASTRA CHF 7.8 Mio. – Kostenteilung, ASTRA zahlt an SBB ✓ soweit korrekt
  - Vertragsreferenz: Ziff. 15, S. 6: *„Die gesamten Investitionskosten [...] werden auf CHF 15.8 Mio. geschätzt (Genauigkeitsgrad von +/-10% [...] Preisbasis März, 2022)"* und *„leistet das ASTRA eine Vorteilsanrechnung [...] von einem Globalbetrag CHF 7.8 Mio."*
- **Betriebskosten (periodisch, %):** SBB 45% / ASTRA 55% – **NICHT EXTRAHIERT**
  - Vertragsreferenz: Ziff. 17, S. 7: *„Arbeiten zur Instandsetzung oder Erneuerung des Bauwerks"* → Tabelle: *„Anteil der SBB AG: 45% / Anteil des ASTRA: 55%"* und *„Der Kosteinteiler basiert auf den Flächen der Brücke: [...] TOTAL (540m²) [...] SBB 245m² / ASTRA 295m²"*

**Fehleranalyse:**
1. Die Betriebskosten-Prozente (45% SBB / 55% ASTRA) stehen in Ziff. 17 (Seiten 7-8) – diese waren im verkürzten Input (nur 380 Zeilen) nicht enthalten
2. Selbst mit vollständigem Text: Die %-Aufteilung müsste als periodische Ausgabe/Einnahme mit `art: "kostenteiler_anteil"` und `frequenz: "periodisch"` erfasst werden
3. Der Kostenteiler-Abschnitt im JSON enthält nur die Investitionskosten, nicht die Betriebskosten

**Korrekte Extraktion müsste sein:**
```json
"periodische_einnahmen": [
  { "betrag": 7800000, "art": "kostenteiler_anteil", "frequenz": "einmalig", "hinweis": "Invest ASTRA-Anteil" },
  { "betrag": null, "art": "kostenteiler_anteil", "frequenz": "periodisch", "hinweis": "55% der Betriebskosten durch ASTRA" }
],
"kostenteiler": [
  { "bezeichnung": "Investitionskosten Neubau", "gesamtkosten": 15800000, "anteile": [SBB 8M, ASTRA 7.8M] },
  { "bezeichnung": "Betriebskosten/Erhaltung", "gesamtkosten": null, "anteile": [SBB 45%, ASTRA 55%] }
]
```

### Zusammenfassung Verifikation

| Feld | Extraktion | Verifikation |
|------|-----------|--------------|
| Vertragsbeginn | ❌ fehlend | ✓ korrekt – Handschrift nicht lesbar |
| Investitionskosten | ✓ korrekt | CHF 8M SBB / 7.8M ASTRA |
| Betriebskosten | ❌ nicht extrahiert | 45% SBB / 55% ASTRA – im abgeschnittenen Input nicht vorhanden |

**Root Cause:** Dem Subagent wurden nur 380 von 2727 Zeilen übergeben (Seiten 1-6 statt 1-14). Die Betriebskosten-Regelung steht auf Seite 7-8 (Ziff. 17).

## Beobachtungen

### Was gut funktioniert hat
1. **markitdown** extrahiert den Vertragstext (S. 1-14) sauber
2. **Vertragstyp-Ableitung** korrekt: Titel + Ziff. 3 → V3&4 (Ausführung + Betrieb)
3. **Investitions-Kostenteiler** korrekt (Beträge, Richtung, Veranlasserprinzip)
4. **Quellenangaben** konsistent und nachvollziehbar
5. **Sonderfälle** korrekt behandelt: Punktobjekt, bedingte Zahlung, Querverweis

### Probleme / Learnings

| Problem | Ursache | Lösung |
|---------|---------|--------|
| Betriebskosten fehlen | Nur 380 von 2727 Zeilen übergeben (S. 1-6 statt 1-14) | **Immer vollständigen Text übergeben** |
| Vertragsbeginn fehlt | Handschriftliches Datum im Bild → markitdown kann es nicht lesen | Human-in-the-Loop oder OCR mit Handschrift-Erkennung |
| Bauwerksplan erzeugt ~2300 Zeilen OCR-Müll | Technische Zeichnung wird als Text extrahiert | Pre-Processing: Plan-Seiten filtern |

### Verbesserungspotenzial
1. **Volltext übergeben** – alle Zeilen bis zum Bauwerksplan (≈ Seite 14), Plan-Anhang abschneiden
2. **Plan-Seiten filtern** – Seiten mit >90% Zahlen/Koordinaten als "Beilage" markieren
3. **Zweiter Lauf mit vollem Text** – Betriebskosten-Extraktion verifizieren

## Taxonomie-Validierung

Extrahierter Pfad: `Zusammenarbeit bei Anlagen › Ausführung Projekt mit Betrieb und Unterhalt (Vertrag 3&4) › Kreuzungsbauwerk (Brücke)`

Prüfung gegen `taxonomy.yaml`:
- ✅ Ebene 2: `zusammenarbeit` – gültig
- ✅ Ebene 3: `ausfuehrung_betrieb` (Vertrag 3&4) – gültig
- ✅ Ebene 4: `kbw_bruecke` – im Pool `zusammenarbeit` vorhanden und bei V3&4 erlaubt

**Ergebnis: Taxonomie-valide ✓**

---

## Iteration 2: Vollständiger Text (23.06.2026, 11:34)

### Änderungen gegenüber Iteration 1
- **Input:** Vollständiger markitdown-Output bis S.14 (880 Zeilen, Bauwerksplan abgeschnitten)
- **Pre-Processing:** `grep -n "Seite 14/14"` → Zeile 874 → `head -880` als Cutoff
- **Erwartung:** Betriebskosten 45% SBB / 55% ASTRA müssen extrahiert werden (Ziff. 17)
- **Erwartung:** Vertragsbeginn bleibt `fehlend` (Handschrift)
- **Erwartung:** Vertragsende = 100 Jahre feste Laufzeit (Ziff. 30)
- **Erwartung:** Vorgängervertrag 90005733 erkannt (Ziff. 32)

### Ergebnis: `results/90051045_v2.json`

| Feld | Qualität | Extrahierter Wert | Korrekt? | Diff zu v1 |
|------|----------|-------------------|----------|------------|
| 1. Vertragsnummer | ✅ eindeutig | 90051045 | ✓ | = |
| 2. Vertragstyp | ⚠️ abgeleitet | Zusammenarbeit › V3&4 › Brücke | ✓ | = |
| 3. Anlage | ✅ eindeutig | Bahnbrücke «U N20 (A51)» ... | ✓ | = |
| 4. Bahnlinie | ✅ eindeutig | Linie 752 | ✓ | = |
| 5. km von | ✅ eindeutig | 8.68 | ✓ | = |
| 6. km bis | ✅ eindeutig | 8.68 | ✓ | = |
| 7. Vertragspartner | ✅ eindeutig | ASTRA | ✓ | = |
| 8. Vertragsbeginn | ❌ fehlend | null (handschriftlich) | ✓ erwartet | = |
| 9. Vertragsende | ✅ eindeutig | 100 Jahre feste Laufzeit | ✓ **NEU** | ⬆️ war `abgeleitet` |
| 10. Period. Einnahmen | ✅ eindeutig | CHF 7.8M (Invest) + 55% (Betrieb) | ✓ **NEU** | ⬆️ Betrieb hinzu |
| 11. Period. Ausgaben | ✅/⚠️ | CHF 8M (Invest) + 45% (Betrieb) + Inspektion | ✓ **NEU** | ⬆️ Betrieb hinzu |
| 12. Gemeinde | ✅/⚠️ | Kloten + Opfikon | ✓ | = |
| 13. Quellenangaben | ✅ | Konsistent | ✓ | ⬆️ erweitert |

### Neue Erkenntnisse (Iteration 2)

| Was | Iteration 1 | Iteration 2 | Korrekt? |
|-----|-------------|-------------|----------|
| Betriebskosten-Teiler | ❌ nicht extrahiert | ✅ 45% SBB / 55% ASTRA | ✓ |
| Vertragsende | ⚠️ "100 Jahre (aus Nutzungsdauer)" | ✅ "100 Jahre feste Laufzeit (Ziff. 30)" | ✓ |
| Vorgängervertrag | nicht erkannt | ✅ 90005733 / 0600-2003-0730 (aufgehoben) | ✓ |
| Flächen-Herleitung | nicht vorhanden | ✅ 245m² SBB / 295m² ASTRA = 540m² Total | ✓ |
| Inspektion alle 5 Jahre | nicht erkannt | ✅ als qualitative Ausgabe erfasst | ✓ |
| Kostenteiler-Struktur | 1 Eintrag (nur Invest) | ✅ 2 Einträge (Invest + Betrieb) | ✓ |

### Qualitätskennzeichen (Vergleich)

| Metrik | Iteration 1 | Iteration 2 |
|--------|------------|-------------|
| Eindeutig | 6 | 8 |
| Abgeleitet | 4 | 3 |
| Fehlend | 1 | 1 |
| Manuelle Prüfung | Ja | Ja (Handschrift) |

### Fazit Iteration 2

**Root Cause bestätigt:** Das Fehlen der Betriebskosten in Iteration 1 lag ausschließlich am abgeschnittenen Input (380 statt 880 Zeilen). Mit vollständigem Vertragstext werden alle Kostenregelungen korrekt extrahiert.

**Verbleibende Limitierung:** Handschriftliche Unterschriftsdaten (Vertragsbeginn) sind für die rein textbasierte Pipeline nicht extrahierbar. Hierfür braucht es entweder:
- Vision-basierte OCR (Handschrifterkennung)
- Human-in-the-Loop (manuelles Nachtragen)
- Abgleich mit SAP-System (falls dort bereits erfasst)

### Learnings für die Pipeline

1. **Pre-Processing:** Bauwerksplan-Anhänge abschneiden (Erkennung via "Seite N/N" + nachfolgende Zeichnungsdaten)
2. **Volltext:** Immer den kompletten Vertragstext übergeben (bis letzte nummerierte Seite)
3. **Iteratives Feedback:** Verifikation nach Iteration 1 verbessert Iteration 2 signifikant
4. **Taxonomie-Validierung:** Pfad weiterhin gültig (V3&4 + Brücke aus Pool A)

## Nächste Schritte

- [ ] Zweiten Vertrag testen (anderer Typ, z.B. Grundstücknutzung oder FinVer)
- [ ] Gegen Masterdatei abgleichen (Vertrag 90051045)
- [ ] Französisches/Italienisches PDF testen
- [ ] Pre-Processing-Logik (Plan-Seiten abschneiden) automatisieren

---

## Abgleich mit Masterdatei (23.06.2026, 13:00)

### Masterdatei-Struktur

Sheet **"Masterliste"** – 33 Spalten, relevante Header (Zeile 3):

| # | Spalte | Mapping auf JSON-Feld |
|---|--------|----------------------|
| 1 | Titel | – (Kategorie, z.B. "Kreuzungsbauwerk") |
| 2 | Vertragsnummer | `felder.vertragsnummer.primaer` |
| 6 | Alte Vertragsnummer | `felder.vertragsnummer.alt_systemnummern` |
| 8 | PDF Anlagen | `felder.anlage.wert` |
| 9 | UUID (RIS Viewer) | – (externe Referenz) |
| 10 | Bahnlinien | `felder.bahnlinie[].wert` |
| 12 | Kilometrierung von | `felder.km_von.wert` |
| 14 | Kilometrierung bis | `felder.km_bis.wert` |
| 16 | Vertragspartner | `felder.vertragspartner[].name` |
| 18 | Vertragsart | – (SAP-Klassifikation) |
| 19 | Vertragstyp Ebene 2 | `felder.vertragstyp.ebene_2` |
| 20 | Vertragstyp Ebene 3 | `felder.vertragstyp.ebene_3` |
| 21 | Vertragstyp Ebene 4 | `felder.vertragstyp.ebene_4` |
| 22 | Herleitung Vertragstypen | – (Freitext-Begründung) |
| 24 | Vertragsbeginn | `felder.vertragsbeginn.wert` |
| 26 | Vertragsende | `felder.vertragsende.wert` |
| 28 | Periodische Ein/Ausgaben | `felder.periodische_einnahmen` / `periodische_ausgaben` |
| 31 | Gemeinde | `felder.gemeinde[].gemeinde` |

Hinweis: Viele Spalten sind VLOOKUP-Formeln auf andere Sheets (SAP-Export, Migrationstabelle). Die "PDF"-Spalten enthalten die manuell aus dem PDF gelesenen Werte.

### Vertrag 90051045: Feld-für-Feld-Vergleich

| Feld | Masterdatei | Extraktion v2 | Match |
|------|-------------|---------------|-------|
| Vertragsnummer | 90051045 | 90051045 | ✅ |
| Anlage | "Bau und Bauwerkserhaltung «U N20 (A51)» / Überführung UEF SBB Balsberg, Opfikon-Kloten" | "Bahnbrücke «U N20 (A51)» / Überführung UEF SBB Balsberg..." | ✅ |
| km von (PDF) | 8.68 | 8.68 | ✅ |
| Vertragstyp Ebene 2 | Zusammenarbeit bei Anlagen | Zusammenarbeit bei Anlagen | ✅ |
| Vertragstyp Ebene 3 | Ausführung Projekt mit Betrieb und Unterhalt (V3&4) | Ausführung Projekt mit Betrieb und Unterhalt | ✅ |
| **Vertragstyp Ebene 4** | **Kreuzungsbauwerk (Bahnübergang)** | **Kreuzungsbauwerk (Brücke)** | ❌ |
| Vertragsbeginn (PDF) | **2023-06-14** | fehlend (handschriftlich) | ⚠️ |
| Vertragsende (PDF) | **2123-06-13** | "100 Jahre feste Laufzeit" | ✅ (2023+100=2123) |
| Period. Ein/Ausgaben | **nein** | ja (CHF 7.8M + 45%/55%) | ❓ |
| Gemeinde (PDF) | Kloten | Kloten + Opfikon | ✅ |

### Auffälligkeiten

#### 1. Ebene 4: "Bahnübergang" vs. "Brücke" ❌

- **Masterdatei:** Kreuzungsbauwerk (Bahnübergang)
- **Extraktion:** Kreuzungsbauwerk (Brücke)
- **Im Vertrag steht wörtlich:**
  - Ziff. 4, S. 3: *„Art des Bauwerks: Bahnbrücke"*
  - Ziff. 4, S. 3: *„Die Bahnbrücke überquert die Nationalstrasse A51"*
  - S. 1, Titel: *„den Bau und die Bauwerkserhaltung «U N20 (A51)» (SBB) / Überführung UEF SBB Balsberg"*
  - Ziff. 1, S. 2: *„Das Bauwerk wurde im Jahr 1949 [...] unter der bestehenden einspurigen Bahnstrecke gebaut."* (= Bahn überquert Strasse = Brücke, nicht Bahnübergang)

**Bewertung:** Die Extraktion ist korrekt – es handelt sich eindeutig um eine Brücke (Bahn überquert Strasse von oben). Ein "Bahnübergang" wäre eine niveaugleiche Kreuzung mit Schrankenanlage. Die Masterdatei enthält hier einen Klassifikationsfehler.

→ **Die KI-Extraktion hat einen Fehler in den Stammdaten gefunden.**

#### 2. Periodische Ein/Ausgaben: "nein" vs. Kostenteiler ❓

- **Masterdatei:** "nein"
- **Extraktion:** Investitionskosten (einmalig) + Betriebskosten (45%/55% periodisch)
- **Im Vertrag steht:**
  - Ziff. 15, S. 6: Investitionskosten CHF 15.8 Mio. (einmalig) – Globalbetrag ASTRA CHF 7.8 Mio.
  - Ziff. 17, S. 7: *„Die Investitionsfolgekosten für diese Massnahmen werden nach dem folgenden Verteilschlüssel getragen: SBB AG 45% / ASTRA 55%"* (periodisch, bei Bedarf)
  - Ziff. 17, S. 7: *„Das Bauwerk ist [...] periodisch (alle 5 Jahre) zu inspizieren"*
  - Ziff. 17, S. 8: *„Das ASTRA zahlt den Betrag [...] im Zusammenhang mit dem Bauwerkserhalt, gegen Vorlage einer Rechnung."*

**Bewertung:** Vermutlich definiert die Masterdatei "periodisch" als fixen CHF-Betrag pro Jahr. Ein %-basierter Kostenteiler ohne fixen Betrag wird offenbar nicht als "periodische Ein/Ausgabe" gewertet. Das ist eine Definitionsfrage, kein Extraktionsfehler.

→ **Unterschiedliche Definition von "periodisch" in Masterdatei vs. System-Prompt.**

#### 3. Vertragsbeginn: 2023-06-14 vs. fehlend ⚠️

- **Masterdatei:** 2023-06-14 (manuell erfasst in "PDF Vertragsbeginn")
- **Extraktion:** fehlend (Unterschrift handschriftlich, nicht im OCR)
- **Im Vertrag steht:**
  - Ziff. 29, S. 12: *„Sie tritt mit der Unterzeichnung durch alle Parteien in Kraft."*
  - S. 13: Unterschriftsfelder für Zürich (SBB), Bern (SBB), Winterthur (ASTRA/Otto Noger) – Daten sind handschriftlich eingetragen
  - Dokumenten-Code S. 1: *„20230702 l-NAT-PAG-PSV-VEM"* (Hinweis auf Juli 2023, aber kein verbindliches Vertragsdatum)

**Bewertung:** Korrekt als `fehlend` markiert. Das Datum 2023-06-14 wurde von einem Menschen aus dem handschriftlichen Eintrag gelesen. Für markitdown nicht lesbar.

→ **Bekannte Limitation, kein Fehler.**

### Zusammenfassung Masterdatei-Abgleich

| Kategorie | Anzahl |
|-----------|--------|
| ✅ Übereinstimmung | 7 Felder |
| ❌ Abweichung (Extraktion besser) | 1 (Ebene 4: Brücke statt Bahnübergang) |
| ⚠️ Nicht extrahierbar (Handschrift) | 1 (Vertragsbeginn) |
| ❓ Definitionsunterschied | 1 (Period. Ein/Ausgaben) |

**Fazit:** Die Pipeline erreicht bei diesem Vertrag eine höhere Datenqualität als die manuelle Erfassung in der Masterdatei (Ebene 4 korrekter klassifiziert).

---

*Erstellt: 23.06.2026, 11:01 | Iteration 2: 11:34 | Masterdatei-Abgleich: 13:00*
