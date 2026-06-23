import os
import io
import re
import sys
import json
import uuid
import base64
import hashlib
import datetime

import pdfplumber
import yaml
import ollama
from jsonschema import Draft7Validator


# === Part 1: Read PDF pages as Markdown ====================================

def clean_text(text):
    """Remove margin artifacts and rejoin split words."""

    # 1. join a hyphen at the end of a line – even with a single stray margin
    #    character in between: "Li- Z\nnienführung" -> "Linienführung"
    text = re.sub(r"-\s*[A-Za-zÄÖÜäöüß(]?\s*\n\s*", "", text)

    # 2. remove single unrelated characters at the end of a line:
    #    "...km/h. b" -> "...km/h."
    text = re.sub(r"(?m)[ \t]+[A-Za-zÄÖÜäöüß(]\s*$", "", text)

    # 3. delete lines that consist of just a single character
    text = re.sub(r"(?m)^\s*[A-Za-zÄÖÜäöüß(]\s*$\n?", "", text)

    # 4. remaining line breaks -> spaces, collapse multiple spaces
    text = " ".join(text.split())

    return text


def is_header_table(table):
    rows = table.extract()
    if len(rows) != 2:
        return False
    return all(len(row) == 3 for row in rows)


def table_to_markdown(table):
    """Convert a pdfplumber table into a clean Markdown table."""

    def cell(c):
        # clean the cell content: collapse line breaks, escape "|"
        return " ".join((c or "").split()).replace("|", r"\|")

    rows = [[cell(c) for c in row] for row in table.extract()]
    # drop completely empty rows
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""

    width = max(len(r) for r in rows)
    # pad every row to the same number of columns
    rows = [(r + [""] * width)[:width] for r in rows]

    header = rows[0]
    md = ["| " + " | ".join(header) + " |",
          "| " + " | ".join(["---"] * width) + " |"]
    md += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(md)


def in_range(value, low, high):
    return low <= value <= high


def page_side(x0, x1):
    """Classify a page as "left" or "right" from the header table's x-edges."""
    if in_range(x0, 10, 60) and in_range(x1, 450, 480):
        return "left"
    if in_range(x0, 115, 145) and in_range(x1, 535, 585):
        return "right"
    return None


TOP_LIMIT = 160          # header table must end above this y-coordinate
BOTTOM_LIMIT = 770       # bottom of the reading area
OFFSET = 87              # horizontal shift between the header and the body column
IMAGE_RESOLUTION = 150   # dpi when rasterizing an image region to PNG
IMAGE_MIN_SIZE = 20      # ignore tiny decorative images (in points)


def reading_area(side, hx0, hbottom, hx1):
    if side == "left":
        return (hx0 + OFFSET, hbottom + 2, hx1 + 2, BOTTOM_LIMIT)
    if side == "right":
        return (hx0 - 2, hbottom + 2, hx1 - OFFSET, BOTTOM_LIMIT)
    return None


def images_in_area(page, area):
    """Return the images whose center lies inside the reading area."""
    x0, top, x1, bottom = area
    found = []
    for image in page.images:
        cx = (image["x0"] + image["x1"]) / 2
        cy = (image["top"] + image["bottom"]) / 2
        if x0 <= cx <= x1 and top <= cy <= bottom:
            found.append(image)
    return found


def image_to_markdown(page, image):
    """Render an image region to PNG and return a Markdown image reference with
    the PNG embedded as a Base64 data URI: ``![<hash>](data:image/png;base64,…)``.

    The short content hash serves as the alt text (a stable identifier).
    Returns None if the image is too small or rendering is unavailable.
    """
    if image["width"] < IMAGE_MIN_SIZE or image["height"] < IMAGE_MIN_SIZE:
        return None

    bbox = (image["x0"], image["top"], image["x1"], image["bottom"])
    try:
        rendered = page.crop(bbox).to_image(resolution=IMAGE_RESOLUTION).original
    except Exception as error:
        print(f"  image on page {page.page_number} skipped – {error}")
        return None

    buffer = io.BytesIO()
    rendered.save(buffer, format="PNG")
    data = buffer.getvalue()

    digest = hashlib.sha256(data).hexdigest()[:16]
    encoded = base64.b64encode(data).decode("ascii")
    return f"![{digest}](data:image/png;base64,{encoded})"


