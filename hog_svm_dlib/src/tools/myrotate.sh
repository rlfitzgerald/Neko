#!/bin/bash
for f in *.jpg; do
	filename=$(basename $f);
	extension="${filename##*.}";
	filename="${filename%.*}";
	angles=( 30 60 90 120 150);
	for angle in "${angles[@]}"; do
		outFile=$filename"_rotate"$angle".jpg"
		echo $outFile
		convert $f \( +clone -background black -rotate -$angle \)  -gravity center -compose Src -composite $outFile
	done;
done;

