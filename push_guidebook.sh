#!/bin/bash
cd /home/team/shared && git add wc-guidebook.md && git commit -m "Final guidebook manuscript" && git push origin main 2>&1 | tail -3