#!/bin/bash
cd /home/team/shared
for f in wc-*.md; do
  sed -i 's/At half-time,/Between periods,/g' "$f"
  sed -i 's/At half-time the/Between periods, the/g' "$f"
  sed -i 's/The second half starts/The next period starts/g' "$f"
  sed -i 's/The second half began/The next period began/g' "$f"
  sed -i 's/the second half\./the next period./g' "$f"
  sed -i 's/the second half,/the next period,/g' "$f"
  sed -i 's/the second half /the next period /g' "$f"
  sed -i 's/The second half\./The next period./g' "$f"
  sed -i 's/The second half,/The next period,/g' "$f"
  sed -i 's/The second half /The next period /g' "$f"
  echo "Fixed: $f"
done
grep -rn "half" wc-*.md
