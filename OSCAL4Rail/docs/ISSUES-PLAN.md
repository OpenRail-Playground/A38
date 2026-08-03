# OSCAL4Rail – Issue Plan

> Vorlage für GitHub Issues + Project Board.
> Jede Sektion = ein Issue. Labels und Milestones in Klammern.

---

## GitHub Project Setup

1. Repository: `OpenRailAssociation/oscal4rail` (oder aktuell `OpenRail-Playground`)
2. Project anlegen: Settings → Projects → "New Project" → Board layout
3. Spalten: `Backlog` | `Ready` | `In Progress` | `Review` | `Done`
4. Labels erstellen:

| Label | Farbe | Beschreibung |
|-------|-------|--------------|
| `layer:catalog` | 🔵 blau | Layer 1: Catalog |
| `layer:rules` | 🟢 grün | Layer 2: Rules |
| `layer:change` | 🟠 orange | Layer 3: Change Impact |
| `layer:assessment` | 🟣 lila | Layer 4: Assessment |
| `layer:cascade` | 🔴 rot | Regulatory Cascade (cross-layer: Catalog + Assessment) |
| `type:spec` | ⬜ grau | Spezifikation/Schema |
| `type:tooling` | 🟤 braun | CLI/Tooling |
| `type:docs` | 📄 weiß | Dokumentation |
| `type:example` | 🟡 gelb | Beispiel-Implementierung |
| `priority:high` | 🔴 rot | Hohe Priorität |
| `priority:medium` | 🟠 orange | Mittlere Priorität |
| `opencode` | 🏛️ | Bezug zu OpenCode/Law-as-Code |

5. Milestones:

| Milestone | Ziel |
|-----------|------|
| `v0.1.1 – Catalog Profile` | Layer 1 Railway-Profil formalisiert |
| `v0.2.0 – Rules Layer` | Layer 2 spezifiziert + Beispiel |
| `v0.3.0 – Change Layer` | Layer 3 spezifiziert + Tooling |
| `v0.4.0 – Assessment Layer` | Layer 4 spezifiziert + Beispiel |
| `v1.0.0 – Framework Release` | Alle 4 Layer stabil, Doku komplett |

---

## Phase 0: Catalog Layer Formalisierung (Milestone v0.1.1)

### Issue #22: Catalog Layer – Railway Profile Spezifikation

**Title:** `spec: Formalize OSCAL4Rail Catalog Profile (Layer 1 – Railway-specific conventions)`
**Labels:** `layer:catalog`, `type:spec`, `priority:high`
**Milestone:** `v0.1.1 – Catalog Profile`

**Description:**

Layer 1 (Catalog) funktioniert bereits (BS-KI Beispiel validiert gegen NIST Schema), aber die **railway-spezifischen Konventionen** sind noch nicht als formale Spezifikation dokumentiert:
- Wie werden IDs vergeben? (Kapitel-basiert)
- Wie wird Applicability modelliert? (props mit class)
- Was ist das Multilingual-Modell?
- Was sind die Pflichtfelder über NIST OSCAL hinaus?

**Acceptance Criteria:**
- [ ] `docs/reference/catalog-format.md` – Vollständige Spezifikation des Railway Profile
- [ ] ID-Schema dokumentiert (Konvention: `<regulation>-<chapter.section>[-<context>]`)
- [ ] Applicability-Modell spezifiziert (channel × transport × obligation)
- [ ] Multilingual-Strategie (ein File pro Sprache, Linking-Konvention)
- [ ] Pflichtfelder über NIST OSCAL hinaus (source-chapter, source-document, etc.)
- [ ] Verbatim-Quoting als harte Invariante dokumentiert

---

### Issue #23: Catalog Layer – OSCAL4Rail Profile Schema (Constraints über NIST)

**Title:** `feat: Create oscal4rail-catalog-profile.schema.json (additional constraints)`
**Labels:** `layer:catalog`, `type:spec`, `priority:medium`
**Milestone:** `v0.1.1 – Catalog Profile`
**Depends on:** #22

**Description:**

Ein JSON Schema das die OSCAL4Rail-spezifischen Constraints **über** dem NIST OSCAL Schema definiert. NIST validiert die Struktur, dieses Schema validiert die Railway-Konventionen.

**Acceptance Criteria:**
- [ ] `schemas/oscal4rail-catalog-constraints.schema.json`
- [ ] Prüft: ID-Format (regex), required props (source-chapter, source-document)
- [ ] Prüft: Applicability-props haben gültige class-Werte
- [ ] `tools/validate.py` nutzt beide Schemas (NIST + OSCAL4Rail Constraints)
- [ ] BS-KI Beispiel validiert gegen beide

---

### Issue #24: Catalog Layer – Validator erweitern (Railway-Constraints)

**Title:** `feat: Extend validate.py with OSCAL4Rail-specific checks`
**Labels:** `layer:catalog`, `type:tooling`, `priority:medium`
**Milestone:** `v0.1.1 – Catalog Profile`
**Depends on:** #23

**Description:**

Aktuell validiert `validate.py` nur gegen NIST OSCAL JSON Schema. Erweitern um:
- OSCAL4Rail ID-Format prüfen
- Pflicht-props prüfen
- Applicability-Vollständigkeit prüfen (keine leeren class-Werte)
- Verbatim-Quoting: statement-parts dürfen nicht leer sein

**Acceptance Criteria:**
- [ ] `tools/validate.py --strict` prüft Railway-Constraints zusätzlich
- [ ] Klare Fehlermeldungen bei Verletzungen
- [ ] Exitcode ≠ 0 bei Fehlern (CI-fähig)

