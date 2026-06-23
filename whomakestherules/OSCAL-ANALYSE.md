# NIST OSCAL – Analyse für die Governance Engine (hack4rail 2026)

## Überblick

**OSCAL Version:** 1.2.1 (aktuell, alle Modelle im Status „Released")
**Quelle:** https://pages.nist.gov/OSCAL/learn/concepts/layer/

## Architektur: 3 Schichten, 9 Modelle

```
┌─────────────────────────────────────────────────────────────────┐
│  ASSESSMENT LAYER                                                │
│  Assessment Plan │ Assessment Results │ POA&M                    │
├─────────────────────────────────────────────────────────────────┤
│  IMPLEMENTATION LAYER                                            │
│  System Security Plan (SSP) │ Component Definition               │
├─────────────────────────────────────────────────────────────────┤
│  CONTROL LAYER                                                   │
│  Catalog │ Profile │ Control Mapping                             │
└─────────────────────────────────────────────────────────────────┘
```

Jede Schicht referenziert die darunterliegende. Informationsfluss von unten nach oben.

## Relevante Modelle für Eisenbahn-Governance

| Modell | Zweck | Für uns relevant? |
|--------|-------|-------------------|
| **Catalog** | Sammlung von Controls (Regeln) hierarchisch gruppiert | ✅ Kernmodell |
| **Profile** | Auswahl + Tailoring von Controls aus einem/mehreren Katalogen | ✅ Länderspezifische Auswahl |
| **Control Mapping** | Beziehungen zwischen Controls verschiedener Kataloge | ✅ Cross-Referenz BS-KI ↔ TSI |
| Component Definition | Wiederverwendbare Bausteine | ⚠️ Evtl. für Systeme |
| SSP | Architekturplan eines Systems | ❌ Nicht für Regelwerke |
| Assessment Plan | Wie geprüft wird | ⚠️ Evtl. für Compliance-Checks |
| Assessment Results | Prüfergebnisse | ✅ Compliance-Bewertung |
| POA&M | Maßnahmenplan bei Abweichungen | ⚠️ Evtl. langfristig |

## Catalog Model – Kernstruktur

Quelle: https://pages.nist.gov/OSCAL/learn/tutorials/control/basic-catalog/

```yaml
catalog:
  uuid: <UUIDv4>
  metadata:
    title: "Titel des Katalogs"
    published: "2023-10-12T00:00:00Z"
    last-modified: "2025-08-26T17:57:28Z"
    version: "1.1"
    oscal-version: "1.1.3"
  groups:                    # Hierarchische Gruppierung (Kapitel)
  - id: s1
    title: "Kapitelname"
    props:
    - name: label
      value: "1"
    groups:                  # Verschachtelte Unterkapitel
    - id: s1.1
      title: "Abschnitt"
      controls:              # Die eigentlichen Regeln
      - id: s1.1.1
        title: "Regelname"
        params:              # Variable Werte (Schwellwerte, Fristen)
        - id: s1.1.1-prm1
          label: "Beschreibung"
          select:
            how-many: one-or-more
            choice: [...]
        props:
        - name: label
          value: "1.1.1"
        parts:               # Inhaltsteile der Regel
        - id: s1.1.1_stm
          name: statement    # Verpflichtender Regeltext
          prose: "..."
        - id: s1.1.1_gdn
          name: guidance     # Implementierungshinweise
          parts:             # Verschachtelte Sub-Parts
          - id: s1.1.1_gdn.1
            name: objective
            prose: "..."
        - id: s1.1.1_inf
          name: information  # Ergänzende Hinweise
          prose: "..."
```

### Wichtige Konzepte

- **Groups** können verschachtelt werden (Kapitel → Abschnitt → Unterabschnitt)
- **Controls** enthalten die eigentlichen Regeln
- **Parts** strukturieren den Regelinhalt: `statement`, `guidance`, `information`, `objective`
- **Params** machen variable Werte explizit und maschinenlesbar
- **Props** sind Metadaten (Labels, Klassifizierung)
- **UUID** auf Dokumentebene = Versionskontrolle (neue UUID bei jeder Änderung)

## Mapping OSCAL → Eisenbahn-Governance

| OSCAL-Konzept | Eisenbahn-Äquivalent | Beispiel |
|---------------|---------------------|----------|
| **Catalog** | Regelwerk/Vorgabenkatalog | BS-KI, Ril 420, TSI Telematics |
| **Group** | Kapitel/Abschnitt | „4. Echtzeitinformation" |
| **Control** | Einzelne Regel/Vorgabe | „4.2.1 Anzeige bei Verspätung > 3 Min" |
| **Part (statement)** | Verpflichtender Regeltext | „Die Information MUSS angezeigt werden" |
| **Part (guidance)** | Implementierungshinweise | „Empfohlen über SIRI-SX Kanal" |
| **Part (information)** | Ergänzende Hinweise | „Gilt nicht für Güterverkehr" |
| **Props** | Metadaten/Labels | Kapitelnummer, Klassifizierung |
| **Params** | Variable Werte | Schwellwert (z.B. „3 Minuten") |
| **Profile** | Länderspezifische Auswahl | „Schweiz: alle BS-KI Controls, plus Anhang 2" |
| **Control Mapping** | Cross-Referenz zwischen Regelwerken | BS-KI 4.2.1 ≈ TSI TAT Art. 12.2 |
| **Assessment Results** | Compliance-Bewertung | „Bahn X erfüllt 87% der BS-KI Controls" |

## Warum OSCAL passt

1. **Hierarchische Gruppierung** – Kapitel → Abschnitt → Regel (genau wie BS-KI aufgebaut)
2. **Parts-System** – Trennung von Pflichttext (statement), Anleitung (guidance), Zusatzinfo (information)
3. **Parameter** – Variable Werte (Schwellwerte, Fristen) als eigene Entität → maschinenlesbar änderbar
4. **Profile** – Länderspezifische Auswahl ohne Katalog zu duplizieren
5. **Control Mapping** – Querverweise zwischen Regelwerken (BS-KI ↔ TSI ↔ nationale Regeln)
6. **Versionierung** – UUID + `last-modified` + `version` in Metadata
7. **Serialisierung** – XML, JSON, YAML gleichwertig unterstützt
8. **JSON Schema** – Validierung möglich
9. **Tooling** – IBM Trestle (Python CLI), OSCAL-CAT (Web Editor)

## Vorgeschlagenes Rail-OSCAL-Schema

```yaml
catalog:
  uuid: <uuid>
  metadata:
    title: "Branchenstandard Kundeninformation (BS-KI)"
    published: "2026-01-01T00:00:00Z"
    last-modified: "2026-01-15T10:30:00Z"
    version: "2026.1"
    oscal-version: "1.2.0"
    props:
    - name: jurisdiction
      value: "CH"                # ← länderspezifisch
    - name: domain
      value: "rail-passenger-information"
    - name: responsible-organization
      value: "VöV/UTP"          # ← Governance Owner!
    - name: language
      value: "de"
  groups:
  - id: bski-4
    title: "Echtzeitinformation"
    props:
    - name: label
      value: "4"
    controls:
    - id: bski-4.2.1
      title: "Anzeige bei Verspätung"
      params:
      - id: bski-4.2.1-threshold
        label: "Verspätungsschwelle"
        value: "PT3M"            # ← ISO 8601 Duration: 3 Minuten
      parts:
      - id: bski-4.2.1_stm
        name: statement
        prose: |
          Bei einer prognostizierten Verspätung von mehr als
          {{ insert: param, bski-4.2.1-threshold }} MUSS die
          Echtzeitinformation am Perron angezeigt werden.
      - id: bski-4.2.1_gdn
        name: guidance
        prose: |
          Die Anzeige soll über SIRI-SX oder VDV 454 realisiert werden.
          Fallback: Textanzeige mit vordefinierten Ereignistexten gem. Anhang 1.
      - id: bski-4.2.1_inf
        name: information
        prose: |
          Gilt für alle Haltestellen mit elektronischer Anzeige.
          Ausnahme: Bedarfshalte ohne Fahrgastinformationsanlage.
```

## Namespace-Vorschlag für alle Bahnen

```
urn:rail:bs-ki:<control-id>       # Schweiz (BS-KI)
urn:rail:tsi-tat:<article>        # EU (TSI Telematics)
urn:rail:ril420:<paragraph>       # Deutschland (Ril 420)
urn:rail:oebb-ki:<control-id>     # Österreich
urn:rail:sncf-ref:<control-id>    # Frankreich
```

## OSCAL-Tooling

| Tool | Sprache | Nutzen |
|------|---------|--------|
| [IBM Trestle](https://github.com/oscal-compass/compliance-trestle) | Python | CLI für Catalog/Profile-Management |
| [OSCAL-CAT](https://github.com/usnistgov/oscal-cat) | Web | Content Authoring Tool |
| JSON Schema | – | Validierung von YAML/JSON |
| XSLT Converters | – | XML ↔ JSON Konvertierung |

## Bezug zu vASE-OSCAL (DB Systel)

Das vASE-OSCAL-Projekt (db-architekturprinzipien-vase-alpha) nutzt dasselbe Prinzip:
- 10 Architekturprinzipien + 5 Grundsätze als OSCAL Catalog
- Bewertungsskala als Parts (vollständig erfüllt, teilweise, nicht erfüllt, nicht relevant)
- Assessment Results für ausgefüllte vASE-Instanzen

→ Gleiche Architektur, andere Domäne. Wiederverwendbare Patterns.

---

*Erstellt: 23.06.2026 für hack4rail Challenge 7 „Who Makes the Rules"*
