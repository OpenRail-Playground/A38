# Hack4Rail 2026 – Challenge 7: "Who Makes the Rules"

## Team: A38 (Passierschein A38)

- Rebeca
- Simon
- Jens
- Jonathan

## Challenge

Regeln/Vorgaben im Eisenbahnsektor sind verstreut über heterogene Quellen:
- PDF-Dokumente (Regelwerke, TSIs, nationale Vorschriften)
- Word-Dateien (interne Richtlinien, Entwürfe)
- Jira-Tickets (Anforderungen, Change Requests)
- Wikis (Confluence, MediaWiki)
- SharePoint-Seiten (Team-Dokumentation)

**Kernproblem:** Niemand findet die relevante Regel im Heuhaufen. Änderungen werden nicht nachvollzogen. Regeln sind Freitext statt maschinenlesbar.

## Drei Kernfragen

1. **Analyse:** Wie extrahieren wir aus heterogenen Quellen maschinenlesbare Regeln?
2. **Change Tracking:** Wie verfolgen wir Änderungen an Regeln über Zeit und Quellen?
3. **Deterministische Extraktion:** Wie kommen wir von Freitext zu strukturierten, eindeutigen Regeln?
4. **Zukunft:** Wie sollten Regeln zukünftig geschrieben/gepflegt werden?

## Architektur-Idee

```
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                                │
│  PDF Parser │ DOCX Parser │ Jira API │ Confluence API │ SPO API  │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 NORMALIZATION LAYER                               │
│  Text-Extraktion │ Chunking │ Metadaten (Quelle, Version, Datum) │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              RULE EXTRACTION LAYER                                │
│  LLM-basiert: "Extrahiere Regeln als strukturierte Aussagen"     │
│  Format: IF <Bedingung> THEN <Pflicht/Verbot> [Quelle, §, Vers.] │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              CHANGE TRACKING LAYER                                │
│  Git-artige Versionierung │ Diff auf Regel-Ebene │ Notifications │
└──────────────────────────┬──────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              QUERY / COMPLIANCE LAYER                             │
│  "Welche Regeln gelten für X?" │ "Was hat sich geändert seit Y?" │
└─────────────────────────────────────────────────────────────────┘
```

## Hackathon-Scope: Vertikaler Durchstich

**Ziel:** In 3 Minuten zeigen: "Regelwerk rein → strukturierte Regeln raus → Änderungen sichtbar"

### MVP-Features

1. PDF/DOCX einlesen und Text extrahieren
2. LLM extrahiert strukturierte Regeln (JSON/YAML)
3. Zwei Versionen vergleichen → Diff auf Regel-Ebene
4. Einfache Abfrage: "Welche Regeln gelten für [Thema]?"

### Nice-to-have (wenn Zeit)

- Zweite Quelle (Wiki/Jira) anbinden
- Web-UI für Live-Demo
- Regelformat-Vorschlag für die Zukunft ("Rules as Code")

## Zeitplan

| Block | Wann | Fokus |
|-------|------|-------|
| Mo Abend | 19:30 – 23:00 (3,5h) | Setup, Beispiel-Dokumente, Ingestion-Pipeline |
| Di Vormittag | 08:00 – 12:00 (4h) | Rule Extraction Prompts, strukturiertes Output |
| Di Nachmittag | 13:00 – 18:00 (5h) | Diff/Change-Tracking, Demo-UI |
| Di Abend | 18:00 – 23:00 (5h) | Demo-Flow, Präsentation, Edge Cases |
| Mi Früh | 08:00 – 10:00 (2h) | Letzte Fixes, Proben |
| Mi | 10:00 – 11:00 | Präsentation (3 Min) |

## 3-Minuten-Präsentation – Storyboard

| Sek | Inhalt |
|-----|--------|
| 0-30 | Problem: "500 Seiten Regelwerk – was gilt für MICH?" (Heuhaufen-Bild) |
| 30-60 | Live-Demo: Dokument rein → Regeln extrahiert |
| 60-120 | "Neue Version kommt..." → Diff: 3 geändert, 1 neu, 2 gestrichen |
| 120-150 | Zukunftsvision: automatisches Change-Tracking für alle Regelquellen |
| 150-180 | Punchline + nächste Schritte |