---

### Issue #25: Catalog Layer – Zweites Beispiel (TSI Telematics, minimal)

**Title:** `example: Minimal TSI Telematics extract (5-10 controls) to prove generality`
**Labels:** `layer:catalog`, `type:example`, `priority:low`
**Milestone:** `v0.1.1 – Catalog Profile`
**Depends on:** #22

**Description:**

Ein zweites, minimales Katalog-Beispiel beweist, dass das Format über BS-KI hinaus funktioniert. 5-10 Controls aus der EU TSI Telematics reichen.

**Acceptance Criteria:**
- [ ] `catalogs/tsi-tat/en/tsi-tat-en.yaml` – minimal, 5-10 Controls
- [ ] Validiert gegen NIST + OSCAL4Rail Constraints
- [ ] Zeigt: anderes Applicability-Modell (EU-weit, andere Channels)
- [ ] Zeigt: englischsprachiger Katalog (Multilingual-Beweis)

---

## Phase 1: Rules Layer (Milestone v0.2.0)

### Issue #1: Rules Layer Spezifikation

**Title:** `spec: Define Rules Layer format (Layer 2 – Applicability & Decision Logic)`
**Labels:** `layer:rules`, `type:spec`, `priority:high`
**Milestone:** `v0.2.0 – Rules Layer`

**Description:**

Define the OSCAL4Rail Rules Layer specification that answers: "Which controls apply to MY context?"

**Acceptance Criteria:**
- [ ] `docs/reference/rules-format.md` – Prose specification
- [ ] Schema covers: context filters, threshold conditions, obligation overrides
- [ ] Clear interface definition to Rulemapping/OpenCode (how to reference external decision trees)
- [ ] Distinction: simple rules (YAML inline) vs. complex rules (external Rulemapping reference)
- [ ] At least 2 examples in the spec

**Context:**
- Existing concept: `KONZEPT-RULEMAPPING.md` (from DB implementation)
- ADR-006: Rulemapping complement, not competition
- OpenCode interface: when a legislator publishes via OpenCode, Rules Layer can reference it

---

### Issue #2: Rules Layer JSON Schema

**Title:** `feat: Create oscal4rail-rules.schema.json`
**Labels:** `layer:rules`, `type:spec`, `priority:high`
**Milestone:** `v0.2.0 – Rules Layer`
**Depends on:** #1

**Description:**

Implement the JSON Schema for the Rules Layer based on the specification from #1.

**Acceptance Criteria:**
- [ ] `schemas/oscal4rail-rules.schema.json` exists and is valid JSON Schema (Draft 7 or 2020-12)
- [ ] Covers: rule conditions, context variables, obligation outcomes, AMC references
- [ ] Supports linking to external decision logic (Rulemapping XML, OpenCode artifacts)
- [ ] `tools/validate.py` extended to validate Rules files
- [ ] CI validates all example Rules files

---

### Issue #3: AMC (Acceptable Means of Compliance) Schema

**Title:** `feat: Define AMC format – "HOW to comply"`
**Labels:** `layer:rules`, `type:spec`, `priority:medium`
**Milestone:** `v0.2.0 – Rules Layer`

**Description:**

AMCs answer "How do I concretely fulfill this control?" – tool links, reference implementations, step-by-step guidance. This is the actionable counterpart to abstract controls.

**Acceptance Criteria:**
- [ ] `docs/reference/amc-format.md` – Specification
- [ ] Schema: `schemas/oscal4rail-amc.schema.json`
- [ ] AMCs can be attached to controls (inline or separate file)
- [ ] AMC format is provider-agnostic (works for EA, Security, Operations)
- [ ] Example: AMC for BS-KI 2.1

---

### Issue #4: Rules Layer Example – BS-KI Applicability

**Title:** `example: BS-KI 2.1 Applicability Rule (threshold + channel logic)`
**Labels:** `layer:rules`, `type:example`, `priority:medium`
**Milestone:** `v0.2.0 – Rules Layer`
**Depends on:** #2

**Description:**

Create a working example of the Rules Layer using BS-KI 2.1 (the Rulemapping pilot case).

**Acceptance Criteria:**
- [ ] `examples/rules/bs-ki-2.1-applicability.yaml` – valid against schema
- [ ] Demonstrates: threshold condition (≥800 passengers), channel×transport logic
- [ ] References the Rulemapping XML from the pilot (`rulemaps/bs-ki-2.1.xml`)
- [ ] Validates with `tools/validate.py`

---

### Issue #5: OpenCode/Rulemapping Interface Definition

**Title:** `spec: Define interface to OpenCode and Rulemapping artifacts`
**Labels:** `layer:rules`, `type:spec`, `opencode`, `priority:high`
**Milestone:** `v0.2.0 – Rules Layer`

**Description:**

Formally define how OSCAL4Rail references external decision logic from:
- OpenCode (SPRIND Law-as-Code, future official legal code)
- Rulemapping (RUML format, XML decision trees)
- Other rule engines (DMN, Catala – as fallback)

**Acceptance Criteria:**
- [ ] `docs/reference/external-rules-interface.md`
- [ ] Link format in OSCAL4Rail controls (`links[rel="decision-logic"]`)
- [ ] Supported `rel` types defined: `decision-logic`, `legal-source`, `amc`
- [ ] Versioning: how to pin a specific version of an external rule artifact
- [ ] Example: BS-KI 2.1 control referencing Rulemapping XML

