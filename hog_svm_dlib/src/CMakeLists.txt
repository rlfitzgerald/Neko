#
# This is a CMake makefile.  You can find the cmake utility and
# information about it at http://www.cmake.org
#


cmake_minimum_required(VERSION 2.8.4)

PROJECT(examples)

include(libs/dlib-18.12/dlib/cmake)

# We are going to use a macro to add all the example programs.  However,
# usually you will only create one executable in your cmake projects.
# Therefore, you would just need to invoke ADD_EXECUTABLE() and
# TARGET_LINK_LIBRARIES() as shown below.  
MACRO(add_example name)
   ADD_EXECUTABLE(${name} ${name}.cpp)
   TARGET_LINK_LIBRARIES(${name} dlib )
ENDMACRO()


#here we apply our macros 
add_example(car_detector_multiple)
add_example(car_detector_single)

