#!/usr/bin/env bash
# Everything the article reports from a PC: the three-node bus test on
# native_sim (five noise patterns) and the sample built for the M2S010 MKR Kit.
# Reports land in twister-out/ of the west workspace; scripts/evidence.py
# turns them into the tables of the article.
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

top="$(west topdir)"
cd "${top}"
west twister -T modules/lib/baton-c/zephyr \
    -p native_sim/native/64 -p m2s010_mkr_kit/m2s010 \
    --inline-logs --outdir "${top}/twister-out" "$@"