---

## Phase 2: Change Impact Layer (Milestone v0.3.0)

### Issue #6: Change Impact Spezifikation

**Title:** `spec: Define Change Impact Layer format (Layer 3 – What changed?)`
**Labels:** `layer:change`, `type:spec`, `priority:high`
**Milestone:** `v0.3.0 – Change Layer`

**Description:**

Define the format for structured change notifications when a catalog version changes.

OSCAL has NO built-in concept for "what changed between version N and N+1 at control level". This is the core USP of OSCAL4Rail Layer 3.

**Acceptance Criteria:**
- [ ] `docs/reference/change-format.md` – Specification
- [ ] Change categories defined: `added`, `removed`, `tightened`, `relaxed`, `replaced`, `content-changed`
- [ ] Impact model: change → affected systems/contexts → required action
- [ ] Machine-readable change notification (not just a prose changelog)
- [ ] Relationship to Git diff (tooling can derive change notifications from git history)

---

### Issue #7: Change Impact JSON Schema

**Title:** `feat: Create oscal4rail-change.schema.json`
**Labels:** `layer:change`, `type:spec`, `priority:high`
**Milestone:** `v0.3.0 – Change Layer`
**Depends on:** #6

**Description:**

JSON Schema for structured change notifications.

**Acceptance Criteria:**
- [ ] `schemas/oscal4rail-change.schema.json`
- [ ] Covers: source version, target version, list of changes per control
- [ ] Each change has: control-id, change-type, old-value, new-value, impact-assessment
- [ ] Optional: affected-systems field (for implementations that can link to asset inventories)
- [ ] Validates example change notifications

---

### Issue #8: Diff Tooling – Structured Change Notifications

**Title:** `feat: tools/diff.py – Generate structured change notifications from catalog versions`
**Labels:** `layer:change`, `type:tooling`, `priority:medium`
**Milestone:** `v0.3.0 – Change Layer`
**Depends on:** #7

**Description:**

Extend `tools/diff.py` to produce machine-readable change notifications (not just human-readable text).

**Acceptance Criteria:**
- [ ] `tools/diff.py old.yaml new.yaml --output change-notification.yaml`
- [ ] Output validates against `oscal4rail-change.schema.json`
- [ ] Categorizes changes correctly (added/removed/tightened/relaxed/content-changed)
- [ ] Human-readable summary (--format text) also available
- [ ] Test: BS-KI v1.0 vs. simulated v2.0

---

### Issue #9: Change Impact Example – Simulated BS-KI Version Update

**Title:** `example: Simulated BS-KI v1.0 → v2.0 change notification`
**Labels:** `layer:change`, `type:example`, `priority:medium`
**Milestone:** `v0.3.0 – Change Layer`
**Depends on:** #8

**Description:**

Create a simulated version update of BS-KI and demonstrate the Change Impact Layer in action.

**Acceptance Criteria:**
- [ ] `examples/change/bs-ki-v1-to-v2.yaml` – valid change notification
- [ ] Demonstrates: new control, removed control, tightened obligation, relaxed condition
- [ ] Shows how an implementation could derive "affected systems" from this
- [ ] Documented in `docs/examples/` as a walkthrough

---

## Phase 3: Assessment Layer (Milestone v0.4.0)

### Issue #10: Assessment Layer Spezifikation

**Title:** `spec: Define Assessment Layer format (Layer 4 – Am I compliant?)`
**Labels:** `layer:assessment`, `type:spec`, `priority:high`
**Milestone:** `v0.4.0 – Assessment Layer`

**Description:**

Define the OSCAL4Rail Railway Assessment Profile. OSCAL already has Assessment Results – we define the railway-specific profile for governance assessments.

**Acceptance Criteria:**
- [ ] `docs/reference/assessment-format.md` – Specification
- [ ] Railway-specific assessment scales (e.g. vollständig/teilweise/nicht erfüllt)
- [ ] Assessment Plan template (what to check, how to check)
- [ ] Assessment Result template (findings, recommendations, compliance status)
- [ ] Relationship to OSCAL Assessment Results model (profile, not fork)
- [ ] Support for automated assessment (AI agents) and manual assessment (humans)

---

### Issue #11: Assessment Layer JSON Schema

**Title:** `feat: Create oscal4rail-assessment.schema.json (Railway Profile)`
**Labels:** `layer:assessment`, `type:spec`, `priority:high`
**Milestone:** `v0.4.0 – Assessment Layer`
**Depends on:** #10

**Description:**

JSON Schema for railway-specific assessments.

**Acceptance Criteria:**
- [ ] `schemas/oscal4rail-assessment.schema.json`
- [ ] Extends/profiles NIST OSCAL Assessment Results
- [ ] Railway assessment scales and methodology
- [ ] Validates example assessment results
- [ ] Compatible with both human and automated assessments

---

### Issue #12: Assessment Example – BS-KI Compliance Check

**Title:** `example: Assessment of a fictional railway system against BS-KI catalog`
**Labels:** `layer:assessment`, `type:example`, `priority:medium`
**Milestone:** `v0.4.0 – Assessment Layer`
**Depends on:** #11

**Description:**

Demonstrate the Assessment Layer with a fictional railway information system assessed against the BS-KI catalog.

**Acceptance Criteria:**
- [ ] `examples/assessment/fictional-system-bs-ki.yaml`
- [ ] Shows: 3 controls fully met, 1 partially met, 1 not met
- [ ] Includes findings and recommended actions
- [ ] Validates against schema
- [ ] Walkthrough in `docs/examples/`