## Tech-Stack (Vorschlag)

- **Sprache:** Python
- **PDF-Parsing:** pymupdf / pdfplumber
- **DOCX-Parsing:** python-docx
- **LLM:** OpenAI API / lokales Modell (Ollama)
- **Output-Format:** JSON mit Schema
- **Diff:** struktureller Vergleich auf Regel-ID-Ebene
- **Demo-UI:** Streamlit oder CLI

## Offene Fragen

- [ ] LLM-Zugang: OpenAI API Key vorhanden? Oder lokales Modell (Ollama)?
- [ ] Sprache der Regeln: Deutsch? Englisch? Beides? (BS-KI hat DE/FR/IT)
- [ ] Wie groß soll der Scope der Demo sein? (1 Dokument vs. mehrere Quellen)
- [ ] Nextcloud-Credentials für Team-Ablage

### Governance Engine – Offene Punkte

#### 1. NIST OSCAL als gemeinsames Framework

- [ ] OSCAL-Spezifikation analysieren: Welche Layer sind für Eisenbahn-Governance relevant?
  - Catalog (Regelkatalog) → direkt anwendbar
  - Profile (Auswahl/Anpassung) → z.B. länderspezifische Regelauswahl
  - Component Definition → Wiederverwendbare Bausteine (z.B. "Echtzeitinformation-Modul")
  - Assessment Results → Compliance-Bewertung gegen Regelwerk
- [ ] Mapping: OSCAL-Felder ↔ Eisenbahn-Domäne definieren
  - `control` = eine Governance-Regel (z.B. BS-KI Kapitel 4.2.1)
  - `group` = Regelkapitel/Themenbereich
  - `parameter` = variable Werte (z.B. Schwellwerte, Fristen)
  - `part` = Bewertungskriterien / Nachweispflichten
- [ ] Gemeinsames Schema für alle Bahnen (DB, SBB, ÖBB, SNCF) vorschlagen
  - Namespace-Konzept: `urn:rail:bs-ki:`, `urn:rail:tsi-tat:`, `urn:rail:ril420:`
  - Mehrsprachigkeit: OSCAL unterstützt `xml:lang` / Locale-Felder
- [ ] OSCAL-Tooling evaluieren: https://oscal.io/tools/
  - Trestle (IBM) – Python-basiert, CLI für Catalog/Profile-Management
  - Compliance-Trestle → könnte als Basis für Rail-Governance dienen

#### 2. Governance Ownership / Berechtigungskonzept

- [ ] Nur Governance Owner dürfen Vorgaben schreiben/ändern
  - Rollenmodell: Owner (schreibt) → Reviewer (prüft) → Consumer (liest/befolgt)
  - Technisch: Git-Branch-Protection + CODEOWNERS oder Editor mit Rollenkonzept
  - Jede Regel hat ein `responsible`-Feld (Organisation/Person die sie verantwortet)
- [ ] Freigabe-Workflow für Regeländerungen
  - Analog Merge Request: Owner erstellt Entwurf → Review → Freigabe → Publish
  - Vier-Augen-Prinzip für Regeländerungen
  - Audit-Trail: Wer hat wann was geändert und wer hat es freigegeben?
- [ ] Sichtbarkeit vs. Editierrecht trennen
  - Alle dürfen LESEN (Consumer)
  - Nur Owner darf SCHREIBEN
  - Reviewer darf KOMMENTIEREN und FREIGEBEN

#### 3. Versionierung + Diff auf Regel-Ebene

- [ ] Jede Regel = eine Datei → Git-Versionierung gratis
  - Dateiname = Regel-ID (z.B. `bs-ki-4.2.1-echtzeitinformation.yaml`)
  - Jede Änderung = Git-Commit mit Conventional Commit Message
  - Tags für offizielle Versionen (z.B. `bs-ki/v2026.1`)
