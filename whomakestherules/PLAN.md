# Who Makes the Rules – Arbeitsplan

## Ziel

Aus dem BS-KI-Regelwerk (PDF + Matrix-Excel) deterministische, maschinenlesbare Rules-Dateien erzeugen.

Jede Regel wird **wörtlich zitiert** aus dem PDF. Die Matrix liefert die Struktur (was ist verbindlich/empfohlen für welches Transportmittel/Kanal).

## Datenquellen

| Datei | Inhalt | Rolle |
|-------|--------|-------|
| `Matrix_BS-KI_DE.xlsx` (Sheet "Bewertungsmatrix") | Regeln × Kanäle × Transportmittel → v/e/– | **Struktur & Ground Truth** |
| `BS-KI_DE.pdf` (64 Seiten) | Detaillierte Regeltexte, Definitionen, Beispiele | **Inhalt (wörtlich zitieren)** |

## Output-Struktur

```
whomakestherules/
└── rules/
    ├── bs-ki-de.yaml           # Gesamter Catalog als eine Datei
    ├── bs-ki-fr.yaml           # Französische Version (optional)
    └── schema/
        └── oscal-catalog.json  # NIST JSON-Schema zur Validierung
```

**Hinweis:** Ein OSCAL Catalog ist eine Datei mit verschachtelten Groups/Controls. Wir splitten NICHT in eine Datei pro Regel, sondern halten alles in einem Catalog – das ist OSCAL-konform und validierbar.

## Format-Entscheidung: OSCAL4Rail

**Entscheidung:** Wir nutzen **OSCAL4Rail** – ein leichtgewichtiges OSCAL-Catalog-Profil für Eisenbahn-Regelwerke. Details siehe [OSCAL4Rail.md](OSCAL4Rail.md).

**Warum OSCAL:**
- Offizielles JSON-Schema von NIST zur Validierung (YAML validierbar über JSON-Schema)
- Standardisiert → interoperabel mit anderen Tools/Bahnen
- Erweiterbar über `props` und `parts` ohne Schema-Bruch

**Warum leichtgewichtig:**
- Nur Catalog-Layer (kein Profile/Assessment für den Hackathon)
- Minimale Pflichtfelder, Rest optional
- Ein Catalog pro Regelwerk, ein Control pro Regel

### Catalog-Struktur (1 Datei = 1 Regelwerk)

```yaml
catalog:
  uuid: "<UUIDv4>"
  metadata:
    title: "Branchenstandard Kundeninformation (BS-KI)"
    published: "2026-01-01T00:00:00Z"
    last-modified: "2026-06-23T10:00:00Z"
    version: "1.0"
    oscal-version: "1.1.3"
    props:
      - name: country
        value: "CH"
      - name: language
        value: "de"
      - name: source-url
        value: "https://www.oev-info.ch/de/branchenstandard/nationaler-branchenstandard-kundeninformation"
  groups:
    - id: bs-ki-2
      title: "Allgemeine Informationsinhalte der Kundeninformation"
      controls:
        - id: bs-ki-2.1
          title: "Aktuelle Uhrzeit"
          parts:
            - name: statement
              prose: |
                «Wörtliches Zitat aus dem PDF – vollständiger Regeltext»
            - name: guidance
              prose: "Ergänzende Hinweise aus dem PDF (wenn vorhanden)"
          props:
            - name: source-chapter
              value: "2.1"
            - name: source-page
              value: "16"
            # Applicability als Props – je Kombination Kanal×Transportmittel
            - name: applicability
              value: "verbindlich"
              class: "haltestelle.bahn"
            - name: applicability
              value: "empfohlen"
              class: "haltestelle.bus-tram-metro"
            - name: applicability
              value: "verbindlich"
              class: "fahrzeug-innen.bahn"
```

### Erweiterbarkeit

Weitere Regelwerke werden als eigene Catalogs angelegt:

```
rules/
├── bs-ki-de.yaml           # Schweizer Branchenstandard KI
├── bs-ki-fr.yaml           # Gleicher Standard, Französisch
├── tsi-tat.yaml            # EU TSI Telematics (Zukunft)
└── schema/
    └── oscal-catalog.json  # NIST JSON-Schema zur Validierung
```

Cross-Referenzen zwischen Catalogs → später über OSCAL Control Mapping.

### Validierung

```bash
# OSCAL JSON-Schema von NIST herunterladen
curl -o rules/schema/oscal-catalog.json \
  https://raw.githubusercontent.com/usnistgov/OSCAL/main/json/schema/oscal_catalog_schema.json

# Validieren (Python jsonschema oder ajv)
python3 -c "
import yaml, jsonschema, json
with open('rules/bs-ki-de.yaml') as f:
    catalog = yaml.safe_load(f)
with open('rules/schema/oscal-catalog.json') as f:
    schema = json.load(f)
jsonschema.validate(catalog, schema)
print('✅ Valid OSCAL Catalog')
"
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

- [x] **Format:** OSCAL4Rail – leichtgewichtiges OSCAL Catalog Profil (siehe [OSCAL4Rail.md](OSCAL4Rail.md))
- [x] **Granularität:** Ein Catalog pro Regelwerk, ein Control pro Regel (Matrix-Zeile)
- [ ] **Sprachen:** Nur DE oder auch FR/IT parallel?
- [ ] **Tooling:** Python-Script oder Pipeline?
- [x] **Wo leben die Rules?** `whomakestherules/rules/`

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
