#!/bin/sh
# utility for rsync-ing files from /testrig-src to /testrig
SELF="testrig-setup"

SRC_DIR="${SRC_DIR:-/testrig-src}"
DEST_DIR="${DEST_DIR:-/testrig}"

warn() {
  printf '%s %s %s\n' "$(date '+%FT%T')" "$SELF" "$*" >&2
}

main() {
  set -e

  warn "starting rsync from ${SRC_DIR} to ${DEST_DIR}"
  rsync -aqhHSXA --delete "$@" -- "${SRC_DIR}/." "${DEST_DIR}/."

  warn "done"
  true
}

main "$@"; exit