- [ ] Semantischer Diff (nicht nur Textdiff)
  - Was hat sich inhaltlich geändert? (Schwellwert angepasst, Pflicht verschärft, Ausnahme ergänzt)
  - Strukturierter Vergleich: Feld-für-Feld statt Zeilenvergleich
  - Kategorisierung: `verschärft` | `gelockert` | `präzisiert` | `neu` | `entfallen`
- [ ] Change-Notifications
  - Wer ist betroffen? (Consumer, die diese Regel referenzieren)
  - Was muss der Consumer tun? (Compliance prüfen, Implementierung anpassen)
  - Wann tritt die Änderung in Kraft? (Übergangsfristen)
- [ ] Changelog automatisch generieren
  - Pro Release: Liste aller geänderten Regeln mit Kategorisierung
  - Maschinenlesbar (YAML/JSON) UND menschenlesbar (Markdown/PDF)

## Datenquelle (gesichert)

**Schweizer Branchenstandard Kundeninformation (BS-KI)**
- Website: https://www.oev-info.ch/de/branchenstandard/nationaler-branchenstandard-kundeninformation
- Nextcloud Team-Ablage: https://share.openrailassociation.org/apps/files/files/52349?dir=/Hack4Rail%202026/Challenges/7%20-%20Who%20makes%20the%20rules

### Downloads

| Dokument | Format | URL |
|----------|--------|-----|
| BS-KI (DE) | PDF | https://www.oev-info.ch/sites/default/files/2026-01/BS-KI_DE.pdf |
| BS-KI (FR) | PDF | https://www.oev-info.ch/sites/default/files/2026-01/BS-KI_FR.pdf |
| BS-KI (IT) | PDF | https://www.oev-info.ch/sites/default/files/2026-01/BS-KI_IT_0.pdf |
| Matrix BS-KI (DE) | XLSX | https://www.oev-info.ch/sites/default/files/2025-12/Matrix_BS-KI_DE.xlsx |
| Matrix BS-KI (FR) | XLSX | https://www.oev-info.ch/sites/default/files/2026-02/Matrix_BS-KI_FR.xlsx |
| Matrix BS-KI (IT) | XLSX | https://www.oev-info.ch/sites/default/files/2025-12/Matrix_BS-KI_IT.xlsx |

### Weitere Quellen (noch zu prüfen)

- Fachliche Ausführungsbestimmungen: https://www.oev-info.ch/de/branchenstandard/fachliche-ausfuehrungsbestimmungen/download-fachliche-ausfuehrungsbestimmungen
- Technische Ausführungsbestimmungen: https://www.oev-info.ch/de/branchenstandard/technische-ausfuehrungsbestimmungen/technische-ausfuehrungsbestimmungen
- Übergangsdokument: https://www.oev-info.ch/de/branchenstandard/fachliche-ausfuehrungsbestimmungen/download-uebergangsdokument

### Warum perfekt für den Hackathon

1. Öffentlich zugänglich (kein Login)
2. Mehrsprachig (DE/FR/IT) → Cross-Language-Matching
3. PDF + Excel → heterogene Formate
4. Versioniert (2025-12, 2026-01, 2026-02) → Change Tracking
5. Matrix-Excel = Ground Truth für Validierung

## Weitere Regelwerke (Kontext / Future Work)

| Quelle | Inhalt | Zugang | Für Demo? |
|--------|--------|--------|-----------|
| TSI Telematics (EU 2026/253) | EU-weit: Datenbereitstellung Fahrgastinfo | Öffentlich (EUR-Lex) | ✅ Optional |
| DB Ril 420 ff. | Fahrgastinformation DB-intern | KRWD (Intranet, VPN) | ❌ Nicht zeigbar |
| ÖBB interne Vorgaben | Äquivalent, nicht öffentlich | Nicht zugänglich | ❌ |
| SNCF Référentiel | Äquivalent, nicht öffentlich | Nicht zugänglich | ❌ |

