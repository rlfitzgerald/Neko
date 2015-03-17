#!/bin/bash
for f in *.jpg; do
filename=$(basename $f);
extension="${filename##*.}";
filename="${filename%.*}";
outFile=$filename"_flip.jpg"
echo $outFile
convert -flip $f $outFile;
done;

