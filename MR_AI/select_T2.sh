#!/usr/bin/env bash
mv /Users/chloewang/Downloads/*_3T_Structural_unproc.zip /Users/chloewang/Downloads/MRI_temp/
for f in /Users/chloewang/Downloads/MRI_temp/*.zip; do unzip -d "${f%*.zip}" "$f"; done
mv /Users/chloewang/Downloads/MRI_temp/*/*/unprocessed/3T/T2w_SPC*/*3T_T2w*.nii.gz /Users/chloewang/Downloads/MRI_1000_T2/
rm -R -- /Users/chloewang/Downloads/MRI_temp/*/
rm /Users/chloewang/Downloads/MRI_temp/*.zip