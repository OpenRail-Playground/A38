# ADR-007: compliance-trestle als Tooling-Basis für OSCAL4Rail

**Status:** Proposed
**Date:** 2026-08-03
**Deciders:** Jens Grote, Arpad Vasarhelyi

## Kontext

OSCAL4Rail benötigt Tooling für:
1. Validierung von OSCAL-Artefakten (Catalogs, Profiles, Assessments)
2. Profile Resolution (Cascade-Ebene → resolved Catalog)
3. Change Detection (Layer 3: strukturiertes Diff zwischen Catalog-Versionen)
4. AI-Agent-Integration (MCP-Server für automatisierte Compliance-Prüfung)

Für jede dieser Funktionen stehen bestehende Open-Source-Tools zur Verfügung. Die Frage ist: **Eigenes CLI von Grund auf bauen oder auf bestehende Tooling-Ökosysteme aufsetzen?**

## Alternativen

### Alternative A: Eigenes CLI (`oscal4rail` Python-Tool)

- Eigener Validator (`validate.py` – existiert bereits als Prototyp)
- Eigene Profile Resolution
- Eigenes Diff-Tooling (`diff.py`)
- Eigener MCP-Server

**Vorteile:**
- Volle Kontrolle über Implementierung und UX
- Keine externe Abhängigkeit
- Leichtgewichtig, angepasst auf Railway-Bedarf

**Nachteile:**
- Hoher Entwicklungsaufwand (Profile Resolution allein ist komplex)
- OSCAL-Schema-Updates müssen selbst nachgezogen werden
- Keine Community die mitentwickelt
- MCP-Server muss from scratch gebaut werden

### Alternative B: compliance-trestle + oscal-deep-diff

- **compliance-trestle** (IBM/OSCAL-Compass, Apache 2.0, Python) für: Import, Validate, Profile Resolution, Workspace-Management, Plugin-Architektur
- **oscal-deep-diff** (NIST, Public Domain, TypeScript/Node) für: Strukturiertes Diff zwischen OSCAL-Dokumenten
- **compliance-trestle-mcp** (OSCAL-Compass) für: AI-Agent-Integration via MCP
- Railway-spezifische Logik als **trestle-Plugin** (`trestle-oscal4rail`)

**Vorteile:**
- Profile Resolution funktioniert out-of-the-box (evaluiert mit BS-KI)
- Validierung gegen OSCAL 1.2.1 Schema eingebaut
- Plugin-Architektur erlaubt Railway-Extensions ohne Fork
- MCP-Server existiert bereits
- Aktive Community (IBM, GSA, FedRAMP nutzen es)
- oscal-deep-diff erkennt Control-Level-Änderungen zuverlässig (evaluiert)

**Nachteile:**
- Abhängigkeit von externem Projekt (Governance-Risiko)
- trestle ist Python, oscal-deep-diff ist TypeScript (zwei Runtimes)
- trestle hat viele Abhängigkeiten (>30 Packages)
- Railway-spezifische Semantik (tightened/relaxed) muss trotzdem selbst gebaut werden

### Alternative C: oscal-cli (NIST, Java)

- Offizielle NIST-Referenzimplementierung
- Validierung, Profile Resolution, Konvertierung

**Vorteile:**
- Offizielle Referenz
- Korrekteste Implementierung

**Nachteile:**
- Java-Runtime erforderlich
- Keine Plugin-Architektur
- Kein MCP-Server
- Weniger agile-authoring-freundlich

## Entscheidung

**Alternative B: compliance-trestle + oscal-deep-diff als Tooling-Fundament.**

Railway-spezifische Logik wird als trestle-Plugin implementiert (`trestle-oscal4rail`), das folgende Kommandos ergänzt:

