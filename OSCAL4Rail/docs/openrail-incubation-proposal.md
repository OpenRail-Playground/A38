# OpenRail Association – Stage 1 Incubation Questionnaire
## Project: OSCAL4Rail

> **Status:** Draft – for review in meeting with Max Mehl and Cornelius Schumacher (end of July 2026)
> **Submitted by:** Jens Grote (jens.grote@deutschebahn.com)

---

## What is the project's name?

OSCAL4Rail

---

## Describe the project. What does the project do, why is it valuable, where does it come from?

OSCAL4Rail is an open standard and toolset for making railway regulations machine-readable, schema-validated, versionable, and diffable.

Railway regulations (safety rules, passenger information standards, infrastructure requirements) are scattered across thousands of PDF and Word documents. They are written as free text and interpreted individually by each reader — leading to inconsistent, non-deterministic application across organisations and countries. Changes between versions are invisible at the rule level.

OSCAL4Rail solves this by:
- Extending the **NIST OSCAL** standard (public domain, CC0 1.0) with a **railway-specific profile** — additional schema constraints, ID conventions, applicability model
- Defining a **4-layer framework**: (1) Catalog — machine-readable regulations, (2) Rules — applicability logic using **Rulemapping** methodology (which controls apply in which context), (3) Change Impact — what changed between versions, (4) Assessment — compliance verification by humans or AI agents
- Embracing **Law-as-Code** principles: regulations are code — versioned, diffable, testable, deployable
- **Future-ready for OpenCode/SPRIND**: Railway regulation bodies (ERA, EBA, BAV) currently publish as PDF only. When the SPRIND Law-as-Code initiative establishes machine-readable publication formats, OSCAL4Rail is designed to consume them as authoritative upstream source — replacing today's PDF extraction pipeline
- Requiring **verbatim quotes** from source documents — no paraphrasing, no interpretation
- Giving every rule a **stable identifier** derived from the chapter number (not the page number)
- Providing **one public example catalog** (Swiss BS-KI) as proof of concept — the framework is regulation-agnostic
- Making regulations **queryable by AI agents** and **verifiable against IT systems** (Meaningful Human Control)

The project originated at **Hack4Rail 2026** (joint hackathon by SBB, ÖBB, DB and the OpenRail Association), where team A38 built the first working prototype in 24 hours: a complete OSCAL4Rail **example implementation** for the Swiss "Branchenstandard Kundeninformation" (BS-KI) with 42 controls, validated against the official NIST OSCAL JSON Schema.

---

## Who are the maintainers of the project?

| Name | Organisation | Contact |
|------|-------------|---------|
| Jens Grote (Project Lead) | DB Systel GmbH | jens.grote@deutschebahn.com |
| Arpad Vasarhelyi | Deutsche Bahn | Arpad.Vasarhelyi@deutschebahn.com |
| Simon Freihart (pending) | SBB | Simon.Freihart@sbb.ch |

---

## Which organizations are sponsoring/contributing to the project?

- **Deutsche Bahn / DB Systel GmbH** (project lead, tooling)
- **SBB** (BS-KI example implementation, domain expertise) – participation to be confirmed
- **ÖBB** – participation to be confirmed
- **NIST** (indirect: OSCAL base standard, CC0)

---

## Where is the code hosted?

Currently: https://github.com/OpenRail-Playground/A38/tree/main/OSCAL4Rail

Target: https://github.com/OpenrailAssociation/oscal4rail

---

## Which exact repositories do you intend to transfer to the GitHub organization of the OpenRail Association?

The `OSCAL4Rail/` directory from https://github.com/OpenRail-Playground/A38 will be extracted into a new standalone repository:

**Proposed name:** `OpenRailAssociation/oscal4rail`

Contents:
- Tooling (`tools/`: extract.py, validate.py, diff.py)
- Example implementations (`examples/bs-ki/de/`)
- Documentation (`docs/`: arc42, tutorials, how-tos, examples)
- OSS governance files (LICENSE, CONTRIBUTING, GOVERNANCE, MAINTAINERS, CODE_OF_CONDUCT)

---

