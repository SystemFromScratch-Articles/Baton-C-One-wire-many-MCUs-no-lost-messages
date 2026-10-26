---
hide:
  - navigation
---

# Evidence

Every number of the article comes from the tables below. `scripts/test.sh` runs twister
(the `native_sim` bus test with five noise patterns and the build for the M2S010 MKR
Kit); `scripts/evidence.py` reads the twister reports and the firmware image and writes
`evidence/results.md` and `evidence/results.json`, included here unchanged.

--8<-- "evidence/results.md"

## Reading the noise columns

- **Moderate noise** flips one bit in about 1 of 150 bytes on the wire. The test requires
  every one of 200 events (100 in each direction) to arrive exactly once and in order,
  and no event to be reported lost.
- **Heavy noise** flips one bit in about 1 of 40 bytes. The test requires that no event is
  duplicated or reordered, and that *delivered + reported lost ≥ sent* in both
  directions: every event either arrives or its sender is told. An event whose
  acknowledgement was destroyed is delivered *and* reported, so the sum may exceed 100.
- CRC errors are counted by all three nodes, so one corrupted byte can be counted more
  than once (every node that hears the frame rejects it).

The raw twister report is `evidence/twister_report.xml`; hardware captures will be added
to `evidence/hardware/`.
