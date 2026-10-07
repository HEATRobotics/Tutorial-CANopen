# Validation boundaries

This repository intentionally ships unfinished exercises. Maintainer checks validate Python syntax, package names, blank/lesson coverage, relative links, and the supplied drive safety support. Learner tests require completed code and intentionally fail on unfilled TODO calls. Interface generation intentionally fails until I01/I02 are completed.

The Docker image builds the Humble development environment without building the unfinished exercises. The full pipeline smoke test launches completed learner nodes in simulation and checks the custom message, helper normalization, rpm mixing, stopping, and upstream-loss watchdog. The virtual SDO test checks transport encoding/sequencing without hardware.

Windows/macOS Docker Desktop execution, arm64 Pi execution, physical adapters, ESCON2 commissioning, and real motor stopping require platform/bench validation. No physical hardware validation is claimed. GitHub workflow execution requires pushing these files; no workflow run or lesson checkpoint tags have been published by this change.

## Results from this rewrite

Verified on Linux amd64 in this workspace, 2026-10-06:

- 24 maintainer checks passed, including the supplied controller regressions.
- Relative documentation links, Python syntax, shell syntax, and whitespace checks passed.
- The redesigned Humble development image built successfully.
- In a temporary workspace outside the repository, the documented `ros2 pkg create` commands created all four packages. A completed copy of the starter overlays generated the custom interface and built all packages with colcon.
- All 16 learner tests passed in that temporary completed workspace, including live virtual-CAN SDO request/response testing of the student transport.
- The complete ROS simulation smoke test passed: raw custom message, helper clamping, four-motor rpm mapping, normal stop, and latched upstream-loss watchdog.

The temporary completed copy was used only for validation; the repository still ships numbered blanks and an empty learner workspace. This does not establish Windows/macOS/arm64 or physical bench validation.
