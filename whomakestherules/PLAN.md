# Who Makes the Rules – Arbeitsplan

## Ziel

Aus dem BS-KI-Regelwerk (PDF + Matrix-Excel) deterministische, maschinenlesbare Rules-Dateien erzeugen.

Jede Regel wird **wörtlich zitiert** aus dem PDF. Die Matrix liefert die Struktur (was ist verbindlich/empfohlen für welches Transportmittel/Kanal).

## Datenquellen

| Datei | Inhalt | Rolle |
|-------|--------|-------|
| `Matrix_BS-KI_DE.xlsx` (Sheet "Bewertungsmatrix") | Regeln × Kanäle × Transportmittel → v/e/– | **Struktur & Ground Truth** |
| `BS-KI_DE.pdf` (64 Seiten) | Detaillierte Regeltexte, Definitionen, Beispiele | **Inhalt (wörtlich zitieren)** |

## Output-Struktur (Vorschlag)

```
whomakestherules/
└── rules/
    ├── 01-allgemeine-informationen/
    │   ├── aktuelle-uhrzeit.yaml
    │   ├── name-haltestelle.yaml
    │   ├── beschriftung-haltekante.yaml
    │   ├── wegweisung.yaml
    │   ├── ereignisinformationen.yaml
    │   ├── linien-tarifzonen.yaml
    │   ├── billettbezug.yaml
    │   ├── kontakt-tu.yaml
    │   └── passagierrechte.yaml
    ├── 02-fahrtbezogene-informationen/
    │   ├── uebersicht-fahrten/
    │   │   ├── fahrplanzeit.yaml
    │   │   ├── verkehrsmittelkategorie.yaml
    │   │   ├── liniennummer.yaml
    │   │   ├── ziel.yaml
    │   │   ├── via.yaml
    │   │   ├── abfahrtsort.yaml
    │   │   ├── befoerderungshinweise.yaml
    │   │   ├── angebotshinweise.yaml
    │   │   ├── infotexte.yaml
    │   │   └── marketingname.yaml
    │   ├── informationen-zur-fahrt/
    │   │   └── ...
    │   ├── echtzeit/
    │   │   ├── verspaetung.yaml
    │   │   ├── ausfaelle-betriebszustandsaenderungen.yaml
    │   │   ├── zusatzinformationen.yaml
    │   │   └── reisendenlenkung.yaml
    │   └── anschluesse/
    │       └── ...
    └── schema.yaml          # Schema-Definition für alle Rules
```

## Rule-Format (je Datei)

```yaml
id: bs-ki-2.1
title: "Aktuelle Uhrzeit"
source:
  document: "BS-KI_DE.pdf"
  version: "1.0"
  chapter: "2.1"
  page: 16
quote: |
  «Wörtliches Zitat aus dem PDF – der vollständige Regeltext»
applicability:
  haltestelle:
    bahn: verbindlich
    bus_tram_metro: empfohlen
    schiff: empfohlen
    seilbahn: empfohlen
  fahrzeug_aussen:
    front: null
    seite: null
    heck: null
  fahrzeug_innen:
    bahn: verbindlich
    bus_tram_metro: verbindlich
    schiff: verbindlich
    seilbahn: null
  daten:
    einlieferung: null
```

## Arbeitsschritte

### Phase 1: Matrix parsen (deterministisch)
- [ ] Excel-Sheet "Bewertungsmatrix" → JSON/YAML mit allen Regeln + Verbindlichkeiten
- [ ] Mapping: Zeilen → Regel-IDs, Spalten → Kanäle/Transportmittel
- [ ] Ergebnis: `matrix.json` als Ground Truth

### Phase 2: PDF-Texte extrahieren (deterministisch)
- [ ] BS-KI_DE.pdf kapitelweise extrahieren (markitdown/pdfplumber)
- [ ] Kapitel-Nummern den Matrix-Zeilen zuordnen
- [ ] Pro Regel: wörtliches Zitat aus dem PDF isolieren

### Phase 3: Rules-Dateien erzeugen
- [ ] Matrix + PDF-Zitate zusammenführen → eine YAML-Datei pro Regel
- [ ] Schema validieren
- [ ] Deterministisch: gleiches Input → gleiches Output (kein LLM nötig für die Extraktion!)

### Phase 4: Verifikation
- [ ] Jede Rule-Datei gegen Matrix prüfen (Verbindlichkeiten stimmen)
- [ ] Stichproben: Zitate gegen PDF-Original manuell prüfen

## Offene Entscheidungen (Team)

- [ ] **Format:** YAML vs. OSCAL-YAML vs. JSON? → Vorschlag: erst YAML, dann OSCAL-Mapping
- [ ] **Granularität:** Eine Datei pro Matrix-Zeile? Oder pro Kapitel?
- [ ] **Sprachen:** Nur DE oder auch FR/IT parallel?
- [ ] **Tooling:** Python-Script oder Pipeline?
- [ ] **Wo leben die Rules?** `rules/` im Repo-Root oder unter `whomakestherules/rules/`?

## Aufgabenverteilung (Vorschlag)

| Aufgabe | Wer | Status |
|---------|-----|--------|
| Matrix parsen → JSON | | |
| PDF kapitelweise extrahieren | | |
| Rule-Schema definieren | | |
| Zusammenführung Matrix + PDF → Rules | | |
| Verifikation / Stichproben | | |
| Demo vorbereiten | | |

## Tools

- `markitdown` – PDF → Markdown (installiert: `~/Library/Python/3.14/bin/markitdown`)
- `pdfplumber` – PDF → Text mit Seitenreferenzen (installiert)
- `openpyxl` – Excel parsen (installiert)
- Python 3.14

---

*Erstellt: 23.06.2026, 09:54*
