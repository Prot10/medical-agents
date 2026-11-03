"""Render the HTML figures to PDF (vector, for submission) and PNG (preview).

    python3 paper/figures/build.py [fig1 fig2 ...]      # default panel style (tint)
    python3 paper/figures/build.py fig1:tint fig2:dots  # a panel style (border, tint, dots) -> fig1-tint.png
    python3 paper/figures/build.py --static fig1 fig2   # self-contained static HTML (figma/fig1.html) for Figma import

Each figN.html declares its printed size in <meta name="figure-size" content="180x170"> (mm).
The pages are served over a local HTTP server so they can fetch the icons and data/figures.json.
"""

from __future__ import annotations

import functools
import http.server
import re
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PX_PER_MM = 96 / 25.4


def serve() -> int:
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args) -> None:
            pass

    handler = functools.partial(Quiet, directory=str(HERE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server.server_address[1]


def chrome(*args: str) -> None:
    profile = Path(tempfile.gettempdir()) / "figchrome"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    f"--user-data-dir={profile}", "--virtual-time-budget=6000", *args],
                   check=True, capture_output=True, timeout=120)


def build(target: str, port: int) -> None:
    name, _, style = target.partition(":")
    html = (HERE / f"{name}.html").read_text()
    w, h = map(float, re.search(r'name="figure-size" content="([\d.]+)x([\d.]+)"', html).groups())
    url = f"http://127.0.0.1:{port}/{name}.html" + (f"?style={style}" if style else "")
    out = f"{name}-{style}" if style else name
    chrome("--force-device-scale-factor=4", f"--window-size={round(w * PX_PER_MM)},{round(h * PX_PER_MM)}",
           f"--screenshot={HERE / f'{out}.png'}", url)
    chrome("--no-pdf-header-footer", f"--print-to-pdf={HERE / f'{out}.pdf'}", url)


def static(name: str, port: int) -> None:
    """Rendered DOM with scripts removed, the stylesheet inlined and arrow markers flattened."""
    profile = Path(tempfile.gettempdir()) / "figchrome"
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={profile}",
                          "--virtual-time-budget=6000", "--dump-dom", f"http://127.0.0.1:{port}/{name}.html?static=1"],
                         check=True, capture_output=True, text=True, timeout=120).stdout
    assert 'data-ready="1"' in dom, f"{name} did not finish rendering"
    dom = re.sub(r"<script\b.*?</script>", "", dom, flags=re.S)
    css = (HERE / "figure.css").read_text()
    dom = re.sub(r'<link rel="stylesheet" href="figure.css">', f"<style>{css}</style>", dom)
    out = HERE / "figma" / f"{name}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text("<!doctype html>\n" + dom)
    print("static", out.relative_to(HERE), f"{len(dom) / 1024:.0f} kB")


if __name__ == "__main__":
    port = serve()
    args = sys.argv[1:]
    if args and args[0] == "--static":
        for name in args[1:] or ["fig1", "fig2"]:
            static(name, port)
        sys.exit()
    for name in args or sorted(p.stem for p in HERE.glob("fig*.html")):
        build(name, port)
        print("built", name)
