#!/bin/bash
cd /home/team/shared
for f in make_wc*.py; do
  sed -i "s/At half-time,/Between periods,/g" "$f"
  sed -i "s/The second half began/The next period began/g" "$f"
  sed -i "s/The second half started/The next period started/g" "$f"
  sed -i "s/The second half brought/The next period brought/g" "$f"
  sed -i "s/The second half was/The next period was/g" "$f"
  sed -i "s/the second half\./the next period./g" "$f"
  sed -i "s/the second half,/the next period,/g" "$f"
  echo "Fixed: $f"
done
echo "--- Checking remaining half refs ---"
grep -rn "half" make_wc*.py