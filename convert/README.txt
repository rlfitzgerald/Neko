
DESCRIPTION:

convert.py is a .ntf to .pgm conversion tool developed to allow us to use tools
inside openCV on nitf images. None of the metadata associated with the nitf is
extracted during the conversion process, but the original nitf is left intact.

Usage example:

	python convert.py InputImage.ntf

The output file will be placed in the same directory as convert.py. A sample 
output file has not been provided, as it will typicaly exceed the 100MB file
size limit on GitHub. 
