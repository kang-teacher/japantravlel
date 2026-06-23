#!/bin/bash
set -e

if [ -z "$CLAUDE_API_KEY" ]; then
  echo "Warning: CLAUDE_API_KEY is not set. Skipping key injection."
  exit 0
fi

python3 - "$CLAUDE_API_KEY" <<'EOF'
import sys

key = sys.argv[1]
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("__CLAUDE_API_KEY__", key)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Claude API key injected successfully.")
EOF
