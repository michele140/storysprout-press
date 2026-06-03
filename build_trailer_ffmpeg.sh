#!/bin/bash
set -e
# Direct shell script to assemble the trailer video from pre-made segments

TMP=/tmp/trailer_build
OUT=/home/team/shared/little-cloud-trailer.mp4

echo "Step 1: Creating concat list..."
cd "$TMP"
rm -f concat_list.txt
for f in seg_*.mp4; do
  echo "file '$PWD/$f'" >> concat_list.txt
done
echo "  Found $(wc -l < concat_list.txt) segments"

echo "Step 2: Concatenating video segments..."
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy concat_raw.mp4 2>&1 | tail -2
echo "  Concat done: $(ls -lh concat_raw.mp4 | awk '{print $5}')"

echo "Step 3: Adding fade transitions..."
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 concat_raw.mp4)
echo "  Duration: ${DUR}s"
ffmpeg -y -i concat_raw.mp4 -vf "fade=t=in:st=0:d=0.8,fade=t=out:st=$(echo "$DUR - 0.8" | bc):d=0.8" \
  -af "afade=t=in:st=0:d=0.8,afade=t=out:st=$(echo "$DUR - 0.8" | bc):d=0.8" \
  concat_faded.mp4 2>&1 | tail -2
echo "  Fades done"

echo "Step 4: Adding background music..."
MUSIC="$TMP/music.aac"
if [ -f "$MUSIC" ]; then
  ffmpeg -y -i concat_faded.mp4 -i "$MUSIC" \
    -filter_complex "[1:a]volume=0.3[a1]" \
    -map 0:v:0 -map "[a1]" -c:v libx264 -preset medium -crf 23 \
    -c:a aac -b:a 128k -shortest "$OUT" 2>&1 | tail -3
else
  cp concat_faded.mp4 "$OUT"
fi

echo "Step 5: Final output"
ls -lh "$OUT"
echo "DONE: $OUT"