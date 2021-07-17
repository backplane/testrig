#!/bin/sh
# utility for running python testing utilities installed under /testrig/venv
SELF="$(basename "$0")"

VENV="$(dirname "$0")/venv"

warn() {
  printf '%s %s %s\n' "$(date '+%FT%T')" "$SELF" "$*" >&2
}

die() {
  warn "FATAL:" "$@"
  exit 1
}

main() {
  set -e

  warn "loading virtualenv"
  . "${VENV}/bin/activate"

  warn "==> black"
  black --check .

  warn "==> isort"
  isort --check .

  warn "==> pylint"
  pylint -- ./*.py

  warn "==> flake8"
  flake8 .

  warn "==> mypy"
  mypy --ignore-missing-imports .

  warn "==> bandit"
  bandit -r . -x ./venv

  warn "ALL CHECKS PASSED"
  exit 0
}

main "$@"; exit