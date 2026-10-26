#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Render the link preview image of the article (1200x627, the size LinkedIn
shows) to docs/assets/images/social-card.png.

    pip install playwright && playwright install chromium
    python scripts/social_card.py
"""

from __future__ import annotations

import base64
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO = ROOT / "docs/assets/images/brand/systemfromscratch-logo-on-dark.png"
OUT = ROOT / "docs/assets/images/social-card.png"

NODES = [("MASTER", "0x01"), ("SLAVE", "0x11"), ("SLAVE", "0x12"), ("SLAVE", "0x13")]


def html() -> str:
    logo = base64.b64encode(LOGO.read_bytes()).decode()
    nodes = "".join(
        f'<div class="node{" master" if i == 0 else ""}"><span>{role}</span><b>{addr}</b></div>'
        for i, (role, addr) in enumerate(NODES)
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1200px; height: 627px; font-family: Inter, 'Segoe UI', 'DejaVu Sans', Arial, sans-serif;
  background: radial-gradient(circle at 85% 15%, #16365f 0%, #0B2545 45%, #071a33 100%); color: #fff;
  position: relative; overflow: hidden; }}
.grid {{ position: absolute; inset: 0; background-image:
  linear-gradient(rgba(201,214,234,.06) 1px, transparent 1px),
  linear-gradient(90deg, rgba(201,214,234,.06) 1px, transparent 1px); background-size: 40px 40px; }}
.wrap {{ position: absolute; inset: 0; padding: 56px 64px; display: flex; flex-direction: column; }}
.top {{ display: flex; align-items: center; justify-content: space-between; }}
.eyebrow {{ font-size: 20px; letter-spacing: .14em; text-transform: uppercase; color: #5fd0dc; font-weight: 700; }}
img.logo {{ height: 84px; }}
h1 {{ margin-top: 34px; font-size: 68px; line-height: 1.05; font-weight: 800; letter-spacing: -.01em; }}
h1 em {{ font-style: normal; color: #F29A2E; }}
p.sub {{ margin-top: 18px; font-size: 28px; color: #C9D6EA; }}
.bus {{ margin-top: auto; position: relative; height: 120px; }}
.wire {{ position: absolute; left: 0; right: 0; top: 92px; height: 6px; background: #E07A00; border-radius: 3px;
  box-shadow: 0 0 18px rgba(224,122,0,.55); }}
.nodes {{ position: absolute; left: 0; right: 0; top: 0; display: flex; justify-content: space-between; padding: 0 30px; }}
.node {{ width: 190px; height: 70px; border-radius: 12px; background: #F2F5FA; color: #0B2545;
  border: 2px solid #1E5AA8; display: flex; flex-direction: column; align-items: center; justify-content: center;
  position: relative; }}
.node::after {{ content: ""; position: absolute; left: 50%; top: 70px; width: 3px; height: 24px; background: #E07A00; }}
.node span {{ font-size: 14px; letter-spacing: .12em; color: #5A6472; font-weight: 700; }}
.node b {{ font-family: 'JetBrains Mono', 'DejaVu Sans Mono', monospace; font-size: 26px; }}
.node.master {{ background: #0F8B9A; color: #fff; border-color: #5fd0dc; }}
.node.master span {{ color: #dff6f8; }}
.chips {{ margin-top: 26px; display: flex; gap: 12px; }}
.chip {{ font-size: 19px; padding: 8px 16px; border-radius: 999px; border: 1.5px solid rgba(201,214,234,.45); color: #E6EEF8; }}
</style></head><body><div class="grid"></div><div class="wrap">
<div class="top"><div class="eyebrow">Zephyr RTOS module · open source</div><img class="logo" src="data:image/png;base64,{logo}"></div>
<h1>One wire, many MCUs,<br><em>no lost messages</em></h1>
<p class="sub">Baton-C as a Zephyr module: from a native_sim bus test to SmartFusion2</p>
<div class="bus"><div class="wire"></div><div class="nodes">{nodes}</div></div>
<div class="chips"><div class="chip">MISRA C:2012</div><div class="chip">No heap · no RTOS dependency</div>
<div class="chip">Devicetree</div><div class="chip">Exactly-once events</div></div>
</div></body></html>"""


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--disable-gpu"])
        page = browser.new_page(viewport={"width": 1200, "height": 627})
        page.set_content(html())
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT), timeout=60000)
        browser.close()
    print("written", OUT)


if __name__ == "__main__":
    main()
