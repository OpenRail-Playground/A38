# OSCAL4Rail

> A 4-layer framework extending [NIST OSCAL](https://pages.nist.gov/OSCAL/) for machine-readable railway governance.
> Inspired by Arpad Vasarhelyi (Arpad.Vasarhelyi@deutschebahn.com)

**OSCAL4Rail** is an open standard for making railway governance machine-readable, deterministic, and AI-agent-ready — from internal IT standards (Konzernrichtlinien) down to regulatory compliance.

## Why OSCAL4Rail?

Railway companies translate legal requirements into internal IT governance (Konzernrichtlinien, internal standards). These company-level adaptations are today scattered across PDFs and Word documents — interpreted individually, applied inconsistently, invisible to automated systems. Nobody knows what changed between v1.0 and v2.0 at the rule level.

OSCAL4Rail solves this with a **4-layer framework**:

| Layer | Based on | What it does |
|-------|----------|--------------|
| **(1) Catalog** | [NIST OSCAL Control Layer](https://pages.nist.gov/OSCAL/learn/concepts/layer/control/) | Machine-readable regulations with railway-specific profile (IDs, applicability, multilingual) |
| **(2) Rules** | [Rulemapping](https://rulemapping.org/) format | Applicability logic: which controls apply in which context? **New — not in NIST OSCAL.** |
| **(3) Change Impact** | — | Structured diff: what changed between versions? **New — not in NIST OSCAL.** |
| **(4) Assessment** | [NIST OSCAL Assessment Layer](https://pages.nist.gov/OSCAL/learn/concepts/layer/assessment/) | Compliance verification by AI agents and human reviewers (Assessment Plan, Results, POA&M) |

The broader vision: the same framework also works for upstream regulations (EU TSI → national laws → industry standards → company implementation) — creating a complete, machine-readable regulatory cascade.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/OpenRail-Playground/OSCAL4Rail.git

# Validate an existing catalog
python3 tools/validate.py catalogs/bs-ki/de/bs-ki-de.yaml
# ✅ catalogs/bs-ki/de/bs-ki-de.yaml: Valid OSCAL4Rail Catalog
```

## Documentation

| Type | Document | Description |
|------|----------|-------------|
| **Architecture** | [docs/arc42.md](docs/arc42.md) | Full arc42 architecture documentation |
| **Motivation** | [docs/motivation.md](docs/motivation.md) | Why OSCAL4Rail exists and what problem it solves |
| **OSS Structure** | [docs/oss-structure.md](docs/oss-structure.md) | Future project structure and governance |
| **Tutorial** | [docs/tutorials/getting-started.md](docs/tutorials/getting-started.md) | Extract your first regulation catalog |
| **How-To** | [docs/how-to/migrate-existing-governance.md](docs/how-to/migrate-existing-governance.md) | Migrate existing governance to OSCAL4Rail |
| **How-To** | [docs/how-to/integrate-agents.md](docs/how-to/integrate-agents.md) | Integrate OSCAL4Rail into AI agents and skills |
| **How-To** | [docs/how-to/verify-it-systems.md](docs/how-to/verify-it-systems.md) | Verify your IT systems against OSCAL4Rail catalogs |
| **Examples** | [docs/examples/](docs/examples/) | Example catalogs and use cases |
| **Reference** | [docs/reference/format.md](docs/reference/format.md) | OSCAL4Rail format specification |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |

## Example Implementations

| Implementation | Language | Status | Source |
|----------------|----------|--------|--------|
| `examples/bs-ki/de` | German | ✅ 42 controls | [BS-KI v1.0](https://www.oev-info.ch/de/branchenstandard/nationaler-branchenstandard-kundeninformation) |
| `examples/bs-ki/fr` | French | 🔜 planned | BS-KI v1.0 |
| `examples/bs-ki/it` | Italian | 🔜 planned | BS-KI v1.0 |
| `examples/tsi-tat` | English | 🔜 planned | EU TSI Telematics |

> **Note:** These are example implementations demonstrating how OSCAL4Rail works in practice. They are not official catalogs published by the respective standards bodies (KKI, ERA). Official catalogs would be published directly by standards bodies once they adopt OSCAL4Rail.

## Relationship to Law-as-Code / Rulemapping

OSCAL4Rail is positioned within the emerging Law-as-Code ecosystem:

| Actor | Role |
|-------|------|
| **SPRIND** | Funds the Law-as-Code initiative for machine-readable legislation |
| **Rulemapping Group** | Defines the rules format — **adopted by OSCAL4Rail as Layer 2** |
| **OpenCode.de** | Will host the machine-readable artifacts |
| **OSCAL4Rail** | Sectoral governance layer for railway — manages, versions, and verifies rules at scale |

| Phase | Who | Tool | Question |
|-------|-----|------|----------|
| **Create** | Legislators, standards bodies | Rulemapping | "How do I formulate this rule precisely?" |
| **Manage** | Compliance teams, IT architects | OSCAL4Rail | "Which rules apply? What changed? Is our implementation conformant?" |
| **Verify** | AI agents, human reviewers | OSCAL4Rail Assessment Layer | "Does system X comply with control Y?" |

Railway regulation bodies (ERA, EBA, BAV) currently publish as PDF only. Once the Law-as-Code ecosystem delivers machine-readable regulations, OSCAL4Rail is designed to consume them as authoritative upstream — replacing today's PDF extraction pipeline.

See [ADR-006](docs/adr/ADR-006-oscal4rail-vs-rulemapping.md) for the full analysis.

## License

- **OSCAL4Rail tooling and documentation:** [Apache 2.0](LICENSE)
- **NIST OSCAL base standard:** [CC0 1.0 Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)
- **Regulation content (BS-KI, TSI, etc.):** Copyright of respective standards bodies — verbatim quotes for compliance purposes
