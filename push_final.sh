#!/bin/bash
cd /home/team/shared
git add wc2026-guidebook-kdp.pdf make_guidebook.py
git commit -m "Final guidebook PDF with photorealistic graphics"
git push origin main 2>&1 | tail -3
echo "DONE"