| Kommando | Funktion |
|----------|----------|
| `trestle oscal4rail cascade` | Cascade-Ebenen analysieren (Profile-Kette) |
| `trestle oscal4rail diff` | Semantisches Diff mit Railway-Klassifikation (tightened/relaxed/added/removed) |
| `trestle oscal4rail assess` | Assessment-Template generieren mit Railway-Bewertungsskala |
| `trestle oscal4rail validate` | Railway-Constraints zusätzlich zum NIST-Schema prüfen |

Das strukturelle Diffing delegiert an oscal-deep-diff (als Subprocess oder portierter Subset).

## Evaluierungs-Ergebnisse

### compliance-trestle v4.2.0

Evaluiert am 2026-08-03 mit BS-KI v1.0 Catalog:

```
$ trestle import -f bs-ki-de.yaml -o bs-ki-de
✅ Import erfolgreich

$ trestle validate -a
✅ VALID (3 unreferenzierte UUIDs in back-matter – Warning, kein Fehler)

$ trestle author profile-resolve -n sbb-subset -o resolved-sbb
✅ Resolved Catalog enthält nur die 5 selektierten Controls
✅ Props und Statements vollständig erhalten
✅ Link rel="resolution-source" auf Quell-Catalog
```

Workspace-Struktur bildet alle OSCAL-Modelle ab:
```
catalogs/ profiles/ assessment-plans/ assessment-results/
component-definitions/ mapping-collections/ system-security-plans/
plan-of-action-and-milestones/
```

### oscal-deep-diff v1.0.0

Evaluiert am 2026-08-03 mit BS-KI v1.0 → simulierter v2.0:

```
Änderungen eingefügt:
- Schwellwert 800 → 500 (Text-Änderung in bs-ki-2.1)
- Applicability empfohlen → verbindlich (Obligation verschärft)
- Neuer Control bs-ki-2.99 (hinzugefügt)

Ergebnis:
✅ Alle 3 Änderungen erkannt
✅ JSON-Pointer auf geänderte Felder
✅ Neuer Control als "rightOnly" identifiziert
✅ Performance: 7ms für 42 Controls
```

Output-Format:
```json
{
  "changes": [
    {"change": "property_changed", "leftPointer": "/catalog/groups/0/controls/0/parts/0/prose", ...},
    {"change": "property_changed", "leftPointer": "/catalog/groups/0/controls/0/props/2/value", ...},
    {"change": "array_changed", "rightOnly": [{"rightElement": {"id": "bs-ki-2.99", ...}}]}
  ],
  "score": 230
}
```

## Konsequenzen

### Positiv
- Schneller Time-to-Value: Profile Resolution, Validation, Import funktionieren sofort
- MCP-Server für AI-Agents existiert
- Community-Anschluss an OSCAL-Compass Ökosystem
- FedRAMP-Plugin als Referenz für eigenes Railway-Plugin

### Negativ
- Zwei Runtimes (Python + Node.js) für den vollständigen Stack
- Governance-Risiko: Abhängigkeit von IBM-geführtem OSS-Projekt
- oscal-deep-diff ist nicht auf npm publiziert (muss von GitHub installiert werden)

### Maßnahmen
- trestle-Plugin als separates Paket (`trestle-oscal4rail`), nicht als Fork
- oscal-deep-diff Subset für die benötigte Diff-Logik ggf. nach Python portieren (eliminiert Node-Dependency)
- Fallback: Bei Einstellung von trestle kann der Plugin-Code als Standalone-CLI extrahiert werden

## Referenzen

- [compliance-trestle](https://github.com/oscal-compass/compliance-trestle) – Apache 2.0
- [compliance-trestle-mcp](https://github.com/oscal-compass/compliance-trestle-mcp) – MCP-Server
- [oscal-deep-diff](https://github.com/usnistgov/oscal-deep-diff) – Public Domain
- [oscal-cli](https://github.com/usnistgov/oscal-cli) – NIST Referenz (Java)
- [compliance-trestle-fedramp](https://github.com/oscal-compass/compliance-trestle-fedramp) – Referenz für sektorales Plugin
