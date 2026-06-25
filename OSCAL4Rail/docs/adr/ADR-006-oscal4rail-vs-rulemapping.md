# ADR-006: OSCAL4Rail und Rulemapping – Komplementarität oder Konkurrenz?

**Status:** Accepted
**Date:** 2026-06-25
**Deciders:** Jens Grote, Arpad Vasarhelyi
**Technical Story:** Evaluation des Rulemapping-Builder-Exports (Pilot BS-KI 2.1, 2026-06-25)

---

## Kontext und Problemstellung

Im Rahmen der SPRIND-Initiative „Law as Code" hat sich Rulemapping als zentrale Methodik für maschinenlesbare Gesetzgebung etabliert. OSCAL4Rail verfolgt mit NIST OSCAL einen anderen Ansatz für dasselbe Grundproblem: Regulatorik maschinenlesbar machen.

**Die zentrale Frage:** Sind OSCAL4Rail und Rulemapping konkurrierende Ansätze – oder ergänzende Werkzeuge, die durch Integration ihre jeweiligen Stärken ausspielen?

### Auslöser

- SPRIND-Initiative „Law as Code" mit Rulemapping als Kernmethodik
- Pilot-Test des Rulemapping Builders mit BS-KI 2.1 (erfolgreich, 2026-06-25)
- Bahnen unterliegen einer tiefen Regulierungskaskade (EU → National → Branche → Konzern → Tochtergesellschaft)
- Bedarf an Klarheit für die OpenRail-Incubation und Stakeholder-Kommunikation

### Die Regulierungskaskade

Eisenbahnregulierung ist kein flaches Regelwerk, sondern eine Vererbungshierarchie mit konformer Spezialisierung:

```
EU-Richtlinie / TSI (abstrakt)
  "Systeme müssen gegen bekannte Schwachstellen geschützt werden"
    │
    ▼ nationale Umsetzung
BSI IT-Grundschutz / BSKG / EBO
  "Patches müssen nach Risikobewertung eingespielt werden"
    │
    ▼ Konzernregel
DB Richtlinie
  "Du musst nach BSI Grundschutz patchen"
    │
    ├─▼ DB Systel                          ├─▼ DB InfraGO
    │  "CVSS Score bestimmt Frist:         │  "Nur KRITIS-Systeme,
    │   Critical ≤72h, High ≤7d..."        │   nach Methode XYZ"
    │                                       │
    └── beide KONFORM zur DB-Richtlinie ───┘
```

Jede Ebene **spezialisiert** die darüber liegende – sie darf konkretisieren, aber nicht widersprechen. Unterschiedliche Tochtergesellschaften dürfen die gleiche Oberregel unterschiedlich, aber jeweils konform umsetzen.

---

## Entscheidungstreiber (Decision Drivers)

1. **Regelinhalt** – Was steht in der Regel? Verbatim, auditierbar.
2. **Anwendbarkeit** – Für wen gilt es? (Kanal, Verkehrsträger, Obligation)
3. **Entscheidungslogik** – Unter welchen Bedingungen gilt es? (Schwellenwerte, Ausnahmen)
4. **Change Tracking** – Was hat sich geändert? Neu, weggefallen, verschärft, gelockert, ersetzt?
5. **Konsistenz & Redundanz** – Gibt es Doppelungen, Widersprüche, Ergänzungen über Regelwerke und Ebenen hinweg?
6. **Kaskade & Vererbung** – Kann die Hierarchie EU → National → Konzern → Tochter abgebildet werden?
7. **Konformitätsprüfung** – Ist eine Spezialisierung noch konform zur Oberregel?
8. **Schema-Validierbarkeit** – CI-fähige Validierung gegen ein formales Schema?
9. **Stabile Identifikatoren** – Für Versionsdiff und systemübergreifende Referenzierung?
10. **Offenheit** – Kein Vendor-Lock-in, Open Source, offene Standards?
11. **Unabhängigkeit** – Jeder Ansatz funktioniert auch allein?

---

## Analyse: Stärken und Schwächen

### OSCAL4Rail

| Dimension | Stärke | Schwäche |
|-----------|--------|----------|
| Regelinhalt | Verbatim-Zitate, auditierbar, keine Interpretation | – |
| Anwendbarkeit | Matrix-Modell (Kanal × Verkehrsträger → Obligation) | Statisch, keine Bedingungslogik |
| Entscheidungslogik | – | Nicht modellierbar. Schwellenwerte nur als Freitext |
| Change Tracking | Semantischer Diff auf Control-Ebene: neu, geändert, entfallen | – |
| Konsistenz & Redundanz | Vergleich zwischen Katalogen (Diff/Alignment) | Widerspruchserkennung noch nicht implementiert |
| Kaskade & Vererbung | ✅ OSCAL-Schichtenmodell: Catalog → Profile → Component Definition | – |
| Konformitätsprüfung | Architektonisch möglich (Profile-Vererbung), noch nicht gebaut | – |
| Schema-Validierung | ✅ NIST JSON Schema, CI-fähig | – |
| Stabile IDs | ✅ Kapitel-basiert, semantisch | – |
| Offenheit | ✅ Apache 2.0, OSCAL selbst CC0, bestehendes Tooling-Ökosystem | – |

