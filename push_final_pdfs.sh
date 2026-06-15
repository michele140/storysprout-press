#!/bin/bash
cd /home/team/shared && git add wc10-seattle-kdp.pdf wc11-boston-kdp.pdf && git commit -m "Seattle + Boston PDFs - WC series complete!" && git push origin main 2>&1 | tail -3