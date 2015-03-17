#!/bin/bash
for f in *.jpg; do
filename=$(basename $f);
extension="${filename##*.}";
filename="${filename%.*}";
outFile=$filename"_flop.jpg"
echo $outFile
convert -flop $f $outFile;
done;

