#!/bin/bash
# Double-click to run Job Hunter on Mac.
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Install Python from https://www.python.org/downloads/"; read -r; exit 1; }
if [ ! -f config.json ]; then
  cp config.example.json config.json
  echo "Created config.json. Fill it in with your info, save it, then double-click run.command again."
  open -e config.json
  exit 0
fi
python3 -m pip install -q -r requirements.txt
python3 hunt.py
open "output/$(date +%F)"
