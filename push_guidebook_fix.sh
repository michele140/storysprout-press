#!/bin/bash
cd /home/team/shared && git add make_guidebook.py && git commit -m "Fixed guidebook: real player stats, no overlay, tighter layout" && git push origin main 2>&1 | tail -3