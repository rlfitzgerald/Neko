#!/bin/sh
./car_detector_single -tv data/cropped_images_64x64/training_images_partitioned_0_30_60_90_120_150_random_negs_64x64/car_orientation_0/training_orientation_0.xml --flip -c 25 --threads 16 --target-size=4096 --eps 0.0019 > car_training_orientation_0.txt
cp object_detector.svm car_detector_orientation_0.svm

echo "Orientation 0 Complete"

./car_detector_single -tv data/cropped_images_64x64/training_images_partitioned_0_30_60_90_120_150_random_negs_64x64/car_orientation_30/training_orientation_30.xml  -c 25 --threads 16 --target-size=4096 --eps 0.0019 > car_training_orientation_30.txt
cp object_detector.svm car_detector_orientation_30.svm

echo "Orientation 30 Complete"

./car_detector_single -tv data/cropped_images_64x64/training_images_partitioned_0_30_60_90_120_150_random_negs_64x64/car_orientation_60/training_orientation_60.xml  -c 25 --threads 16 --target-size=4096 --eps 0.0019 > car_training_orientation_60.txt
cp object_detector.svm car_detector_orientation_60.svm

echo "Orientation 60 Complete"

./car_detector_single -tv data/cropped_images_64x64/training_images_partitioned_0_30_60_90_120_150_random_negs_64x64/car_orientation_90/training_orientation_90.xml --flip  -c 25 --threads 16 --target-size=4096 --eps 0.0019 > car_training_orientation_90.txt
cp object_detector.svm car_detector_orientation_90.svm

echo "Orientation 90 Complete"

./car_detector_single -tv data/cropped_images_64x64/training_images_partitioned_0_30_60_90_120_150_random_negs_64x64/car_orientation_120/training_orientation_120.xml  -c 25 --threads 16 --target-size=4096 --eps 0.0019 > car_training_orientation_120.txt
cp object_detector.svm car_detector_orientation_120.svm

echo "Orientation 120 Complete"

./car_detector_single -tv data/cropped_images_64x64/training_images_partitioned_0_30_60_90_120_150_random_negs_64x64/car_orientation_150/training_orientation_150.xml  -c 25 --threads 16 --target-size=4096 --eps 0.0019 > car_training_orientation_150.txt
cp object_detector.svm car_detector_orientation_150.svm

echo "Orientation 150 Complete"

echo "Orientation 0" > training_results.txt
echo "-------------" >> training_results.txt
tail -n 13 car_training_orientation_0.txt >> training_results.txt
echo "Orientation 30" >> training_results.txt
echo "--------------" >> training_results.txt
tail -n 13 car_training_orientation_30.txt >> training_results.txt
echo "Orientation 60" >> training_results.txt
echo "--------------" >> training_results.txt
tail -n 13 car_training_orientation_60.txt >> training_results.txt
echo "Orientation 90" >> training_results.txt
echo "--------------" >> training_results.txt
tail -n 13 car_training_orientation_90.txt >> training_results.txt
echo "Orientation 120" >> training_results.txt
echo "---------------" >> training_results.txt
tail -n 13 car_training_orientation_120.txt >> training_results.txt
echo "Orientation 150" >> training_results.txt
echo "---------------" >> training_results.txt
tail -n 13 car_training_orientation_150.txt >> training_results.txt
