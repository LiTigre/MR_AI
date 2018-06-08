#!/usr/bin/env bash
cd /Users/chloewang/Downloads/MRI_data
i=0
for x in *; do
  if [ "$i" = 360 ]; then break; fi
  mv -- "$x" /Users/chloewang/Downloads/MRI_temp
  i=$((i+1))
done

count=0
for f in /Users/chloewang/Downloads/MRI_temp/*.nii.gz
do
    patientname=$(basename -- "$f" .nii.gz)
    python /Users/chloewang/Desktop/get_slice.py "$f" "$count"
    count=$((count+1))
done