#!/bin/bash
# SessionStart hook for Claude Code on the web.
#
# The repo currently has no dependency manifests, linters, or tests to set up.
# What web sessions do need is the user's login environment: ~/.zshrc sources
# ~/.local/bin/env, which puts ~/.local/bin on PATH. Non-login/non-interactive
# hook shells don't read ~/.zshrc, so we reproduce that here.
#
# Note: PATH changes made inside this hook process do NOT survive into the
# session. Only what we append to $CLAUDE_ENV_FILE is sourced by the session,
# so PATH must be persisted there.
#
# Idempotent and non-interactive. As the repo grows, add dependency install
# steps (npm install, pip install, etc.) below the environment setup.
set -euo pipefail

# Only run in the remote (Claude Code on the web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Persist ~/.local/bin on PATH for the whole session via $CLAUDE_ENV_FILE.
# The exported line is self-guarding (it only prepends if not already present),
# and we also dedupe against the env file so repeated SessionStart events
# (resume/compact) don't append it more than once.
if [ -n "${CLAUDE_ENV_FILE:-}" ] && [ -d "$HOME/.local/bin" ]; then
  path_line='case ":$PATH:" in *:"'"$HOME"'/.local/bin":*) ;; *) export PATH="'"$HOME"'/.local/bin:$PATH" ;; esac'
  if ! grep -qF -- "$path_line" "$CLAUDE_ENV_FILE" 2>/dev/null; then
    echo "$path_line" >> "$CLAUDE_ENV_FILE"
  fi
fi
