# OSCAL4Rail

> Machine-readable railway regulations based on the [NIST OSCAL](https://pages.nist.gov/OSCAL/) standard.
> Inspired by Arpad Vasarhelyi (Arpad.Vasarhelyi@deutschebahn.com)

**OSCAL4Rail** is an open standard for making railway regulations machine-readable, schema-validated, versionable, and diffable — enabling deterministic compliance checking across railway companies, borders, and languages.

## Why OSCAL4Rail?

Railway regulations are scattered across thousands of PDFs. They are written as free text and interpreted individually by each reader — leading to inconsistent, non-deterministic application across organisations and countries. Version changes are invisible. Nobody knows what changed between BS-KI v1.0 and v2.0 at the rule level.

OSCAL4Rail solves this by:
- Extracting rules **verbatim** from source documents
- Storing them in a **schema-validated, machine-readable** YAML format (NIST OSCAL Catalog)
- Giving every rule a **stable identifier** (chapter number, not page number)
- Enabling **semantic diff** across versions: what changed, what was added, what was removed
- Making regulations **queryable by AI agents** and **verifiable against your IT systems**

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

OSCAL4Rail and the SPRIND "Law as Code" initiative (including Rulemapping) solve **different problems for different audiences** at different phases in the lifecycle of a regulation:

| Phase | Who | Tool | Question |
|-------|-----|------|----------|
| **Create** | Legislators, standards bodies | Rulemapping | "How do I formulate this rule precisely? What conditions, exceptions?" |
| **Manage** | Compliance teams, IT architects | OSCAL4Rail | "Which rules apply? What changed? Is our implementation still conformant?" |
| **Verify** | AI agents, automated checks | OSCAL4Rail + tooling | "Does system X comply with control Y across 10,000 assets?" |

Rulemapping models **decision logic** (interactive decision trees for individual cases). OSCAL4Rail models **regulatory content** (verbatim rules, versioned catalogs, regulatory cascades from EU → national → company level).

They are not competing — they complement each other across the regulation lifecycle. See [ADR-006](docs/adr/ADR-006-oscal4rail-vs-rulemapping.md) for the full analysis.

## License

- **OSCAL4Rail tooling and documentation:** [Apache 2.0](LICENSE)
- **NIST OSCAL base standard:** [CC0 1.0 Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)
- **Regulation content (BS-KI, TSI, etc.):** Copyright of respective standards bodies — verbatim quotes for compliance purposes
