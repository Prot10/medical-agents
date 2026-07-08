#!/usr/bin/env python3
"""Headless-browser driver for the NeuroBench review app (web-review + review_api).

Logs in with a reviewer code, optionally clicks through a chain of tab
labels, and screenshots the result. Requires Chromium to be installed once
via: uvx --from playwright playwright install chromium --with-deps

Usage:
    uvx --from playwright python driver.py \
        --code NB-XXXX-XXXX-XXXX \
        --click "Admin" --click "Reviewer progress" \
        --out /tmp/out.png

    # No --click => stays on the default post-login tab (Overview).
"""
from __future__ import annotations

import argparse
import sys

from playwright.sync_api import sync_playwright


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", default="http://localhost:5174")
    p.add_argument("--code", required=True, help="X-Reviewer-Code to log in with")
    p.add_argument("--click", action="append", default=[], help="Text of an element to click, in order (repeatable)")
    p.add_argument("--out", required=True, help="Screenshot output path")
    p.add_argument("--wait-ms", type=int, default=1200, help="Pause after each click/login, in ms")
    args = p.parse_args()

    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

        page.goto(args.base_url, wait_until="networkidle")
        page.wait_for_selector("input", timeout=15000)
        page.fill("input", args.code)
        page.keyboard.press("Enter")
        page.wait_for_timeout(args.wait_ms)

        for label in args.click:
            page.get_by_text(label, exact=False).first.click()
            page.wait_for_timeout(args.wait_ms)

        page.screenshot(path=args.out, full_page=True)
        browser.close()

    print(f"screenshot: {args.out}")
    print(f"console errors: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
