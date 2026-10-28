#!/bin/bash
# SessionStart hook for Claude Code on the web.
#
# Two jobs:
#  1. Reproduce the login environment. ~/.zshrc sources ~/.local/bin/env, which
#     puts ~/.local/bin on PATH. Non-login/non-interactive hook shells don't read
#     ~/.zshrc, so we persist that PATH entry via $CLAUDE_ENV_FILE (changes to
#     PATH inside this hook process do NOT survive into the session; only the env
#     file is sourced by it).
#  2. Install the Node/TS dependencies (npm install) so `npm run build`,
#     `typecheck`, and `config:check` work in the session.
#
# Idempotent and non-interactive.
set -euo pipefail

# Async mode: the hook runs in the background while the session starts, so
# startup latency is not blocked on it. Trade-off: the session may begin before
# this finishes, so commands that depend on the hook's work (the persisted PATH
# below, or node_modules from npm install) can race with the first few commands
# of the session until the install completes.
echo '{"async": true, "asyncTimeout": 300000}'

# Only run in the remote (Claude Code on the web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# --- 1. Persist ~/.local/bin on PATH for the whole session via $CLAUDE_ENV_FILE.
# The exported line is self-guarding (it only prepends if not already present),
# and we also dedupe against the env file so repeated SessionStart events
# (resume/compact) don't append it more than once.
if [ -n "${CLAUDE_ENV_FILE:-}" ] && [ -d "$HOME/.local/bin" ]; then
  path_line='case ":$PATH:" in *:"'"$HOME"'/.local/bin":*) ;; *) export PATH="'"$HOME"'/.local/bin:$PATH" ;; esac'
  if ! grep -qF -- "$path_line" "$CLAUDE_ENV_FILE" 2>/dev/null; then
    echo "$path_line" >> "$CLAUDE_ENV_FILE"
  fi
fi

# --- 2. Install Node dependencies.
# Prefer `npm install` over `npm ci` so repeated runs reuse the cached
# node_modules that the container snapshots after the hook completes.
project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
if [ -f "$project_dir/package.json" ]; then
  npm install --prefix "$project_dir" --no-audit --no-fund
fi
