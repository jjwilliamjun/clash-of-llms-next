#!/usr/bin/env bash
#
# Runs the Flask API on its own.
#
# The frontend is a separate process: start it in another terminal with `npm run serve`.
# Running both from one script meant Ctrl+C stopped only the foreground one and left the
# other orphaned, and neither could be restarted without killing both.
#
# FLASK_APP is exported here rather than expected from the environment because the module
# path is relative to this directory. The cd is not cosmetic either -- /cleanup shells out
# to ./cleanup.sh with a relative path, so Flask has to be started from here.

set -euo pipefail
cd "$(dirname "$0")"

export FLASK_APP=flask_app/simulation_endpoint.py
# FLASK_ENV was deprecated in Flask 2.3; FLASK_DEBUG is the supported spelling and works
# on the pinned 2.2.3 as well.
export FLASK_DEBUG=1

exec flask run --port "${FLASK_PORT:-5000}"
