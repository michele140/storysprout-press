#!/bin/bash
cd /home/team/shared && git add wc2026-activity-book-kdp.pdf && git commit -m "Activity Book PDF for owner review" && git push origin main 2>&1 | tail -3