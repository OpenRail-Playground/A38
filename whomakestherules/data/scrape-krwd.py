#!/usr/bin/env python3
"""Extrahiert Suchergebnisse von anonyme-suche.intranet.deutschebahn.com"""
from playwright.sync_api import sync_playwright

URL = "https://anonyme-suche.intranet.deutschebahn.com/suche?lang=de&filter=regulations&q=Fahrgastinformation"
OUT = "/Users/jensgrote/work/hack4rail/2026/data/krwd-suchergebnisse.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel="msedge")
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle", timeout=30000)
    text = page.inner_text("body")
    browser.close()

with open(OUT, "w") as f:
    f.write(text)

print(f"Gespeichert: {OUT} ({len(text)} Zeichen)")
