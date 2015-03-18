*------------*
|    SETUP   |
*------------*
	Before you can compile the car detectors, you must set the following
	environment variables:

		export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/Path/to/Neko/hog_svm_dlib/src/libs/dlib-18.12
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Path/to/Neko/hog_svm_dlib/src/libs/dlib-18.12


	Note: DO *NOT* INCLUDE THE DLIB LIBRARY ON THESE PATHS (it causes errors)
				i.e. 
			    export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/.../src/libs/dlib-18.12/dlib
			    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/.../src/libs/dlib-18.12/dlib




*-------------*
|    BUILD    |
*-------------*
	To compile with the cmake build system:

    cd /Path/to/Neko/hog_svm_dlib/src
		mkdir build
		cd build
		cmake ..
		make





*---------------------------*
|    RUN (TL;DR VERSION)    |
*---------------------------*
	To train the car detector with the provided dataset:

    cd /Path/to/Neko/hog_svm_dlib/src
		cp ./build/car_detector_single .
		cp ./build/car_detector_multiple .
		./train_car_detector_orientations.sh
		
	To run the trained HoGs
		./car_detector_multiple input.jpg




*---------------------------*
|    RUN (LONG VERSION)     |
*---------------------------*
	Much of this section has been copied from the comments of
	libs/dlib-18.12/examples/train_object_detector.cpp

	The programs car_detector_single and car_detector_multiple are a command line
  tools for learning to detect objects (in this case cars) in images.  
	Therefore, to create an object detector it requires a set of annotated training 
	images.  To create this annotated data you will need to use the imglab tool 
	included with dlib.  It is located in the libs/dlib-18.12/tools/imglab folder
  and can be compiled using the following commands.  
			cd libs/dlib-18.12/tools/imglab
			mkdir build
			cd build
			cmake ..
			cmake --build . --config Release
	Note that you may need to install CMake (www.cmake.org) for this to work.  

	Next, let's assume you have a folder of images called /tmp/images.  These images 
	should contain examples of the objects you want to learn to detect.  You will 
	use the imglab tool to label these objects.  Do this by typing the following
			./imglab -c mydataset.xml /tmp/images

	This will create a file called mydataset.xml which simply lists the images in 
	/tmp/images.  To annotate them run
			./imglab mydataset.xml

	A window will appear showing all the images.  You can use the up and down arrow 
	keys to cycle though the images and the mouse to label objects.  In particular, 
	holding the shift key, left clicking, and dragging the mouse will allow you to 
	draw boxes around the objects you wish to detect.  So next, label all the objects 
	with boxes.  Note that it is important to label all the objects since any object 
	not labeled is implicitly assumed to be not an object we should detect.  If there
	are objects you are not sure about you should draw a box around them, then double
	click the box and press i.  This will cross out the box and mark it as "ignore".
	The training code in dlib will then simply ignore detections matching that box.
	

	Once you finish labeling objects go to the file menu, click save, and then close 
	the program. This will save the object boxes back to mydataset.xml.  You can verify 
	this by opening the tool again with
			./imglab mydataset.xml
	and observing that the boxes are present.

	Returning to the present program, we can compile it using cmake just as we 
	did with the imglab tool.  Once compiled, we can issue the command 
			./car_detector_single -tv mydataset.xml

	which will train an object detection model based on our labeled data.  The model 
	will be saved to the file object_detector.svm.  Once this has finished we can use 
	the object detector to locate objects in new images with a command like
			./car_detector_single some_image.png

	This command will display some_image.png in a window and any detected objects will
	be indicated by a red box.

	The program also has an option to add left/right flipped images to the
  training set with the --flip option. For example
			./car_detector_single -tv mydataset.xml --flip

	To run the object detection model over your testing set
		./car_detector_single --test /tmp/testing_images/testing.xml -u1
		./car_detector_single  /tmp/testing_images/*.jpg -u1

	Other SVM parameters like the C parameter or the epsilon parameter can also
  be set if the training results are unsatisfactory. For example 
    ./car_detector_single -u1 -c 25 --eps 0.0019 -tv mydataset.xml

	Training can also be accelerated by adding multiple threads. For example
    ./car_detector_single -u1 -c 25 --eps 0.0019 --threads 16 -tv mydataset.xml

	Now you may have noticed that there are two versions of the program:
	car_detector_single and car_detector_multiple. This is because the 
  car HoG descriptor is trained only on specific orientations. The 
  car_detector_single is used in training to train a HoG filter in a
  certain orientation. To cover all possible orientations, multiple
  HoG filters are trained. The car_detector_multiple is designed to 
  use multiple orientation HoG filters together to detect cars with
  higher fidelity. Thus you use car_detector_single in the training
  phase and car_detector_multiple in the detection phase.


	Caveats and Pitfalls
  --------------------
  The car detectors are designed to be trained on cars of size 64x64. This
  means that 64x64 pixels is the SMALLEST size car that they can detect. In order
  to detect smaller cars, the image must be upsampled with the -u option.
  For example
		./car_detector_single -u1 input_size_32x32.jpg
		./car_detector_single -u2 input_size_16x16.jpg

	Each time the image is upsampled, the image doubles in size (quadruples
  the number of pixels). 

	The detectors can be trained in different images sizes, simply throw the 
	--target-size flag when you are training. For example, to train on 
  32x32 pixel size images (notice 32*32=1024)
		./car_detector_single -tv mydataset.xml --target-size=1024



