#!/bin/sh
# utility for rsync-ing files from /testrig-src to /testrig
SELF="$(basename "$0")"

SRC_DIR="${SRC_DIR:-/testrig-src}"
DEST_DIR="${DEST_DIR:-/testrig}"

warn() {
  printf '%s %s %s\n' "$(date '+%FT%T')" "$SELF" "$*" >&2
}

die() {
  warn "FATAL:" "$@"
  exit 1
}

main() {
  set -e

  warn "==> starting rsync from ${SRC_DIR} to ${DEST_DIR}"
  rsync -avhHP8SXA --delete "${SRC_DIR}/." "${DEST_DIR}/."

  warn "DONE"
  exit 0
}

main "$@"; exit