#!/bin/bash

# Run all tests in the `tests` directory.
# Add -k <pattern> to only run tests whose name contains <pattern>.
# Add -rP option shows captures stdout for tests even if they pass.
#   Normally stdout is only shown for failed tests.
pytest tests
