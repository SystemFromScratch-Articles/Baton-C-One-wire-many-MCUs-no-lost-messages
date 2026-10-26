#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the SVG diagrams of the article (same palette and font as the
Baton-C documentation diagrams).

    python scripts/diagrams.py
"""

from __future__ import annotations

import pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets" / "images"

FONT = "Inter, 'Segoe UI', 'DejaVu Sans', Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'DejaVu Sans Mono', monospace"
NAVY, BLUE, TEAL, ORANGE, GREEN = "#0B2545", "#1E5AA8", "#0F8B9A", "#E07A00", "#2E7D32"
GREY, PALE, PALE_TEXT, WHITE = "#5A6472", "#F2F5FA", "#C9D6EA", "#FFFFFF"


class Svg:
    def __init__(self, width: int, height: int, title: str):
        self.w, self.h = width, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" aria-label="{escape(title)}">',
            f"<title>{escape(title)}</title>",
            "<defs>"
            + "".join(
                f'<marker id="arrow-{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
                f'fill="{c}"/></marker>'
                for n, c in (("grey", GREY), ("teal", TEAL), ("orange", ORANGE), ("blue", BLUE))
            )
            + "</defs>",
            f'<rect x="0" y="0" width="{width}" height="{height}" rx="12" fill="{WHITE}"/>',
        ]

    def box(self, x, y, w, h, fill=PALE, stroke=BLUE, rx=10, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.5"{d}/>'
        )

    def text(self, x, y, s, size=13, weight="normal", fill=NAVY, anchor="middle", mono=False):
        family = MONO if mono else FONT
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'
        )

    def line(self, x1, y1, x2, y2, color=GREY, arrow="grey", width=1.6, dash=None, both=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        start = f' marker-start="url(#arrow-{arrow})"' if both and arrow else ""
        end = f' marker-end="url(#arrow-{arrow})"' if arrow else ""
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}"{d}{start}{end}/>'
        )

    def save(self, name: str):
        self.parts.append("</svg>")
        (OUT / name).write_text("\n".join(self.parts) + "\n", encoding="utf-8")


def integration():
    s = Svg(980, 520, "Baton-C as a Zephyr module: layers and data flow")
    # Left: build-time inputs
    s.text(130, 40, "BUILD TIME", 12, "bold", GREY)
    s.box(30, 60, 200, 120, PALE, TEAL)
    s.text(130, 86, "Devicetree", 15, "bold")
    s.text(130, 108, "&uart1 { baton0: baton {", 11, mono=True, fill=GREY)
    s.text(130, 126, 'role = "slave";', 11, mono=True, fill=GREY)
    s.text(130, 144, "address = <0x12>; ... } }", 11, mono=True, fill=GREY)
    s.text(130, 166, "one device per node", 12, fill=TEAL)
    s.box(30, 200, 200, 90, PALE, TEAL)
    s.text(130, 226, "Kconfig", 15, "bold")
    s.text(130, 248, "CONFIG_BATON (auto)", 11, mono=True, fill=GREY)
    s.text(130, 266, "stack, priority, period", 12, fill=GREY)
    s.box(30, 310, 200, 90, PALE, TEAL)
    s.text(130, 336, "baton_user_config.h", 14, "bold")
    s.text(130, 358, "message lists, sizes", 12, fill=GREY)
    s.text(130, 376, "identical on every node", 12, fill=GREY)
    for y in (120, 245, 355):
        s.line(232, y, 300, y, TEAL, "teal", dash="5 4")

    # Middle: the stack
    s.text(560, 40, "RUN TIME", 12, "bold", GREY)
    s.box(310, 60, 500, 56, NAVY, NAVY)
    s.text(560, 85, "Application", 16, "bold", WHITE)
    s.text(560, 105, "baton_zephyr_send() · publish() · callbacks", 12, fill=PALE_TEXT)
    s.box(310, 140, 500, 120, PALE, BLUE)
    s.text(560, 162, "Baton-C Zephyr module  (zephyr/baton_zephyr.c)", 14, "bold")
    s.box(330, 176, 220, 70, WHITE, BLUE, 8)
    s.text(440, 200, "Protocol thread", 13, "bold")
    s.text(440, 220, "baton_node_process()", 11, mono=True, fill=GREY)
    s.text(440, 237, "k_sem wake · 1 ms period", 11, fill=GREY)
    s.box(570, 176, 220, 70, WHITE, BLUE, 8)
    s.text(680, 200, "UART interrupt", 13, "bold")
    s.text(680, 220, "rx → baton_node_rx_isr()", 11, mono=True, fill=GREY)
    s.text(680, 237, "tx FIFO fill · echo → DE off", 11, fill=GREY)
    s.box(310, 284, 500, 56, WHITE, BLUE)
    s.text(560, 308, "Baton-C core  (src/, MISRA C:2012, no heap)", 14, "bold")
    s.text(560, 328, "schedule · TLV packing · ACK/retry · dedup · TTL", 12, fill=GREY)
    s.box(310, 364, 500, 50, PALE, GREY)
    s.text(560, 394, "Zephyr UART driver  (interrupt-driven API, e.g. ns16550)", 13)
    s.line(560, 118, 560, 138, GREY, "grey")
    s.line(440, 248, 440, 282, GREY, "grey", both=True)
    s.line(680, 248, 680, 282, GREY, "grey", both=True)
    s.line(680, 362, 680, 342, GREY, "grey")
    s.line(560, 416, 560, 452, ORANGE, "orange", 2.2, both=True)
    s.parts.append(f'<line x1="250" y1="468" x2="870" y2="468" stroke="{ORANGE}" stroke-width="4"/>')
    s.text(560, 495, "one shared wire: single-wire UART, open drain or RS-485 with echo", 13, "bold", ORANGE)

    # Right: lock
    s.box(830, 140, 130, 120, PALE, GREEN, dash="5 4")
    s.text(895, 166, "k_spinlock", 13, "bold", GREEN)
    s.text(895, 188, "per node", 12, fill=GREY)
    s.text(895, 212, "ISR + send/", 12, fill=GREY)
    s.text(895, 230, "publish from", 12, fill=GREY)
    s.text(895, 248, "any thread", 12, fill=GREY)
    s.save("zephyr-integration.svg")


def test_bus():
    s = Svg(980, 430, "Three Baton nodes on one emulated wire in a native_sim image")
    s.box(20, 20, 940, 390, "#FAFBFD", GREY, 12, dash="6 5")
    s.text(40, 46, "one native_sim executable  (zephyr/tests/bus)", 13, "bold", GREY, "start")
    nodes = (("Master 0x01", "uart-emul-0", 150), ("Slave 0x11", "uart-emul-1", 490),
             ("Slave 0x12", "uart-emul-2", 830))
    for name, uart, x in nodes:
        s.box(x - 120, 70, 240, 70, NAVY, NAVY)
        s.text(x, 98, name, 16, "bold", WHITE)
        s.text(x, 120, "Baton module device + thread", 12, fill=PALE_TEXT)
        s.box(x - 90, 160, 180, 44, PALE, BLUE, 8)
        s.text(x, 187, f"zephyr,{uart}", 12, mono=True)
        s.line(x, 142, x, 158, GREY, "grey", both=True)
        s.line(x, 206, x, 262, ORANGE, "orange", 2, both=True)
    s.parts.append(f'<line x1="60" y1="280" x2="920" y2="280" stroke="{ORANGE}" stroke-width="4"/>')
    s.text(490, 304, "test wire: every byte to every connected node, sender included (echo)",
           12, "bold", ORANGE)
    s.box(250, 326, 220, 62, WHITE, ORANGE, 8)
    s.text(360, 350, "Noise injector", 13, "bold", ORANGE)
    s.text(360, 370, "flip 1 bit in 1/N bytes (seeded)", 11, fill=GREY)
    s.box(510, 326, 220, 62, WHITE, ORANGE, 8)
    s.text(620, 350, "Disconnect switch", 13, "bold", ORANGE)
    s.text(620, 370, "cut one node off the bus", 11, fill=GREY)
    s.save("native-sim-bus.svg")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    integration()
    test_bus()
    print("diagrams written to", OUT)
