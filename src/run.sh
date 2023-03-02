#!/bin/sh
# activate venv, start the testrig
# shellcheck disable=SC1091

VENV=$(dirname "$0")/venv
TESTRIG=$(dirname "$0")/testrig.py

. "${VENV}/bin/activate"
exec "$TESTRIG" "$@"