---

## Phase 4: Framework Release (Milestone v1.0.0)

### Issue #13: CLI Tool – `oscal4rail`

**Title:** `feat: Unified CLI tool – oscal4rail validate|diff|assess|rules`
**Labels:** `type:tooling`, `priority:medium`
**Milestone:** `v1.0.0 – Framework Release`

**Description:**

Single CLI entry point for all OSCAL4Rail operations.

**Acceptance Criteria:**
- [ ] `oscal4rail validate <file>` – validate any OSCAL4Rail artifact
- [ ] `oscal4rail diff <old> <new>` – structured change notification
- [ ] `oscal4rail rules <catalog> --context <context>` – filter applicable controls
- [ ] `oscal4rail assess <catalog> <system-profile>` – generate assessment template
- [ ] Installable via pip (`pip install oscal4rail`)
- [ ] --help for all subcommands

---

### Issue #14: CI/CD Pipeline (GitHub Actions)

**Title:** `chore: GitHub Actions – validate all schemas and examples on every PR`
**Labels:** `type:tooling`, `priority:medium`
**Milestone:** `v1.0.0 – Framework Release`

**Description:**

Continuous validation of all OSCAL4Rail artifacts.

**Acceptance Criteria:**
- [ ] `.github/workflows/validate.yml`
- [ ] Validates: all catalogs, all rules, all change notifications, all assessments
- [ ] Runs on every PR and push to main
- [ ] Badge in README
- [ ] Fails fast with clear error messages

---

### Issue #15: Framework Documentation – "Why OSCAL4Rail > OSCAL"

**Title:** `docs: Complete framework documentation – 4 layers, USP, OpenCode relationship`
**Labels:** `type:docs`, `priority:high`
**Milestone:** `v1.0.0 – Framework Release`

**Description:**

Update arc42 and create a clear "Why OSCAL4Rail" page that explains the 4-layer architecture and why it's more than just OSCAL.

**Acceptance Criteria:**
- [ ] `docs/arc42.md` updated with all 4 layers
- [ ] `docs/why-oscal4rail.md` – clear comparison table (OSCAL vs. OSCAL4Rail)
- [ ] `docs/opencode-integration.md` – how OSCAL4Rail relates to OpenCode/Law-as-Code
- [ ] Each layer has its own reference page under `docs/reference/`
- [ ] Diagram: 4-layer architecture (Mermaid or ASCII)

---

### Issue #16: Regulatory Cascade Model (Railway USP)

**Title:** `spec: Formalize Regulatory Cascade Model (6–7 levels, conformance constraints, impact propagation)`
**Labels:** `layer:cascade`, `type:spec`, `priority:high`
**Milestone:** `v0.1.1 – Catalog Profile`

**Description:**

The Regulatory Cascade is the defining railway-specific innovation — the reason it's "4Rail" and not just "OSCAL+". Formalize how OSCAL4Rail models the inheritance/specialization hierarchy across 6–7 levels:

```
International → EU → National → Agency → Industry → Company → System/Team
```

Key constraints:
- Each level may only specialize, never contradict its parent (conformance downward)
- Changes cascade: when a parent changes, all children must adapt
- Impact propagates: which downstream catalogs/systems are affected by an upstream change?
- Cross-border: parallel cascade branches share a common parent (e.g. DE and CH both implement same TSI)
- Multimodal: regulations cover rail, bus, tram, cable cars, ships
- Multi-domain: vehicles, infrastructure, procurement, maintenance, passenger information

This touches both the **Catalog schema** (how to express parent-child relationships between catalogs) and the **Assessment schema** (conformance checking: "Is child still conformant to parent?").

**Acceptance Criteria:**
- [ ] `docs/reference/cascade-model.md` – Specification
- [ ] Catalog schema: `parent-catalog` reference field (link to upstream catalog)
- [ ] Cascade levels taxonomy defined (International, EU, National, Agency, Industry, Company, System)
- [ ] Conformance constraint model: what "must not contradict" means formally
- [ ] Impact propagation concept: upstream change → which downstream catalogs affected?
- [ ] Cross-border model: parallel branches sharing a common EU parent
- [ ] Example: ISO 27001 → EU TSI → CH LEisenbG → BS-KI → SBB internal standard
- [ ] Integration with Assessment Layer: conformance as an assessable property

---

### Issue #17: ADR-007 – Framework Scope Decision

**Title:** `docs: ADR-007 – OSCAL4Rail Framework Scope (what's in, what's out)`
**Labels:** `type:docs`, `priority:high`
**Milestone:** `v0.2.0 – Rules Layer`

**Description:**

Formal architecture decision: What is part of the OSCAL4Rail framework (schemas, tooling, examples) vs. what is an implementation (specific catalogs, company rules).

**Acceptance Criteria:**
- [ ] `docs/adr/ADR-007-framework-scope.md`
- [ ] Clear boundary: Framework ≠ Content
- [ ] DB catalogs are explicitly NOT part of the framework
- [ ] Framework provides: schemas, validators, tooling, example catalogs (BS-KI)
- [ ] Implementations provide: actual catalogs, rules, assessments

---

## Backlog (ungeplant, aber bekannt)

### Issue #18: Multilingual Catalog Linking

**Title:** `feat: Cross-language consistency checking (OSCAL Control Mapping)`
**Labels:** `layer:catalog`, `type:spec`

---

### Issue #19: SPRIND/OpenCode Contact & Alignment

