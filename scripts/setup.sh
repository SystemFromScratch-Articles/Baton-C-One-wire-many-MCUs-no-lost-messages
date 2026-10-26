#!/usr/bin/env bash
# Initialize the west workspace around this repository and install the Python
# packages of the Zephyr build, twister and the documentation.
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

here="$(cd "$(dirname "$0")/.." && pwd)"
top="$(dirname "${here}")"

cd "${top}"
if ! west topdir >/dev/null 2>&1; then
    west init -l "${here}"
fi
west update -o=--depth=1 -n
pip install -r zephyr/scripts/requirements-base.txt \
            -r zephyr/scripts/requirements-build-test.txt \
            -r "${here}/requirements-docs.txt"
west zephyr-export
