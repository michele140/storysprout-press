#!/bin/bash
cd /home/team/shared && python3 make_guidebook.py 2>&1
git add make_guidebook.py wc2026-guidebook-kdp.pdf
git commit -m "Fixed: photos not stretched, text fills column, extra spacing"
git push origin main 2>&1 | tail -3