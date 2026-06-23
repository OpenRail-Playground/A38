"""Render a catalog YAML (produced by pdf_zu_yaml.py) as a standalone HTML page.

Usage:
    python yaml_to_html.py 800_0110.yaml

Writes 800_0110.html next to the input. The file is self-contained (Base64
images are embedded) and opens directly in a browser – no web server needed.
"""

import os
import re
import sys
import html

import yaml


# Markdown image reference with an embedded data URI: ![alt](data:image/png;base64,…)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((data:[^)]+)\)")

CSS = """
body { font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto;
       padding: 0 1rem; line-height: 1.5; color: #222; }
h1 { border-bottom: 2px solid #ccc; padding-bottom: .3rem; }
h2, h3, h4, h5, h6 { margin-top: 1.6rem; }
.gid { color: #888; font-weight: normal; }
table { border-collapse: collapse; margin: 1rem 0; }
th, td { border: 1px solid #999; padding: .3rem .6rem; text-align: left;
         vertical-align: top; }
th { background: #f0f0f0; }
img { max-width: 100%; height: auto; display: block; margin: 1rem 0;
      border: 1px solid #ddd; }
p { margin: .6rem 0; }
"""


def render_inline(text):
    """Escape text and turn Markdown image references into <img> tags."""
    out = []
    last = 0
    for m in IMAGE_RE.finditer(text):
        out.append(html.escape(text[last:m.start()]))
        out.append(f'<img src="{m.group(1)}" alt="">')  # data URI, no escaping
        last = m.end()
    out.append(html.escape(text[last:]))
    return "".join(out)


def split_cells(line):
    """Split one Markdown table row into cells, honouring escaped pipes (\\|)."""
    inner = line.strip().strip("|")
    return [c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", inner)]


def is_table_block(block):
    lines = [l for l in block.strip().split("\n") if l.strip()]
    return len(lines) >= 2 and all(l.lstrip().startswith("|") for l in lines)


def render_table(block):
    rows = [split_cells(l) for l in block.strip().split("\n") if l.strip()]
    header = rows[0]
    body = rows[2:]  # rows[1] is the "| --- | --- |" separator
    parts = ["<table>", "<thead><tr>"]
    parts += [f"<th>{render_inline(c)}</th>" for c in header]
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in row) + "</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def render_prose(prose):
    """Render a prose string (text, Markdown tables, embedded images) to HTML."""
    blocks = re.split(r"\n\n+", prose.strip())
    out = []
    for block in blocks:
        if not block.strip():
            continue
        if is_table_block(block):
            out.append(render_table(block))
        else:
            out.append(f"<p>{render_inline(block)}</p>")
    return "\n".join(out)


def render_group(group, level):
    """Render a section group and its subgroups recursively."""
    gid = group.get("id", "")
    title = group.get("title", "")
    tag = f"h{min(level, 6)}"

    out = [f'<{tag} id="{html.escape(gid)}">'
           f'<span class="gid">{html.escape(gid)}</span> {html.escape(title)}</{tag}>']

    for part in group.get("parts", []):
        prose = part.get("prose", "")
        if prose:
            out.append(render_prose(prose))

    for sub in group.get("groups", []):
        out.append(render_group(sub, level + 1))

    return "\n".join(out)


def build_html(title, body):
    return (
        '<!DOCTYPE html>\n<html lang="de">\n<head>\n'
        '<meta charset="utf-8">\n'
        f"<title>{html.escape(title)}</title>\n"
        f"<style>{CSS}</style>\n"
        "</head>\n<body>\n"
        f"<h1>{html.escape(title)}</h1>\n"
        f"{body}\n"
        "</body>\n</html>\n"
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python yaml_to_html.py <catalog.yaml>")
        sys.exit(1)

    yaml_path = sys.argv[1]
    if not os.path.exists(yaml_path):
        print(f"File not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    catalog = (data or {}).get("catalog", {})
    title = catalog.get("metadata", {}).get("title", "Catalog")
    body = "\n".join(render_group(g, 2) for g in catalog.get("groups", []))

    out_path = os.path.splitext(yaml_path)[0] + ".html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(build_html(title, body))

    print(f"HTML written to {out_path} – open it in your browser.")


if __name__ == "__main__":
    main()
