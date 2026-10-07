# Validation

The container builds and installs all four premade packages with node blanks intact. Building does not execute node callbacks. Maintainer checks validate package layout, Python syntax, nine blank IDs and matching lesson references, relative links, and the supplied safety controller.

Learner tests call the actual helper callback and comms node hooks; they intentionally fail until those blanks are filled. The simulation smoke test launches all three completed nodes and verifies the entire message/normalization/rpm/stop/watchdog flow. Virtual-CAN tests validate the supplied transport without hardware.

The one-hour plan assumes a ready development environment. Image downloads and physical hardware commissioning are separate. Native Pi hardware operation, Windows/macOS execution and arm64 execution need validation on those platforms; simulated success does not establish real motor stopping. No hardware validation is claimed.

Verified for the simplified exercise on Linux amd64: the Docker image built and installed all four packages with blanks intact; all 24 maintainer checks passed. A temporary completed copy outside the repository passed all 19 package tests and the full ROS simulation smoke test. The repository's nine blanks remain unfilled. Shell syntax, relative links and whitespace checks also passed.
