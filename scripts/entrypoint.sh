#!/usr/bin/env bash
set -euo pipefail

mode="${1:-all}"

case "$mode" in
  all)
    set +e
    echo "=== Requesting ChatGPT export ==="
    /app/scripts/run_export.sh
    chatgpt_exit=$?
    echo ""
    echo "=== Requesting Claude export ==="
    /app/scripts/run_claude_export.sh
    claude_exit=$?
    set -e
    echo ""
    if [ "$chatgpt_exit" -ne 0 ] || [ "$claude_exit" -ne 0 ]; then
      echo "One or more exports failed (chatgpt=$chatgpt_exit, claude=$claude_exit)" >&2
      exit 1
    fi
    ;;
  request)
    exec /app/scripts/run_export.sh
    ;;
  bootstrap)
    exec /app/scripts/bootstrap_profile.sh
    ;;
  claude-request)
    exec /app/scripts/run_claude_export.sh
    ;;
  claude-bootstrap)
    exec /app/scripts/bootstrap_claude_profile.sh
    ;;
  *)
    echo "Unknown mode: $mode" >&2
    echo "Valid modes: all, request, bootstrap, claude-request, claude-bootstrap" >&2
    exit 2
    ;;
esac