**Title:** `chore: Contact SPRIND initiative – present OSCAL4Rail as sectoral implementation`
**Labels:** `opencode`, `type:docs`

---

### Issue #20: ERA/EBA Engagement

**Title:** `chore: Engage ERA/EBA via OpenRail for machine-readable railway regulations`
**Labels:** `opencode`, `type:docs`

---

### Issue #21: Second Catalog – TSI Telematics

**Title:** `feat: Extract EU TSI Telematics regulation as OSCAL4Rail catalog`
**Labels:** `layer:catalog`, `type:example`

---

## Zusammenfassung: Reihenfolge

```
v0.1.1 (Catalog Profile + Cascade)
  #16 Regulatory Cascade Model (Railway USP) ──▶ feeds into #22 and #11
  #22 Catalog Railway Profile Spec ──▶ #23 Constraints Schema ──▶ #24 Validator
                                   └──▶ #25 TSI Example (minimal)

v0.2.0 (Rules Layer)
  #17 ADR-007 Framework Scope ──┐
  #1  Rules Spec ───────────────┼──▶ #2 Rules Schema ──▶ #4 Example
  #5  OpenCode Interface ───────┘    #3 AMC Schema
                                          
v0.3.0 (Change Layer)
  #6 Change Spec ──▶ #7 Change Schema ──▶ #8 Diff Tooling ──▶ #9 Example

v0.4.0 (Assessment Layer)
  #10 Assessment Spec ──▶ #11 Assessment Schema (incl. cascade conformance) ──▶ #12 Example

v1.0.0 (Framework Release)
  #13 CLI Tool
  #14 CI/CD
  #15 Framework Docs
```


---

## Gap-Analyse: Fehlende NIST OSCAL Modelle (August 2026)

> Ergebnis der Analyse gegen das vollständige NIST OSCAL v1.2.1 Modell.
> OSCAL4Rail nutzt aktuell nur das Catalog Schema. Die folgenden NIST-Modelle fehlen komplett.

### Kerninsight

**Die Regulatory Cascade ist kein neues Konzept – sie ist eine Kette von OSCAL Profiles mit Control Mappings.**

Jede Cascade-Ebene (EU → National → Industry → Company) ist:
1. Ein **Profile** das Controls aus dem Upstream-Catalog selektiert/spezialisiert
2. Ein **Control Mapping** das die Beziehung zum Upstream formalisiert

Statt ein komplett neues Cascade-Modell zu definieren, können die bestehenden NIST-Mechanismen genutzt werden. Railway-spezifische Conformance-Constraints als Extension (`props` mit Namespace `ns="https://github.com/OpenRailAssociation/oscal4rail/ns"`).

### NIST OSCAL Modelle – Status in OSCAL4Rail

| NIST OSCAL Modell | Layer | Status | Rail-Priorität |
|---|---|---|---|
| Catalog | Control | ✅ Implementiert | – |
| **Profile** | Control | ❌ Fehlt | 🔴 Kritisch |
| **Control Mapping** | Control | ❌ Fehlt | 🔴 Hoch |
| Component Definition | Implementation | ❌ Fehlt | 🟠 Mittel |
| System Security Plan (SSP) | Implementation | ❌ Fehlt | 🟡 Niedrig |
| **Assessment Plan** | Assessment | ❌ Fehlt | 🟠 Hoch |
| **Assessment Results** | Assessment | ❌ Fehlt | 🟠 Hoch |
| POA&M | Assessment | ❌ Fehlt | 🟡 Mittel |

### NIST-Tooling das OSCAL4Rail nutzen sollte

| Tool/Projekt | Repository | Relevanz für Rail |
|---|---|---|
| `oscal-deep-diff` | github.com/usnistgov/oscal-deep-diff | Basis für Layer 3 (Change Impact) statt Eigenentwicklung |
| `oscal-cli` | github.com/usnistgov/oscal-cli | Validation, Profile Resolution, Conversion |
| `compliance-trestle` | github.com/oscal-compass/compliance-trestle | Agile Authoring, Plugin-Architektur, **MCP-Server** |
| `compliance-trestle-mcp` | github.com/oscal-compass/compliance-trestle-mcp | AI-Agent-Interface (genau OSCAL4Rail Vision) |
| OSCAL Content | github.com/usnistgov/oscal-content | Beispiele für Profile, SSP, Assessment Results |

### Evaluierungsergebnisse (2026-08-03)

**compliance-trestle v4.2.0** – ✅ Empfohlen als Tooling-Basis (→ [ADR-007](../adr/ADR-007-tooling-foundation.md))

- Import BS-KI Catalog: ✅ funktioniert (YAML + JSON)
- Validate gegen OSCAL 1.2.1 Schema: ✅ funktioniert
- Profile Resolution: ✅ funktioniert (Subset-Selektion + resolved Catalog)
- Workspace-Struktur: alle 8 OSCAL-Modelltypen vorbereitet
- Plugin-Architektur: FedRAMP als Referenz für `trestle-oscal4rail`

**oscal-deep-diff v1.0.0** – ✅ Empfohlen als Layer-3-Basis

- Erkennt Textänderungen: ✅ (800 → 500 in bs-ki-2.1)
- Erkennt Obligation-Verschärfungen: ✅ (empfohlen → verbindlich)
- Erkennt neue Controls: ✅ (bs-ki-2.99 als rightOnly)
- Performance: 7ms für 42 Controls
- Config-Aufwand: 15 Zeilen YAML für OSCAL Catalog
- Output: JSON mit JSON-Pointern, maschinenlesbar

