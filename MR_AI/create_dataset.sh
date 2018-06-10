#!/usr/bin/env bash
cd /Users/chloewang/Downloads/Train_1
i=0
for x in *.jpg; do
  if [ "$i" = 9000 ]; then break; fi
  mv -- "$x" /Users/chloewang/Downloads/Train
  i=$((i+1))
done

#count=229
#for f in /Users/chloewang/Downloads/MRI_temp/*.nii.gz
#do
#    patientname=$(basename -- "$f" .nii.gz)
#    python /Users/chloewang/Desktop/get_slice.py "$f" "$count"
#    count=$((count+1))
#done