**Hinweis:** Kundeninformation ≠ Fahrgastrechte. BS-KI und Ril 420 regeln das "Was zeige ich wann wo wie", nicht Entschädigungsansprüche.

**KRWD:** https://krwd.intranet.deutschebahn.com/ (nur mit DB-VPN)
**Intranet-Suche:** https://anonyme-suche.intranet.deutschebahn.com/suche?lang=de&filter=regulations&q=Fahrgastinformation

## Idee: Governance Engine (Regeleditor + OSCAL)

### Konzept

Ein Web-Editor, der wie ein Word-Dokument aussieht, aber im Hintergrund strukturierte, maschinenlesbare Daten erzeugt. Aus dem gleichen Datenmodell werden generiert:
- **OSCAL-YAML** (maschinenlesbar, KI-abfragbar, validierbar)
- **Word (.docx)** (für Menschen, Freigabeprozess)
- **PDF** (für Veröffentlichung, Archivierung)

### Warum nicht Word mit Hidden Attributes?

Word-Templates mit Content Controls / Custom XML Parts sind möglich, aber fragil:
- Nutzer brechen die Struktur (Copy-Paste, Formatierung)
- Parsing-Logik wird komplex und fehleranfällig
- Validierung erst NACH Export möglich (zu spät)
- Zwei Welten synchron halten = dauerhafter Wartungsaufwand

**→ Besser: Editor-First.** Der Editor ist die Single Source of Truth. Word/PDF sind Ausgabeformate.

### Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│                    GOVERNANCE ENGINE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌────────────────┐    ┌──────────────────┐  │
│  │  Katalog     │    │  Web-Editor     │    │  Renderer        │  │
│  │  (Regelwerk- │───▶│  (WYSIWYG,     │───▶│  .docx           │  │
│  │   Schema)    │    │   Word-Look)    │    │  .pdf            │  │
│  └─────────────┘    └───────┬────────┘    │  .yaml (OSCAL)   │  │
│                              │             └──────────────────┘  │
│                              ▼                                    │
│                     ┌─────────────────┐                          │
│                     │  Zentraler Store │                          │
│                     │  (Git / DB)      │                          │
│                     └────────┬────────┘                          │
│                              │                                    │
│                     ┌────────┴────────┐                          │
│                     ▼                 ▼                           │
│              ┌────────────┐   ┌────────────────┐                 │
│              │ KI-Abfrage  │   │ Change Tracking │                 │
│              │ (RAG/SQL)   │   │ (Git-Diff auf   │                 │
│              │             │   │  Regel-Ebene)   │                 │
│              └────────────┘   └────────────────┘                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Zentrale Speicherung (nicht lokal!)

**Problem:** Regeln dürfen NICHT lokal beim User liegen. Sonst: keine Versionierung, kein Change Tracking, keine KI-Abfrage, kein Multi-User.

**Lösung – drei Optionen:**

| Option | Backend | Vorteile | Nachteile |
|--------|---------|----------|-----------|
| **A) Git-Repo** | GitLab/GitHub + YAML-Dateien | Versionierung gratis, Diff gratis, CI/CD, MR-Workflow | Kein Echtzeit-Multi-User |
| **B) Datenbank + Git** | PostgreSQL + Git-Sync | Echtzeit-Abfragen, KI-SQL, Multi-User | Mehr Infrastruktur |
| **C) Git + DataLake** | Git als Source of Truth, DataLake-Sync für Analysen | Strukturierte KI-Abfragen, Versionierung | Sync-Latenz |

**Empfehlung für hack4rail:** Option A (Git-Repo) als MVP. YAML-Dateien in Git, CI/CD generiert Word+PDF bei jedem Commit. KI liest direkt aus dem Repo.

**Langfristig:** Option B oder C – Git bleibt Source of Truth, Datenbank/DataLake als Query-Layer.

### Datenfluss

