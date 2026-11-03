#!/usr/bin/env bash
# Source this file; PATH changes apply only to the calling project shell/process.
if command -v node >/dev/null 2>&1; then
  if node -e 'const n=+process.versions.node.split(".")[0];process.exit(n===22||n===24?0:1)' >/dev/null 2>&1; then
    return 0
  fi
fi
if [ -x /Users/cuing/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node ]; then
  export PATH="/Users/cuing/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:$PATH"
fi
if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  echo "Node.js/npm missing. Install Node 24 LTS or select it with your version manager." >&2
  return 1
fi
# Package engines also enforce the precise minor version at installation.
node -e 'const n=+process.versions.node.split(".")[0];if(n!==22&&n!==24){console.error("Use Node 22/24 LTS; no global environment was modified.");process.exit(1)}'