def read_area_as_markdown(page, area):
    """Read the reading area top to bottom: prose is smoothed with
    clean_text(), tables become Markdown tables and images become Markdown
    references with the PNG embedded as a Base64 data URI."""
    x0, top, x1, bottom = area

    # collect tables and images as (top, bottom, markdown) regions
    regions = []
    for t in page.crop(area).find_tables():
        md = table_to_markdown(t)
        if md:
            regions.append((t.bbox[1], t.bbox[3], md))
    for image in images_in_area(page, area):
        md = image_to_markdown(page, image)
        if md:
            regions.append((image["top"], image["bottom"], md))

    regions.sort(key=lambda r: r[0])

    blocks = []

    def prose_block(start, end):
        # read the narrow band between two regions (or the edges) as text
        if end <= start:
            return
        raw = page.crop((x0, start, x1, end)).extract_text()
        if raw and raw.strip():
            blocks.append(clean_text(raw))

    cursor = top
    for region_top, region_bottom, md in regions:
        prose_block(cursor, region_top)    # prose above the region
        blocks.append(md)
        cursor = max(cursor, region_bottom)
    prose_block(cursor, bottom)            # prose below the last region

    return "\n\n".join(b for b in blocks if b)


def read_pages(pdf_path):
    """Read the relevant pages of the PDF as a list of (number, side, text)."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for number, page in enumerate(pdf.pages, start=1):

            # find a matching header row
            header = None
            for t in page.find_tables():
                x0, top, x1, bottom = t.bbox
                if bottom <= TOP_LIMIT and is_header_table(t):
                    header = t
                    break

            if header is None:
                continue

            hx0, htop, hx1, hbottom = header.bbox
            side = page_side(hx0, hx1)

            if side not in ("left", "right"):
                continue

            # crop the reading area, smooth prose, read tables as Markdown
            area = reading_area(side, hx0, hbottom, hx1)
            text = read_area_as_markdown(page, area)

            if text and text.strip():
                pages.append((number, side, text))

    return pages


def write_markdown(path, base_name, pages):
    """Save the extracted pages as Markdown (H1 = base name)."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {base_name}\n\n")
        for number, side, text in pages:
            # one heading per page so it can be located again later
            f.write(f"## Page {number} ({side})\n\n")
            f.write(text)
            f.write("\n\n---\n\n")   # separator between pages


# === Part 2: Split page text into section and numbered paragraphs ==========

def split_into_paragraphs(rest):
    """Split the text at real paragraph markers "(1)", "(2)", ...

    Not every "(n)" is a paragraph: references to laws or other guidelines
    such as "§ 4 (11)" or "Ril 800.0120, Abschnitt 4 (1)" sit directly behind
    a number and belong to the running text. Such spots are not treated as a
    paragraph boundary.

    Returns (preamble, paragraphs) like parse_page.
    """
    markers = []
    for match in re.finditer(r"\((\d+)\)", rest):
        before = rest[:match.start()].rstrip()
        # if a digit sits directly before it, it is a reference -> skip
        if before and before[-1].isdigit():
            continue
        markers.append((match.start(), match.end(), match.group(1)))

    if not markers:
        return rest.strip(), []

    preamble = rest[:markers[0][0]].strip()
    paragraphs = []
    for i, (_, marker_end, number) in enumerate(markers):
        end = markers[i + 1][0] if i + 1 < len(markers) else len(rest)
        paragraphs.append((number, rest[marker_end:end].strip()))

    return preamble, paragraphs


def parse_page(text):
    """Split a page text into (section_nr, preamble, paragraphs).

    - section_nr: the leading section number, e.g. "1". None if the page does
                  not start with a heading ("1 Allgemeines") – then it is a
                  continuation of the previous page.
    - preamble:   the text before the first "(n)" – on a heading page the
                  heading ("Allgemeines"), on a continuation the carried-over
                  prose of the previous page.
    - paragraphs: list of (number, text) for each "(n)" paragraph.
    """
    # A heading is a leading number followed by a capital letter
    # ("1 Allgemeines"). If the page starts with "(6)" or a lowercase letter,
    # there is no heading.
    m = re.match(r"\s*(\d+)\s+([A-ZÄÖÜ].*)", text, flags=re.DOTALL)
    if m:
        section_nr = m.group(1)
        rest = m.group(2).strip()
    else:
        section_nr = None
        rest = text.strip()

    # split at the real paragraph markers "(1)", "(2)", ... – references like
    # "§ 4 (11)" stay part of the running text.
    preamble, paragraphs = split_into_paragraphs(rest)

    return section_nr, preamble, paragraphs