### Rulemapping

| Dimension | Stärke | Schwäche |
|-----------|--------|----------|
| Regelinhalt | – | Kein Verbatim-Modell. Regeltext nur als Freitext in `alttext` |
| Anwendbarkeit | – | Kein Applicability-Modell |
| Entscheidungslogik | ✅ Boolesche Operatoren (OR, AND, XOR, NAND, NOR), Negation, Baumstruktur | Schwellenwerte nur als Freitext im Knotentitel |
| Change Tracking | – | Keine Versionierung im Format, kein Diff-Tooling |
| Konsistenz & Redundanz | – | Kein Vergleich zwischen Rulemaps vorgesehen |
| Kaskade & Vererbung | – | Kein Schichtenmodell, keine Hierarchie zwischen Regelebenen |
| Konformitätsprüfung | – | Nicht vorgesehen |
| Schema-Validierung | – | Kein publiziertes Schema (XSD/JSON Schema) |
| Stabile IDs | – | Numerisch (auto-increment), nicht semantisch |
| Offenheit | RUML als offener Standard angekündigt. Builder kostenlos nutzbar | Stand heute: proprietäres Format, nicht schema-validierbar |

---

## Kernbefund

**OSCAL4Rail und Rulemapping adressieren unterschiedliche Fragen am selben Regelwerk:**

| Frage | Wer antwortet |
|-------|--------------|
| *Was* steht in der Regel? (Verbatim-Text) | OSCAL4Rail |
| *Für wen* gilt sie? (Kanal, Verkehrsträger, Obligation) | OSCAL4Rail |
| *Wie bindend* ist sie? (verbindlich/empfohlen) | OSCAL4Rail |
| *Was hat sich geändert?* (Diff Version A → B) | OSCAL4Rail |
| *Wie hängen Regeln hierarchisch zusammen?* (EU → Tochter) | OSCAL4Rail |
| *Widerspricht Umsetzung X der Oberregel?* | OSCAL4Rail (geplant) |
| *Unter welchen Bedingungen* gilt die Regel? | **Rulemapping** |
| *Welche Ausnahmen* gibt es? | **Rulemapping** |
| *Ist mein konkreter Fall betroffen?* (Entscheidungspfad) | **Rulemapping** |

### Wichtig: Nicht jede Regel braucht einen Entscheidungsbaum

Viele Regeln sind einfache, binäre Aussagen:
- „Code muss in Git öffentlich lesbar abgelegt werden."
- „Architekturentscheidungen müssen dokumentiert und veröffentlicht sein."
- „Systeme müssen gepatcht werden."

Für solche Regeln ist OSCAL4Rail mit `statement` + `obligation` ausreichend. Rulemapping bringt **nur dort Mehrwert**, wo es tatsächlich Bedingungslogik gibt (Schwellenwerte, Ausnahmen, kontextabhängige Anwendbarkeit).

Der BS-KI 2.1 Pilot-Test (mit Schwellenwert ≥800 Fahrgäste und mehrdimensionaler Applicability) ist ein *komplexer* Fall – kein universeller Blueprint.

---

## Entscheidung

**OSCAL4Rail ist das tragende Rückgrat. Rulemapping ist eine optionale Ergänzung für Regeln mit komplexer Entscheidungslogik.**

```
┌────────────────────────────────────────────────────────────┐
│                    OSCAL4Rail (immer)                        │
│                                                             │
│  Catalog ──→ Profile ──→ Component Definition               │
│  (EU/TSI)    (DB Konzern)  (DB Systel / DB InfraGO)        │
│                                                             │
│  Jeder Control:                                             │
│  ├── statement (Verbatim)                                   │
│  ├── props (Applicability, Obligation)                      │
│  ├── diff (Change Tracking über Git)                        │
│  └── link rel="decision-logic" ──┐  (nur wenn nötig)       │
│                                   │                         │
│  ┌────────────────────────────────▼──────────────────┐     │
│  │  Rulemapping (optional, bei komplexer Logik)       │     │
│  │  Entscheidungsbaum: Bedingungen, Ausnahmen,        │     │
│  │  Schwellenwerte, invertierte Pfade                 │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────┘
```

### Technische Integration