**NIST OSCAL Schemas v1.2.1** – ✅ Importiert

Alle 4 relevanten Schemas lokal verfügbar (`/work/beta/oscal-schemas/schemas/`):
- `oscal-profile.json` (68 KB)
- `oscal-mapping.json` (67 KB)
- `oscal-assessment-results.json` (152 KB)
- `oscal-component-definition.json` (82 KB)

---

### Issue #26: Profile Schema importieren + Cascade-als-Profile-Kette

**Title:** `feat: Import OSCAL Profile Schema – model Regulatory Cascade as Profile chain`
**Labels:** `layer:catalog`, `layer:cascade`, `type:spec`, `priority:high`
**Milestone:** `v0.1.1 – Catalog Profile`

**Description:**

Das NIST OSCAL Profile-Modell ist der natürliche Mechanismus für die Regulatory Cascade. Ein Profile selektiert Controls aus einem Upstream-Catalog und kann sie spezialisieren (Parameter setzen, Guidance ergänzen) – genau was jede Cascade-Ebene tut.

Statt ein eigenständiges Cascade-Modell zu erfinden (#16), die Cascade als Kette von OSCAL Profiles modellieren:
- EU TSI Catalog → CH National Profile (selektiert + verschärft)
- CH National Profile → BS-KI Catalog (Industry-Level)  
- BS-KI Catalog → SBB Profile (selektiert Subset für eigene Systeme)

Railway-spezifische Extensions (Conformance-Constraints, Impact-Propagation) als Props mit eigenem Namespace.

**Acceptance Criteria:**
- [ ] `schemas/oscal-profile.json` – NIST OSCAL Profile Schema v1.2.1 importiert
- [ ] `docs/reference/cascade-as-profiles.md` – Konzept: Cascade = Profile-Kette
- [ ] `examples/profiles/sbb-subset-bs-ki.yaml` – SBB selektiert 20 von 42 BS-KI Controls
- [ ] Profile Resolution funktioniert (resolved Profile = neuer Catalog)
- [ ] Railway-Extension Props definiert: `cascade-level`, `conformance-constraint`, `parent-catalog-ref`
- [ ] ADR: Warum Profile statt eigenem Cascade-Schema
- [ ] Validierung mit `oscal-cli` oder eigener `validate.py`

**Beziehung zu #16:** Ersetzt den Custom-Ansatz aus #16 durch Nutzung des NIST-Standards. #16 wird zu einer Spezifikation der Railway-Extensions innerhalb des Profile-Modells.

---

### Issue #27: Control Mapping Schema importieren (v1.2.1)

**Title:** `feat: Import OSCAL Control Mapping Schema – cross-framework relationships`
**Labels:** `layer:catalog`, `type:spec`, `priority:high`
**Milestone:** `v0.1.1 – Catalog Profile`

**Description:**

Das OSCAL Control Mapping Modell (ab v1.2.0) beschreibt Beziehungen zwischen Controls aus verschiedenen Frameworks. Exakt das, was Rail für Cross-Border und Multilingual braucht:
- BS-KI 2.1 (CH) ↔ TSI TAT 4.2.1 (EU) – gleiche Anforderung, verschiedene Frameworks
- BS-KI DE ↔ BS-KI FR – gleiche Regelung, verschiedene Sprachen
- ISO 27001 A.8.1 ↔ interner Standard – Abdeckung nachweisen

Das Mapping hat `coverage` (0-1) und `gap-summary` – ideal für Gap-Analyse.

**Acceptance Criteria:**
- [ ] `schemas/oscal-mapping.json` – NIST OSCAL Control Mapping Schema v1.2.1
- [ ] `examples/mappings/bs-ki-de-to-fr.yaml` – Multilingual-Mapping (löst #18)
- [ ] `examples/mappings/bs-ki-to-tsi-tat.yaml` – Cross-Framework-Mapping (minimal)
- [ ] Coverage-Berechnung: wie viel Prozent des Upstream sind abgedeckt?
- [ ] Gap-Summary: welche Upstream-Controls haben kein Mapping?
- [ ] `tools/validate.py` erweitert um Mapping-Validierung

**Beziehung zu #18:** Löst #18 (Multilingual Catalog Linking) als Spezialfall von Control Mapping.

---

### Issue #28: Assessment Results Schema importieren + Railway-Profil

**Title:** `feat: Import OSCAL Assessment Results Schema – railway assessment scales`
**Labels:** `layer:assessment`, `type:spec`, `priority:high`
**Milestone:** `v0.4.0 – Assessment Layer`

**Description:**

Das NIST Assessment Results Schema ist fertig spezifiziert. OSCAL4Rail muss es nicht neu erfinden, sondern als Railway-Profile nutzen. Erweiterungen:
- Railway-Bewertungsskala: `vollständig erfüllt` / `teilweise erfüllt` / `nicht erfüllt` / `nicht relevant` (statt nur satisfied/not-satisfied)
- Cascade-Conformance als assessierbares Property
- Support für AI-Agent-Assessments UND menschliche Reviews

**Acceptance Criteria:**
- [ ] `schemas/oscal-assessment-results.json` – NIST Schema v1.2.1
- [ ] `docs/reference/assessment-format.md` – Railway Assessment Profile
- [ ] Railway-Props definiert: `assessment-scale` mit 4 Werten, `assessor-type` (human/agent/hybrid)
- [ ] `examples/assessment/fictional-fis-bs-ki.yaml` – Fiktives FIS gegen BS-KI
- [ ] Zeigt: 3 Controls vollständig, 1 teilweise, 1 nicht erfüllt
- [ ] Findings referenzieren Control-IDs aus dem Catalog
- [ ] Validierung gegen NIST Schema + Railway Extensions

**Beziehung zu #10, #11, #12:** Ersetzt #10-#12 durch Nutzung des fertigen NIST Schemas mit Railway-Extension statt Neudesign.

---

### Issue #29: oscal-deep-diff als Basis für Change Layer

**Title:** `feat: Build Layer 3 (Change Impact) on top of oscal-deep-diff`
**Labels:** `layer:change`, `type:tooling`, `priority:medium`
**Milestone:** `v0.3.0 – Change Layer`

**Description:**

NIST hat mit `oscal-deep-diff` (github.com/usnistgov/oscal-deep-diff) bereits ein schema-agnostisches Diffing-Tool für OSCAL-Dokumente. Statt ein eigenes Diff-Tooling from scratch zu bauen, darauf aufsetzen und nur die Railway-spezifische semantische Interpretation ergänzen:

- oscal-deep-diff liefert: "Feld X in Control Y hat sich von A zu B geändert"
- OSCAL4Rail interpretiert: "Das ist eine Verschärfung (tightened)" oder "Das ist eine Lockerung (relaxed)"
- OSCAL4Rail propagiert: "Diese Änderung betrifft folgende Downstream-Profiles/Systeme"

**Acceptance Criteria:**
- [ ] oscal-deep-diff evaluiert und als Dependency aufgenommen (oder Subset portiert)
- [ ] `tools/diff.py` nutzt oscal-deep-diff als Backend
- [ ] Railway-Interpretation oben drauf: Kategorisierung (added/removed/tightened/relaxed/content-changed)
- [ ] Impact-Propagation: Change + Profile-Kette → betroffene Downstream-Catalogs
- [ ] Eigenes Change-Notification-Schema nur für die semantische Interpretation, nicht für das Diff selbst

**Beziehung zu #6, #7, #8:** Vereinfacht #6-#8 erheblich – der Diff-Kern existiert bereits.

---

### Issue #30: Component Definition für Railway-Systeme

**Title:** `feat: Import OSCAL Component Definition – model railway IT systems`
**Labels:** `layer:assessment`, `type:spec`, `priority:medium`
**Milestone:** `v0.4.0 – Assessment Layer`

**Description:**

Das OSCAL Component Definition Modell beschreibt, wie eine Komponente (Software, Hardware, Service) Controls erfüllt. Für Rail der Brückenschlag zwischen Catalog und Assessment:

- Ein Fahrgastinformationssystem (FIS) als Component → "erfüllt BS-KI 2.1, 2.2, 3.1-3.6"
- Eine BEAM-Anwendung als Component → verknüpft mit Railway-Profile
- Ein Fahrzeug-Display als Component → erfüllt BS-KI Fahrzeug-Controls

**Acceptance Criteria:**
- [ ] `schemas/oscal-component-definition.json` – NIST Schema v1.2.1
- [ ] `examples/components/fictional-fis.yaml` – Fiktives FIS mit Control-Satisfaction
- [ ] Mapping Component → Assessment: Component claims erfüllt → Assessment verifiziert
- [ ] Railway-Props: `system-type` (FIS, DPI, IBIS, Leitsystem), `operator` (SBB, DB, ÖBB)
- [ ] Beziehung zu Profile: Component referenziert welches Profile es erfüllen soll

---

### Issue #31: compliance-trestle Evaluierung + Plugin-Architektur

**Title:** `research: Evaluate compliance-trestle as OSCAL4Rail tooling foundation`
**Labels:** `type:tooling`, `priority:medium`
**Milestone:** Backlog

**Description:**

Das `oscal-compass/compliance-trestle`-Projekt (IBM, Open Source, Apache 2.0) bietet:
- Agile Authoring von OSCAL-Artefakten in Git
- Plugin-Architektur (FedRAMP als Beispiel-Plugin)
- MCP-Server (`compliance-trestle-mcp`) für AI-Agent-Integration
- Profile Resolution, Validation, SSP-Authoring
- Etablierte Community und Governance

Prüfen ob ein `compliance-trestle-oscal4rail`-Plugin sinnvoller ist als eigenes CLI-Tooling (#13).

**Acceptance Criteria:**
- [ ] compliance-trestle lokal installiert und getestet
- [ ] BS-KI Catalog in trestle-Workspace importiert
- [ ] FedRAMP-Plugin als Referenz für eigenes Rail-Plugin analysiert
- [ ] MCP-Server getestet (AI-Agent-Integration)
- [ ] ADR: Eigenes CLI vs. trestle-Plugin – Vor-/Nachteile
- [ ] Falls Plugin: Scope definieren (was macht das Plugin, was bleibt im Core)

---

### Konsistenzprüfung: Bestehende Issues vs. neue Gap-Issues

| Bestehend | Status nach Gap-Analyse | Begründung |
|---|---|---|
| **#16 Cascade Model** | ⚠️ Umscopen → wird Teil von #26 | Die Cascade IST eine Profile-Kette. #16 wird zur Spezifikation der Railway-Extensions (Props) innerhalb des Profile-Modells, nicht mehr ein eigenständiges Schema. |
| **#18 Multilingual Linking** | ✅ Gelöst durch #27 | Control Mapping löst das als Spezialfall: Mapping BS-KI DE ↔ BS-KI FR mit `relationship-type: equivalent`. Kein eigenes Konstrukt nötig. |
| **#10 Assessment Spec** | ⚠️ Umscopen → wird Teil von #28 | Statt eigenes Schema designen → NIST Assessment Results importieren + Railway-Props als Extension. Die *Spezifikation* (`assessment-format.md`) bleibt als Deliverable, aber basiert auf NIST. |
| **#11 Assessment Schema** | ❌ Ersetzt durch #28 | Kein eigenes `oscal4rail-assessment.schema.json` – stattdessen NIST Schema + Constraints-Schema (analog #23 für Catalog). |
| **#12 Assessment Example** | ✅ Bleibt – wird Deliverable von #28 | Acceptance Criteria identisch, nur Schema-Basis ändert sich. |
| **#6 Change Spec** | ⚠️ Reduzieren | Scope reduzieren: Nur die *semantische Interpretation* (tightened/relaxed) spezifizieren. Das Diff-Tooling selbst kommt von oscal-deep-diff (#29). |
| **#7 Change Schema** | ⚠️ Reduzieren | Schema nur für die Railway-Interpretation (Change-Notification), nicht für das Diff-Ergebnis selbst. |
| **#8 Diff Tooling** | ⚠️ Vereinfacht durch #29 | `tools/diff.py` wird Wrapper um oscal-deep-diff + Railway-Klassifikation. Kein eigener Diff-Algorithmus. |
| **#13 CLI Tool** | ⚠️ Abhängig von #31 | Falls compliance-trestle-Plugin → kein eigenes CLI nötig. Falls nicht → eigenes CLI wie geplant. Entscheidung erst nach #31. |
| **#22 Catalog Profile Spec** | ✅ Bleibt | Ergänzt sich mit #26: #22 definiert die Railway-Konventionen für Catalogs, #26 für Profiles. Beide in v0.1.1. |
| **#23 Constraints Schema** | ✅ Bleibt | Muster wird auch für Profile (#26) und Assessment (#28) angewandt: NIST-Schema + OSCAL4Rail-Constraints-Schema obendrauf. |
| **#24 Validator** | ✅ Bleibt + erweitern | `validate.py` muss zusätzlich Profile, Mapping, Assessment validieren können. |
| **#25 TSI Example** | ✅ Bleibt | Wird durch #27 wertvoller: TSI-Catalog + Mapping zu BS-KI demonstriert Cascade. |
| **#1-#5 Rules Layer** | ✅ Bleiben unverändert | Kein NIST-Äquivalent – Eigenentwicklung ist richtig. |
| **#9 Change Example** | ✅ Bleibt | – |
| **#14 CI/CD** | ✅ Bleibt | – |
| **#15 Framework Docs** | ✅ Bleibt + erweitern | Muss nun auch Profile, Mapping, Component Definition, Assessment beschreiben. |
| **#17 ADR-007 Scope** | ✅ Bleibt | Noch wichtiger: NIST-Schemas sind *importiert* (nicht geforkt), Railway-Extensions sind *eigener* Code. |
| **#19 SPRIND Contact** | ✅ Bleibt | – |
| **#20 ERA/EBA Engagement** | ✅ Bleibt | – |
| **#21 TSI Catalog** | ✅ Bleibt | Prerequisite für #27 (Mapping) und #26 (Profile-Kette). |

### Empfohlene Aktionen

1. **#16 umscopen**: Issue-Titel ändern zu "Cascade Model as OSCAL Profile Extension". Deliverables: Railway-Props-Definition + Conformance-Constraint-Logik. Kein eigenständiges Cascade-Schema mehr.
2. **#10 + #11 zusammenführen mit #28**: Ein Issue statt drei. Assessment-Spec + Schema + Railway-Extension in einem.
3. **#18 schließen als Duplikat**: Verweis auf #27 (Control Mapping löst das).
4. **#8 umscopen**: Titel ändern zu "Diff wrapper on oscal-deep-diff". Kein eigener Algorithmus.
5. **#13 als "blocked by #31" markieren**: Erst evaluieren, dann entscheiden.

---

### Angepasste Roadmap (nach Gap-Analyse)

```
v0.1.1 (Catalog Profile + Cascade) – ANGEPASST
  #26 Profile Schema importieren + Cascade-als-Profile-Kette (NEU)
  #27 Control Mapping Schema importieren (NEU)
  #16 Cascade Model → wird Railway-Extension INNERHALB #26
  #22 Catalog Railway Profile Spec ──▶ #23 ──▶ #24
  #25 TSI Example (minimal)

v0.2.0 (Rules Layer) – unverändert
  #17 ADR-007 Framework Scope
  #1  Rules Spec ──▶ #2 Rules Schema ──▶ #4 Example
  #5  OpenCode Interface
  #3  AMC Schema

v0.3.0 (Change Layer) – ANGEPASST
  #29 oscal-deep-diff als Basis (NEU – vereinfacht #6-#8)
  #6  Change Spec (reduziert auf semantische Interpretation)
  #7  Change Schema (nur Railway-Interpretation, nicht Diff selbst)
  #9  Example

v0.4.0 (Assessment Layer) – ANGEPASST
  #28 Assessment Results Schema importieren + Railway-Profil (NEU – ersetzt #10-#12)
  #30 Component Definition (NEU)

v1.0.0 (Framework Release)
  #31 compliance-trestle Evaluierung (NEU)
  #13 CLI Tool (ggf. als trestle-Plugin statt eigenem CLI)
  #14 CI/CD
  #15 Framework Docs
```