# === Part 3: Generate titles with the local model =========================

TITLE_FORMAT = {
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
}

OUTPUT_FORMAT = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "prose": {"type": "string"},
    },
    "required": ["title", "prose"],
}


def generate_title(text):
    """Have the model phrase a short heading for a paragraph.

    The instruction is German on purpose: the source documents are German and
    the resulting titles must be German as well.
    """
    instruction = (
        "Du erhältst einen nummerierten Absatz aus einer technischen Richtlinie. "
        "Formuliere eine sehr kurze, treffende Überschrift (3 bis 6 Wörter) für "
        "diesen Absatz. Gib nur das Feld title zurück, ohne Absatznummer und ohne "
        "Satzzeichen am Ende."
    )
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": text},
        ],
        format=TITLE_FORMAT,
    )
    return json.loads(response["message"]["content"])["title"].strip()


def extract_title_and_prose(text):
    """For sections without "(n)" paragraphs, split heading from running text.

    German instruction on purpose (see generate_title).
    """
    instruction = (
        "Du erhältst den Text eines Abschnitts aus einer technischen Richtlinie, "
        "der mit seiner Überschrift beginnt. Trenne die Überschrift vom Fließtext. "
        "Gib title (nur die Überschrift) und prose (der restliche Text) zurück."
    )
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": text},
        ],
        format=OUTPUT_FORMAT,
    )
    return json.loads(response["message"]["content"])


# === Part 4: Build groups from the parsed pages ===========================

def build_subgroup(base_name, section_nr, paragraph_nr, paragraph_text):
    """A numbered paragraph "(n)" becomes the subgroup <base>.N.n."""
    return {
        "id": f"{base_name}.{section_nr}.{paragraph_nr}",
        "title": generate_title(paragraph_text),
        "parts": [{"name": "statement", "prose": paragraph_text}],
    }


def build_group(base_name, section_nr, preamble, paragraphs):
    """Build a new section group from a heading page."""
    group = {"id": f"{base_name}.{section_nr}"}
    if paragraphs:
        # the section heading is right there in the text ("Allgemeines")
        group["title"] = preamble or generate_title(paragraphs[0][1])
        group["groups"] = [build_subgroup(base_name, section_nr, p_nr, p_text)
                           for p_nr, p_text in paragraphs]
    else:
        # no numbered paragraph: let the model split heading from running text
        data = extract_title_and_prose(preamble)
        group["title"] = data["title"]
        group["parts"] = [{"name": "statement", "prose": data["prose"]}]
    return group


def append_prose(group, text):
    """Append carried-over prose to the most recently opened paragraph."""
    if group.get("groups"):
        target = group["groups"][-1]["parts"][-1]
    elif group.get("parts"):
        target = group["parts"][-1]
    else:
        group["parts"] = [{"name": "statement", "prose": text}]
        return
    target["prose"] = (target["prose"].rstrip() + " " + text.strip()).strip()


def continue_section(base_name, group, preamble, paragraphs):
    """Continue the running section with the content of a follow-up page."""
    # recover the section number from the group id "<base>.N"
    section_nr = group["id"][len(base_name) + 1:]

    # text before the first "(n)" still belongs to the previous page's paragraph
    if preamble:
        append_prose(group, preamble)

    # further "(n)" paragraphs continue the section's numbering
    if paragraphs:
        group.setdefault("groups", [])
        for p_nr, p_text in paragraphs:
            group["groups"].append(build_subgroup(base_name, section_nr, p_nr, p_text))


def build_groups(base_name, pages):
    """Build the list of section groups from the extracted pages."""
    groups = []
    current_group = None  # most recently opened section – target for continuations

    for number, side, text in pages:
        section_nr, preamble, paragraphs = parse_page(text)

        try:
            if section_nr is not None:
                # heading found -> start a new section
                current_group = build_group(base_name, section_nr, preamble, paragraphs)
                groups.append(current_group)
                print(f"Page {number} (section {section_nr}): new section")
            elif current_group is not None:
                # no heading -> continue the previous section
                continue_section(base_name, current_group, preamble, paragraphs)
                print(f"Page {number}: continuation of {current_group['id']}")
            else:
                # very first page without a heading – nothing to continue
                print(f"Page {number}: no heading and no open section – skipped.")
        except Exception as error:
            print(f"Page {number}: problem – {error}")

    return groups


