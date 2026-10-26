---
hide:
  - navigation
---

# Reproduce

## With the dev container (recommended)

Requirements: Docker and VS Code with the Dev Containers extension.

1. Clone the repository and open it in VS Code.
2. Run **Dev Containers: Reopen in Container**. The first start builds the image (Zephyr
   SDK 1.0.1 with the Arm toolchain only, west, Python 3.13) and runs
   `scripts/setup.sh`, which creates the west workspace around the repository, fetches
   Zephyr and Baton-C, and installs the Python packages.
3. Run the task **Article: Run tests (twister)**, or in the terminal:

```bash
scripts/test.sh
python scripts/evidence.py
```

The west workspace and the compiler cache live in Docker volumes, so rebuilding the
container does not download Zephyr again.

## With a local Zephyr setup

Requirements: the [Zephyr getting started](https://docs.zephyrproject.org/latest/develop/getting_started/index.html)
prerequisites, Python 3.12 or later, and Zephyr SDK 1.0.

```bash
mkdir baton-article && cd baton-article
git clone https://github.com/SystemFromScratch-Articles/Baton-C-One-wire-many-MCUs-no-lost-messages article
west init -l article
west update -o=--depth=1 -n
pip install -r zephyr/scripts/requirements-base.txt -r zephyr/scripts/requirements-build-test.txt
article/scripts/test.sh
python article/scripts/evidence.py
```

## What gets pinned

| Component | Version | Where |
| --- | --- | --- |
| Zephyr | `main` until v4.5.0 is tagged (the M2S010 MKR Kit is new in 4.5) | `west.yml` |
| Baton-C | the branch with the Zephyr module until v1.1.0 is tagged | `west.yml` |
| Zephyr SDK | 1.0.1, Arm toolchain only | `Dockerfile` |
| west | 1.5.0 | `Dockerfile` |

## Building and flashing the board

```bash
west build -b m2s010_mkr_kit/m2s010 modules/lib/baton-c/zephyr/samples/baton_node
west flash --runner openocd
```

The sample is slave 0x12 of the example bus on MSS UART1. The FPGA design must route
MSS UART1 to the pins of the bus (see [Hardware](hardware.md)). A PC can be the master:
`examples/host_serial` of Baton-C uses the same message lists.

## Previewing this website

```bash
pip install -r requirements-docs.txt
mkdocs serve
```
