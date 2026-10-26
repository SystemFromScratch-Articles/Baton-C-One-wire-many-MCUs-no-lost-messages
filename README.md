# One wire, many MCUs, no lost messages — Baton-C on Zephyr

[![Evidence](https://github.com/SystemFromScratch-Articles/Baton-C-One-wire-many-MCUs-no-lost-messages/actions/workflows/ci.yml/badge.svg)](https://github.com/SystemFromScratch-Articles/Baton-C-One-wire-many-MCUs-no-lost-messages/actions/workflows/ci.yml)
[![Pages](https://github.com/SystemFromScratch-Articles/Baton-C-One-wire-many-MCUs-no-lost-messages/actions/workflows/pages.yml/badge.svg)](https://github.com/SystemFromScratch-Articles/Baton-C-One-wire-many-MCUs-no-lost-messages/actions/workflows/pages.yml)

**Read the article:** https://systemfromscratch-articles.github.io/Baton-C-One-wire-many-MCUs-no-lost-messages/

This repository is the article and everything needed to reproduce it:
[Baton-C](https://github.com/AntonVynohradov/Baton-C), a deterministic single-wire UART
bus in MISRA C, integrated into [Zephyr](https://zephyrproject.org/) as a module, tested as
a three-node bus with line noise on `native_sim`, and brought up on a Microchip
SmartFusion2 board (M2S010 MKR Kit).

The module itself lives in the Baton-C repository (`zephyr/`); this repository pins it,
runs it, and publishes the results.

## Contents

| Path | Content |
| --- | --- |
| `docs/` | The article and its pages (MkDocs Material), published to GitHub Pages |
| `west.yml` | West workspace: Zephyr and Baton-C, pinned |
| `scripts/test.sh` | Runs the bus test on `native_sim` (five noise patterns) and builds the sample for the board |
| `scripts/evidence.py` | Turns the twister reports into the tables of the article (`evidence/`) |
| `scripts/diagrams.py`, `scripts/social_card.py` | Generate the diagrams and the link preview image |
| `evidence/` | Results quoted by the article; hardware captures go to `evidence/hardware/` |
| `hardware/` | Bench setup, wiring and the Libero design notes |
| `Dockerfile`, `.devcontainer/` | Reproducible environment: Zephyr SDK 1.0.1 (Arm only), west, Python 3.13 |

## Quick start

```bash
mkdir baton-article && cd baton-article
git clone https://github.com/SystemFromScratch-Articles/Baton-C-One-wire-many-MCUs-no-lost-messages article
west init -l article && west update -o=--depth=1 -n
pip install -r zephyr/scripts/requirements-base.txt -r zephyr/scripts/requirements-build-test.txt
article/scripts/test.sh && python article/scripts/evidence.py
```

Or open the repository in VS Code and choose **Reopen in Container**. Details:
[Reproduce](docs/reproduce.md).

The environment is derived from
[Zephyr-SmartFusion2-workspace](https://github.com/AntonVynohradov/Zephyr-SmartFusion2-workspace),
updated for Zephyr 4.5 (Python 3.12+, Zephyr SDK 1.0).

## Author

**Anton Vynohradov** — Embedded Systems Engineer · Founder of SystemFromScratch®
· ORCID [0009-0005-6965-0911](https://orcid.org/0009-0005-6965-0911)
· [LinkedIn](https://www.linkedin.com/in/vynohradov) · [GitHub](https://github.com/AntonVynohradov)

## License

Code and text: [Apache License 2.0](LICENSE). SystemFromScratch® is a registered trademark;
the license grants no rights to use the name or logo.
