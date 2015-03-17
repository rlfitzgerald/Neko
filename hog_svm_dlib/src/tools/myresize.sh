#!/bin/bash
for f in *.jpg; do
filename=$(basename $f);
extension="${filename##*.}";
filename="${filename%.*}";
outFile=$filename"_3x.jpg"
echo $outFile
convert -filter spline -resize 300% -unsharp 0x1 $f $outFile;
done;

