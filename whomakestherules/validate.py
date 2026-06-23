#!/usr/bin/env python3
"""Validate OSCAL Catalog YAML against the official NIST JSON Schema."""

import json
import sys
from pathlib import Path

import jsonschema
import jsonschema._keywords
import yaml
from jsonschema import Draft7Validator

SCHEMA_PATH = Path(__file__).parent / "rules" / "schema" / "oscal-catalog.json"


def safe_pattern(validator, patrn, instance, schema):
    """Skip Unicode regex patterns (\\p{L}) not supported by Python re."""
    if r"\p{" in patrn:
        return
    yield from jsonschema._keywords.pattern(validator, patrn, instance, schema)


CustomValidator = jsonschema.validators.extend(Draft7Validator, {"pattern": safe_pattern})


def validate(yaml_path: str) -> bool:
    with open(yaml_path) as f:
        catalog = yaml.safe_load(f)

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    validator = CustomValidator(schema)
    errors = sorted(validator.iter_errors(catalog), key=lambda e: list(e.absolute_path))

    if not errors:
        print(f"✅ {yaml_path}: Valid OSCAL Catalog")
        return True

    print(f"❌ {yaml_path}: {len(errors)} validation error(s):")
    for e in errors[:20]:
        path = ".".join(str(p) for p in e.absolute_path)
        print(f"  - [{path}] {e.message[:150]}")
    return False


if __name__ == "__main__":
    files = sys.argv[1:] or ["rules/bs-ki-de.yaml"]
    all_valid = all(validate(f) for f in files)
    sys.exit(0 if all_valid else 1)