## What is the project's main license?

**Apache 2.0**

---

## What other licenses does the project use?

- **NIST OSCAL JSON Schema** (`catalogs/schema/oscal-catalog.json`): CC0 1.0 Universal (Public Domain) — National Institute of Standards and Technology (NIST)
- **Regulation content** (verbatim quotes in catalogs): Copyright of respective standards bodies (KKI/Alliance SwissPass for BS-KI; ERA for TSI). Reproduced for compliance and interoperability purposes.

See [NOTICE.md](NOTICE.md) for details.

---

## Are any trademarks associated with the project?

No trademarks are registered. "OSCAL4Rail" is a descriptive name. "OSCAL" is a NIST acronym (not trademarked).

---

## Does the project have a web site?

Not yet. We are open to hosting documentation on an OpenRail Association-managed site (e.g. projects.openrailassociation.org/oscal4rail).

---

## What are the communication channels the project uses?

- **GitHub Issues and Discussions** (primary)
- **Email** for maintainer coordination
- OpenRail Association community channels (once onboarded)

---

## What is the project's leadership team and decision-making process?

See [GOVERNANCE.md](GOVERNANCE.md).

Summary: Day-to-day decisions by maintainers via PR review. Significant changes require two maintainer approvals. Breaking changes require Steering Committee consensus. The OpenRail TC serves as escalation path.

---

## How is it decided if and when a pull request is merged?

- Minor changes (typos, formatting): one maintainer approval
- Catalog updates: Catalog Maintainer approval + CI validation passing
- Structural/format changes: two maintainer approvals
- Breaking changes: TC discussion

---

## How can someone become a committer or a maintainer?

Contributors with sustained, high-quality contributions are invited by existing maintainers. See [GOVERNANCE.md](GOVERNANCE.md).

---

## How is development planned and organized? Is this transparent to the public?

Planning is done via GitHub Issues and the project roadmap in the README. All discussions and decisions are public on GitHub.

---

## What is the project's roadmap?

**Short-term (Q3 2026):**
- Extract OSCAL4Rail into standalone repository (`OpenRailAssociation/oscal4rail`)
- **Catalog Profile**: Extend OSCAL schema for railway-specific requirements (ID conventions, applicability model, multilingual support)
- **Example Catalog**: One publicly available regulation (BS-KI) as proof of concept
- **Rules Layer**: Define applicability format using **Rulemapping** methodology — which controls apply in which context?
- CI/CD pipeline (GitHub Actions: validate schemas and examples on every PR)

**Mid-term (Q4 2026 – Q1 2027):**
- **Assessment Engine**: Build assessment tooling for AI agents and human reviewers (Meaningful Human Control)
- **Change Impact Layer**: Structured, machine-readable change notifications when regulations are updated
- Contact **SPRIND Law-as-Code** initiative — present OSCAL4Rail as sectoral implementation for railway; align on format compatibility once SPRIND defines their output standard
- Engage standards bodies (KKI, ERA) — today they publish PDF only; demonstrate value of machine-readable regulations
- Publish tooling as installable Python package
- ~~Pilot Rulemapping methodology on one BS-KI control~~ ✅ Done (2026-06-25, see [ADR-006](docs/adr/ADR-006-oscal4rail-vs-rulemapping.md))

**Long-term:**
- Railway regulation bodies (ERA, EBA, BAV) publish natively in machine-readable format — PDF generated from structured source, not the other way around
- Cross-regulation compliance checking (regulatory cascade: EU → National → Industry → Company)
- When SPRIND Law-as-Code defines an official publication format: OSCAL4Rail consumes it as upstream, replacing PDF extraction
- Integration with AI compliance agents (automated assessment with Meaningful Human Control)

---

## What other organizations should be interested in this project?

- All European railway companies (DB, SBB, ÖBB, SNCF, Network Rail, Infrabel, ...)
- Standards bodies: ERA, KKI, BAV, EBA (Eisenbahn-Bundesamt)
- IT system vendors for passenger information systems
- Regulatory compliance teams
- AI/LLM teams building regulation-aware agents

---