```
User (Browser) ──▶ Web-Editor ──▶ API ──▶ Git-Repo (YAML)
                                              │
                                    ┌─────────┼─────────┐
                                    ▼         ▼         ▼
                               CI/CD:     KI-Index:   Diff:
                               .docx      Embedding   Regel-Changelog
                               .pdf       + SQL-View
```

### Bezug zu OSCAL / vASE

Das Konzept ist eine Verallgemeinerung von vASE-OSCAL:
- **vASE-OSCAL** = EA-Governance-Vorgaben maschinenlesbar (10 Prinzipien, 5 Grundsätze)
- **Governance Engine** = JEDE Vorgabe/Regel maschinenlesbar (Eisenbahn-Regelwerke, TSIs, nationale Vorschriften)

Gleiche Schichtentrennung: Katalog → Profil → Assessment

### Tech-Stack (Hackathon-tauglich)

| Komponente | Technologie |
|-----------|-------------|
| Editor | TipTap / Plate (ProseMirror-basiert, Block-Editor mit Word-Feeling) |
| Backend | Python (FastAPI) oder Node.js |
| Storage | Git-Repo (YAML-Dateien, 1 Datei pro Regel) |
| Word-Export | python-docx oder docx (npm) |
| PDF-Export | Playwright page.pdf() oder WeasyPrint |
| KI-Layer | LLM liest OSCAL-YAML direkt, optional Embedding-Index |
| Schema | JSON Schema für Validierung im Editor |

### Abgrenzung zum Hauptansatz

Die Governance Engine ist eine **Zukunftsvision** für "wie sollten Regeln geschrieben werden". Der Hauptansatz (Ingestion → Extraction → Diff) löst das Problem "wie kommen wir an bestehende Regeln ran".

Beides ergänzt sich:
1. **Heute:** Bestehende PDFs/Word → KI extrahiert Regeln → strukturiertes Format
2. **Morgen:** Neue Regeln werden direkt im Editor geschrieben → nie wieder Freitext-PDFs

---

## Status (Mo 22.06. Abend)

- [x] Challenge verstanden, Team A38 benannt
- [x] Datenquelle identifiziert (BS-KI Schweiz)
- [x] Alle deutschen Vorgabendokumente heruntergeladen (7 Dateien, 31 MB)
- [x] Andere Sprachen separiert in `data/other_languages/`
- [x] Vergleich DB/ÖBB/SNCF – nur BS-KI und TSI Telematics öffentlich

## Status (Di 23.06. Morgen, 07:00)

- [x] Governance Engine Konzept entwickelt (Editor-First → OSCAL + Word + PDF)
- [x] Zentrale Speicherung: 3 Optionen bewertet (Git / DB+Git / Git+DataLake)
- [x] NIST OSCAL Standard analysiert (Layers, Catalog Model, YAML-Struktur)
- [x] Mapping OSCAL → Eisenbahn-Governance erstellt
- [x] Rail-OSCAL-Schema vorgeschlagen (mit Namespace-Konzept für alle Bahnen)
- [x] Governance Ownership / Berechtigungskonzept skizziert
- [x] Versionierung + semantischer Diff konzipiert
- [x] OSCAL-Analyse als eigene Datei: `OSCAL-ANALYSE.md`
- [ ] KRWD/Ril 420 prüfen (VPN nötig)
- [ ] BS-KI_DE.pdf analysieren (Struktur, Kapitel, Regelstruktur)
- [ ] Matrix-Excel als Ground Truth parsen
- [ ] LLM-Prompt für Regelextraktion entwickeln
- [ ] Ersten vertikalen Durchstich: 1 BS-KI-Kapitel → OSCAL-YAML
- [ ] Demo-Pipeline aufsetzen (Python)

### Nächste Schritte (Di Vormittag)

1. BS-KI_DE.pdf analysieren (Struktur, Kapitel, Regelstruktur)
2. Matrix_BS-KI_DE.xlsx parsen → Ground Truth
3. Ersten Extraction-Prompt testen (1 Kapitel → OSCAL-YAML)
4. Pipeline-Skeleton aufsetzen (Python)
5. Optional: KRWD per VPN prüfen
