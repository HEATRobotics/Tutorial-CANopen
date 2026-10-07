# Contributing

Keep this a one-hour exercise with four premade packages in `ros2_ws/src`. Only three `node.py` files contain learner blanks: M01–M03, H01–H03, C01–C03. Do not commit completed answers to those files on main. Interface generation, metadata, CAN transport and safety runtime are supplied.

Run `bash scripts/check_template.sh` for scaffold and supplied-support checks. Build the Docker image to verify all packages install with the blanks intact. Validate learner code in a temporary completed copy with the 19 package tests and `scripts/smoke_pipeline.py`. These completed-node tests intentionally fail against unfilled blanks.

Keep native Pi deployment matching Autobot; desktop containers are for development/simulation. Document hardware validation separately. Use a descriptive branch and PR against main; existing review and branch protections apply.
