#!/bin/bash
cd /home/team/shared && git add make_guidebook.py wc2026-guidebook-kdp.pdf && git commit -m "Guidebook: full info, bolder fonts, all 11 stadiums" && git push origin main 2>&1 | tail -3