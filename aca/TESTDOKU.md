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

## Beobachtungen

### Was gut funktioniert hat
1. **markitdown** extrahiert den Vertragstext (S. 1-14) sauber
2. **Vertragstyp-Ableitung** korrekt: Titel + Ziff. 3 → V3&4 (Ausführung + Betrieb)
3. **Kostenteiler** korrekt strukturiert (Veranlasserprinzip erkannt)
4. **Quellenangaben** konsistent und nachvollziehbar
5. **Sonderfälle** korrekt behandelt: Punktobjekt, bedingte Zahlung, Querverweis

### Probleme / Learnings

| Problem | Ursache | Lösung |
|---------|---------|--------|
| OCR endet bei S. 6 (Text) | markitdown hat den Bauwerksplan (letzte Seite) als "Inhalt" interpretiert, aber die Seiten 7-14 des Textes korrekt extrahiert – **Ich hatte fälschlich nur 380 Zeilen übergeben!** | Nächster Test: vollständigen Text übergeben |
| Vertragsbeginn fehlt | Unterschriften stehen auf S. 13 (Zürich/Bern/Winterthur) – waren im Input enthalten aber ohne Datum | Im PDF sind die Daten vermutlich handschriftlich → markitdown kann sie nicht lesen |
| Bauwerksplan erzeugt ~2300 Zeilen OCR-Müll | Technische Zeichnung wird als Text extrahiert | Pre-Processing: Plan-Seiten filtern oder markitdown mit Seitenlimit |

### Verbesserungspotenzial
1. **Volltext übergeben** – alle 2727 Zeilen, nicht nur die ersten 380
2. **Plan-Seiten filtern** – Seiten mit >90% Zahlen/Koordinaten als "Beilage" markieren
3. **Gegen Masterdatei validieren** – Vertrag 90051045 in der Masterdatei suchen und Felder vergleichen

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
