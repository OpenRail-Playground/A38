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

## Existing Catalogs

| Catalog | Language | Status | Source |
|---------|----------|--------|--------|
| `catalogs/bs-ki/de` | German | ✅ 42 controls | [BS-KI v1.0](https://www.oev-info.ch/de/branchenstandard/nationaler-branchenstandard-kundeninformation) |
| `catalogs/bs-ki/fr` | French | 🔜 planned | BS-KI v1.0 |
| `catalogs/bs-ki/it` | Italian | 🔜 planned | BS-KI v1.0 |
| `catalogs/tsi-tat` | English | 🔜 planned | EU TSI Telematics |

## License

- **OSCAL4Rail tooling and documentation:** [Apache 2.0](LICENSE)
- **NIST OSCAL base standard:** [CC0 1.0 Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)
- **Regulation content (BS-KI, TSI, etc.):** Copyright of respective standards bodies — verbatim quotes for compliance purposes
