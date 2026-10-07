# Contributing

Keep the repository a learner exercise. `exercises/` contains starter overlays with numbered blanks; `ros2_ws/src/` starts empty so learners create their own four packages. Do not commit completed learner packages or an answer key to main.

Use descriptive branches such as `docs/explain-normalization`, `fix/sdo-stop`, or `learn/lesson-03`. Open a PR against main. Main requires one approving review and resolved conversations; approvals are dismissed on new commits, force pushes/deletion are blocked, and administrators have no bypass.

Run `bash scripts/check_template.sh` for scaffold/supplied-support checks. Build the Docker image after dependency changes. Learner tests intentionally fail until the corresponding blanks are completed; run them in a separate completed workspace when validating lesson changes. Keep hardware validation separate from simulation results.

Each blank needs a matching lesson entry, reference link, expected behavior, and a completion check. Treat the supplied drive-state, watchdog, fault-latching, and shutdown code as reviewed support. Any change there needs regression tests and a hardware impact review before bench use. Do not publish untested wiring or claim hardware validation from simulation tests.
