#!/usr/bin/env python3
"""Archive yesterday's briefing and regenerate archive/index.html."""
import glob
import os
import shutil
import subprocess
from datetime import date, timedelta

# Use the last git commit date for index.html as the archive filename.
# This correctly labels missed-day gaps instead of always using "yesterday".
result = subprocess.run(
    ['git', 'log', '-1', '--format=%as', '--', 'index.html'],
    capture_output=True, text=True
)
archive_date = result.stdout.strip()
if not archive_date:
    archive_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

dest = f'archive/{archive_date}.html'

if not os.path.exists('index.html'):
    print('No index.html found — skipping archive')
elif os.path.exists(dest):
    print(f'{dest} already exists — skipping')
else:
    shutil.copy('index.html', dest)
    print(f'Archived to {dest}')

# Regenerate archive/index.html from local filesystem
files = sorted(
    [os.path.basename(f) for f in glob.glob('archive/*.html')
     if os.path.basename(f) != 'index.html'],
    reverse=True
)

rows = '\n'.join(
    f'    <li><a href="{f}">{f[:-5]}</a></li>' for f in files
) or '    <li>No archived briefings yet.</li>'

TEMPLATE = (
    "<!doctype html>\n"
    "<html lang=\"en\">\n"
    "<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
    "<title>John’s Daily Briefing — Archive</title>\n"
    "<style>\n"
    "  body { background:#0f0f0f; color:#e0e0e0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; max-width:800px; margin:0 auto; padding:2rem 1.25rem; line-height:1.6; }\n"
    "  h1 { margin:0 0 .25rem; font-size:1.6rem; }\n"
    "  p.sub { color:#888; margin:0 0 2rem; }\n"
    "  ul { list-style:none; padding:0; margin:0; }\n"
    "  li { padding:.5rem 0; border-bottom:1px solid #222; }\n"
    "  a { color:#9ecbff; text-decoration:none; }\n"
    "  a:hover { text-decoration:underline; }\n"
    "  .home { display:inline-block; margin-bottom:1.5rem; color:#888; }\n"
    "</style>\n"
    "</head>\n"
    "<body>\n"
    "  <a class=\"home\" href=\"../\">← Today’s briefing</a>\n"
    "  <h1>Archive</h1>\n"
    "  <p class=\"sub\">All past daily briefings, newest first.</p>\n"
    "  <ul>\n"
    "ROWS\n"
    "  </ul>\n"
    "</body>\n"
    "</html>"
)

with open('archive/index.html', 'w') as f:
    f.write(TEMPLATE.replace('ROWS', rows))

print(f'Archive index updated ({len(files)} entries)')
