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
- Adapting the **NIST OSCAL Catalog** model (public domain, CC0 1.0) as a lightweight profile for railway regulations
- Providing a **deterministic extraction pipeline**: PDF + Excel matrix → validated, machine-readable YAML
- Requiring **verbatim quotes** from source documents — no paraphrasing, no interpretation
- Giving every rule a **stable identifier** derived from the chapter number (not the page number)
- Enabling **semantic diff** across versions: what changed, what was added, what was removed
- Making regulations **queryable by AI agents** and **verifiable against IT systems**

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

Target: A dedicated repository under the OpenRail Association GitHub organization.

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
- Extract OSCAL4Rail into a standalone repository
- Complete BS-KI example implementation (DE/FR/IT)
- Build diff and changelog tooling
- Add CI/CD pipeline (GitHub Actions: validate on every PR)

**Mid-term (Q4 2026 – Q1 2027):**
- Extend to EU TSI Telematics regulation
- Engage standards bodies (KKI, ERA) for official adoption
- Publish tooling as installable Python package

**Long-term:**
- Regulation authors write natively in OSCAL4Rail (PDF generated from YAML)
- Cross-regulation compliance checking
- Integration with AI compliance agents

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

---

## Are there competing products or projects?

No direct competitors for an open, railway-specific, OSCAL-based standard. Adjacent projects:

| Project | Relationship |
|---------|-------------|
| NIST OSCAL | Base standard (public domain) — OSCAL4Rail is a domain profile |
| OSRD (OpenRail) | Infrastructure simulation — complementary, not competing |
| ERA RINF / TAF-TSI | EU data standards for infrastructure/traffic — different domain, potentially linkable |
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