## Why would this project be a good candidate for inclusion in the OpenRail Association?

1. **Cross-company value**: Every European railway faces the same problem. One shared open standard benefits all.
2. **Standards alignment**: Built on NIST OSCAL (public domain) — no license conflicts.
3. **Proven at Hack4Rail 2026**: Working prototype in 24h, 42 rules extracted and validated.
4. **OpenRail DNA**: Open, collaborative, railway-specific, public interest.
5. **Multiplier effect**: Once catalogs exist for BST-KI and TSI, dozens of IT systems can use them.
6. **AI-ready**: Machine-readable regulations enable the next generation of AI compliance agents in the railway sector.
7. **Law-as-Code clarity**: OSCAL4Rail is clearly differentiated from the SPRIND "Law as Code" initiative. While both make regulations machine-readable, they serve different audiences and lifecycle phases: Rulemapping helps legislators *formulate* rules (citizen-facing decision trees), OSCAL4Rail helps compliance teams *manage and verify* rules at scale (versioned catalogs, regulatory cascades, automated checking). They are not competing — potential upstream/downstream relationship where regulations modeled in Rulemapping could feed into OSCAL4Rail catalogs. See [ADR-006](docs/adr/ADR-006-oscal4rail-vs-rulemapping.md).

---

## Are there competing products or projects?

No direct competitors for an open, railway-specific, OSCAL-based standard. Adjacent and complementary projects:

| Project | Relationship |
|---------|-------------|
| NIST OSCAL | Base standard (public domain) — OSCAL4Rail is a domain profile |
| OSRD (OpenRail) | Infrastructure simulation — complementary, not competing |
| ERA RINF / TAF-TSI | EU data standards for infrastructure/traffic — different domain, potentially linkable |
| SPRIND "Law as Code" | Federal initiative for machine-readable legislation. Different problem space: SPRIND/Rulemapping targets legislators and citizen-facing decision support (e.g. "Do I need a building permit?"). OSCAL4Rail targets compliance management at scale (e.g. "Which of 10,000 rules apply to my systems and what changed?"). They address different phases in the regulation lifecycle: Rulemapping helps *create* rules, OSCAL4Rail helps *manage and verify* them. See [ADR-006](docs/adr/ADR-006-oscal4rail-vs-rulemapping.md) |
| Rulemapping (Rulemapping Group) | Methodology for translating legal text into interactive decision trees for individual-case decisions. Different audience (legislators, citizens) and different purpose (single-case yes/no) than OSCAL4Rail (mass compliance, versioning, cascades). Possible interface: regulations modeled in Rulemapping could feed into OSCAL4Rail catalogs as upstream source |
| Commercial compliance tools | Proprietary, vendor lock-in, not railway-specific |

---

## What standards does the project implement or rely on?

| Standard | Role |
|----------|------|
| NIST OSCAL 1.1.3 | Base format (Catalog model) |
| JSON Schema (Draft 7) | Validation |
| Semantic Versioning | Catalog releases |
| Conventional Commits | Contribution workflow |
| BS-KI v1.0 | First example implementation |
| TSI Telematics (EU 2026/253) | Planned catalog |

---

## What is the tech stack?

- **Python 3.10+** — extraction pipeline, validation, diff tooling
- **YAML** — catalog format
- **JSON Schema** — OSCAL validation
- **markitdown** — PDF text extraction
- **openpyxl** — Excel matrix parsing
- **PyYAML, jsonschema** — core libraries

No framework dependencies. Minimal, portable, inspectable.

---

## What is the project's plan for growing in maturity if accepted?

1. **Stage 1 → Stage 2:** Complete tooling suite, add CI/CD, grow maintainer team, publish first version with multiple catalogs
2. **Stage 2 → Stage 3:** Formal adoption by at least one standards body for official catalog publication; proven use by at least two railway companies

---

## Concluding statements

By sending this questionnaire we confirm that the project will adhere to the code of conduct of the OpenRail Association.

By sending this questionnaire we confirm that the project intends to be incubated in the OpenRail Association and plans to meet the maturity criteria set out by the OpenRail Association for incubated projects.
