#!/bin/bash
cd /home/team/shared && python3 make_guidebook.py 2>&1
echo "---"
echo "Pushing..."
git add make_guidebook.py wc2026-guidebook-kdp.pdf
git commit -m "Guidebook: balanced layout, full text fills area"
git push origin main 2>&1 | tail -3