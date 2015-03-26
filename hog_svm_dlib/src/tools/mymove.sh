#!/bin/sh
array=( 324 342 53 54 55 569 56 )
for i in "${array[@]}"
do
	fileName="car_pos_"$i"_flip.jpg"
	#fileName="car_pos_"$i"_flip_flop.jpg"
	echo $fileName
	mv $fileName ../car_orientation_165/
	fileName="car_pos_"$i"_flop.jpg"
	#fileName="car_pos_"$i".jpg"
	echo $fileName
	mv $fileName ../car_orientation_165/
done
