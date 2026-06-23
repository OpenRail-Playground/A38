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
- **Bewertung:** `fehlend` ist korrekt – markitdown kann Handschrift/Bilder nicht lesen
- **Fazit:** Erwartetes Verhalten, kein Fehler der Pipeline. Für diese Felder braucht es OCR mit Handschrift-Erkennung oder Human-in-the-Loop.

### Kosten (Felder 10/11) – ❌ FALSCH EXTRAHIERT

**Ist (Extraktion):**
- Einnahmen SBB: CHF 7.8 Mio. (ASTRA-Anteil, einmalig)
- Ausgaben SBB: CHF 8.0 Mio. (SBB-Eigenanteil, einmalig) + Betrieb qualitativ

**Soll (aus Vertrag):**
- **Investitionskosten (einmalig):** SBB CHF 8.0 Mio. / ASTRA CHF 7.8 Mio. – Kostenteilung, ASTRA zahlt an SBB ✓ soweit korrekt
- **Betriebskosten (periodisch, %):** SBB 45% / ASTRA 55% – **NICHT EXTRAHIERT**

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

## Nächste Schritte

1. [ ] Test mit **vollständigem Text** (alle 2727 Zeilen) wiederholen
2. [ ] Zweiten Vertrag testen (anderer Typ, z.B. Grundstücknutzung oder FinVer)
3. [ ] Gegen Masterdatei abgleichen
4. [ ] Französisches/Italienisches PDF testen

---

*Erstellt: 23.06.2026, 11:01*
