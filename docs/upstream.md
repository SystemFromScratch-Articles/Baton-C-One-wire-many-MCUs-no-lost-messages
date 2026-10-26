---
hide:
  - navigation
---

# Upstream status

Baton-C is developed in its own repository and proposed to the Zephyr project as an
**optional module**: a separate repository, listed in `submanifests/optional.yml` of
Zephyr, with its samples and tests inside the module and no dependency of Zephyr on it.
That is the integration mode Zephyr's
[external component process](https://docs.zephyrproject.org/latest/contribute/external.html)
provides for a library that no Zephyr subsystem depends on. A new module needs an RFC
issue and the approval of the Technical Steering Committee.

| Step | Status |
| --- | --- |
| Zephyr module in Baton-C (`zephyr/`), CI with twister | Done, in review in the Baton-C repository |
| Baton-C v1.1.0 release with the module | Planned |
| Bring-up on the M2S010 MKR Kit, measurements | In progress |
| RFC "New External Source Code" issue in Zephyr | Planned after the hardware results |
| Pull request adding Baton-C to `submanifests/optional.yml` | Planned with the RFC |
| Target Zephyr release | 4.6 (LTS, planned for April 2027) |

Zephyr releases follow a six-month cycle; Zephyr 4.5 is in its stabilization phase, in
which no new features are merged, so the earliest release that can include the module is
4.6.

This page is updated as the process moves; links to the issue and the pull request will
appear here.
