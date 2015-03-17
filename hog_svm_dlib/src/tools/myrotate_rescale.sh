#!/bin/bash
for f in *.jpg; do
	filename=$(basename $f);
	extension="${filename##*.}";
	filename="${filename%.*}";
	angles=( 30 60 90 120 150);
	for angle in "${angles[@]}"; do
		outFile=$filename"_rotate"$angle".jpg"
		echo $outFile
		convert $f -distort SRT "%[fx:aa=$angle*pi/180;(w*abs(sin(aa))+h*abs(cos(aa)))/min(w,h)], $angle" $outFile;
	done;
done;

