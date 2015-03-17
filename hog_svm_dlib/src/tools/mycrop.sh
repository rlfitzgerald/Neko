#!/bin/bash
for f in *.jpg; do
filename=$(basename $f);
extension="${filename##*.}";
filename="${filename%.*}";
convert $f -crop 64x64 +repage +adjoin $filename"_64x64_%02d.jpg"
done;

