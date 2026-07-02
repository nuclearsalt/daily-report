#!/usr/bin/env python3
"""Invoke CC CLI with the briefing prompt, bypassing shell variable expansion issues."""
import os
import subprocess
import sys

with open('scripts/briefing-prompt.md') as f:
    prompt = f.read()

result = subprocess.run(
    [
        'claude',
        '--dangerously-skip-permissions',
        '--allowedTools', 'Bash,Read,Write,WebSearch,WebFetch',
        '-p', prompt,
    ],
    env=os.environ.copy(),
)
sys.exit(result.returncode)
