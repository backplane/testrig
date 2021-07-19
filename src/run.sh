#!/bin/sh
# activate venv, start the testrig

VENV="$(dirname "$0")/venv"
TESTRIG="$(dirname "$0")/testrig.py"

. "${VENV}/bin/activate"
exec "$TESTRIG" "$@"