# === Part 5: Schema repair and validation (known) =========================

def fix_patterns(obj):
    if isinstance(obj, dict):
        return {k: (v.replace(r"\p{L}", r"[^\W\d_]").replace(r"\p{N}", r"\d")
                    if k == "pattern" and isinstance(v, str) else fix_patterns(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [fix_patterns(x) for x in obj]
    return obj


def validate_schema(catalog, schema_path="oscal-catalog.json"):
    """Validate the catalog against the OSCAL schema, if available."""
    if not os.path.exists(schema_path):
        print(f"Note: {schema_path} not found – schema validation skipped.")
        return

    with open(schema_path, encoding="utf-8") as f:
        schema = fix_patterns(json.load(f))

    errors = sorted(Draft7Validator(schema).iter_errors(catalog),
                    key=lambda e: list(e.absolute_path))
    if not errors:
        print("✓ VALID – matches the OSCAL schema.")
    else:
        print(f"✗ INVALID – {len(errors)} problem(s):")
        for e in errors:
            location = " -> ".join(str(x) for x in e.absolute_path) or "(root)"
            print(f"   • at [{location}]: {e.message}")


# === Part 6: Main program =================================================

def build_catalog(base_name, groups):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "catalog": {
            "uuid": str(uuid.uuid4()),
            "metadata": {
                "title": base_name,
                "last-modified": now,
                "version": "1.0",
                "oscal-version": "1.1.3",
            },
            "groups": groups,
        }
    }


def diagnose(pdf_path):
    """Show per page whether/why it is kept or dropped.

    Helps to re-calibrate the hard-coded thresholds (TOP_LIMIT and the
    left/right coordinate windows) for a new document.
    """
    kept = 0
    no_header = 0
    no_side = 0

    with pdfplumber.open(pdf_path) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            all_tables = sorted(page.find_tables(), key=lambda t: t.bbox[1])
            candidates = [t for t in all_tables if t.bbox[3] <= TOP_LIMIT]

            header = next((t for t in candidates if is_header_table(t)), None)
            if header is None:
                no_header += 1
                # show the topmost table on the page – even just below TOP_LIMIT
                if all_tables:
                    t = all_tables[0]
                    rows = t.extract()
                    shape = f"{len(rows)}x{[len(r) for r in rows]}"
                    print(f"Page {number}: no 2x3 header table near the top. "
                          f"Topmost table: bottom={t.bbox[3]:.1f}, shape {shape}")
                else:
                    print(f"Page {number}: no table detected at all")
                continue

            hx0, htop, hx1, hbottom = header.bbox
            side = page_side(hx0, hx1)
            if side is None:
                no_side += 1
                print(f"Page {number}: header found, side unclear – "
                      f"x0={hx0:.1f}, x1={hx1:.1f} (outside the left/right windows)")
                continue

            kept += 1
            print(f"Page {number}: OK ({side})  x0={hx0:.1f} x1={hx1:.1f}")

    print(f"\nKept: {kept} | without header table: {no_header} | "
          f"header without matching side: {no_side}")


def main():
    arguments = [a for a in sys.argv[1:] if not a.startswith("--")]
    diagnose_mode = "--diagnose" in sys.argv[1:]

    if len(arguments) != 1:
        print("Usage: python pdf_zu_yaml.py <file.pdf> [--diagnose]")
        sys.exit(1)

    pdf_path = arguments[0]
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    if diagnose_mode:
        diagnose(pdf_path)
        return

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = f"{base_name}.md"
    yaml_path = f"{base_name}.yaml"

    # 1. read the PDF and save it as Markdown
    pages = read_pages(pdf_path)
    write_markdown(md_path, base_name, pages)
    print(f"{len(pages)} page(s) saved to {md_path} (prefix '{base_name}').")

    # 2. structure the pages
    groups = build_groups(base_name, pages)

    # 3. save the catalog as YAML
    catalog = build_catalog(base_name, groups)
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(catalog, f, allow_unicode=True, sort_keys=False)
    print(f"YAML saved as {yaml_path}")

    # 4. validate against the schema (if present)
    validate_schema(catalog)


if __name__ == "__main__":
    main()