```yaml
# Einfache Regel – kein Rulemapping nötig
controls:
  - id: db-ril-sec-4.2
    title: "Code-Ablage"
    parts:
      - name: statement
        prose: "Code muss in Git öffentlich lesbar in der DB abgelegt werden."
    props:
      - name: applicability
        value: verbindlich
        class: alle-systeme

# Komplexe Regel – Rulemapping als Ergänzung
controls:
  - id: bs-ki-2.1
    title: "Aktuelle Uhrzeit"
    parts:
      - name: statement
        prose: "Bei Haltestellen mit weniger als 800 Ein- und Aussteigern..."
    props:
      - name: applicability
        value: verbindlich
        class: haltestelle.bahn
    links:
      - href: "rulemaps/bs-ki-2.1.xml"
        rel: "decision-logic"
        text: "Entscheidungsbaum: Anwendbarkeitsbedingungen"
```

---

## Konsequenzen

### Positiv

- OSCAL4Rail bleibt einfach und schlank für die Mehrheit aller Regeln
- Entscheidungslogik wird nur dort hinzugefügt, wo sie tatsächlich existiert (YAGNI)
- Die Regulierungskaskade (EU → Tochter) wird durch OSCAL4Rail's Schichtenmodell getragen – etwas das Rulemapping nicht kann
- Change Tracking über Versionen bleibt Git-basiert und deterministisch
- Beide Ansätze bleiben unabhängig nutzbar (lose Kopplung über `link`)
- Attraktiv für SPRIND: konkreter sektoraler Integrationsfall

### Negativ / Risiken

- Rulemapping-Format ist proprietär und nicht schema-validierbar → Mitigation: auf RUML-Publikation warten oder eigenes XSD definieren
- Doppelte Pflege bei komplexen Regeln (Text in OSCAL4Rail, Logik in Rulemap) → Mitigation: Rulemap ist optional, OSCAL4Rail bleibt SSOT für den Regeltext
- Numerische IDs in Rulemap erschweren stabile Referenzierung → Mitigation: Dateinamen-Konvention `rulemaps/<control-id>.xml`

### Offen / noch zu klären

- Wird RUML als offener Standard publiziert? (Monitoring)
- Wie verhält sich die Integration bei Katalog-Updates? (Prozess definieren)
- Konformitätsprüfung über Kaskaden-Ebenen: wie konkret implementieren?
- Konsistenz-/Widerspruchserkennung zwischen Katalogen: wie konkret implementieren?

---

## Betrachtete Alternativen

### Alternative 1: Nur OSCAL4Rail (kein Rulemapping)

- (+) Einfacher, keine externe Abhängigkeit
- (-) Entscheidungslogik und Bedingungen nicht modellierbar
- (-) Agent muss Freitext interpretieren für „Gilt diese Regel für mich?"
- **Bewertung:** Für die Mehrheit der Regeln ausreichend. Für komplexe Regeln fehlt die Logik-Schicht.

### Alternative 2: Entscheidungslogik direkt in OSCAL4Rail modellieren

- (+) Alles in einem Format
- (-) NIST OSCAL Catalog hat kein Logik-Modell (erfordert Custom-Extensions)
- (-) Breaking Change zum OSCAL-Standard
- (-) Vermischung von Daten und Logik (verletzt IOSP-Prinzip)
- **Verworfen:** Widerspricht der OSCAL-Philosophie und dem Prinzip der Verantwortungstrennung.

### Alternative 3: DMN (Decision Model and Notation, OMG/ISO 19510)

- (+) Offener Standard, etabliertes Tooling (Camunda, Drools)
- (+) Formale Entscheidungstabellen mit Datentypen
- (-) Komplex, schwergewichtig
- (-) Kein Bezug zu Law-as-Code/SPRIND-Ökosystem
- **Vorgemerkt als Fallback** falls Rulemapping-Format dauerhaft proprietär bleibt.

### Alternative 4: Catala (funktionale Rechtssprache, INRIA)

- (+) Open Source, akademisch fundiert, formale Semantik
- (-) Programmiersprache → Juristen/Fachexperten können nicht damit arbeiten
- (-) Andere Zielgruppe, kein SPRIND-Bezug
- **Vorgemerkt als technische Alternative** für Zukunft.

---

## Validierung

Pilot-Test durchgeführt am 2026-06-25:
- BS-KI 2.1 „Aktuelle Uhrzeit" als Rulemap modelliert (komplexer Fall mit Schwellenwert)
- Import/Export im Builder erfolgreich
- Boolesche Logik (OR/AND) + Negation (`invertlogic`) funktional
- Ergebnisse dokumentiert in `docs/experiments/rulemapping/`

---

## Links

- [ADR-005: Relationship to Law-as-Code Initiatives](ADR-005-law-as-code-relationship.md)
- [Experiment: Rulemapping Builder Pilot](../experiments/rulemapping-pilot.md)
- [Experiment: Export-Analyse](../experiments/rulemapping/README.md)
- [SPRIND Law-as-Code](https://sprind.org/en/actions/strategic-projects/law-as-code)
- [Rulemapping Builder](https://builder.rulemapping.org)
- [NIST OSCAL](https://pages.nist.gov/OSCAL/)
