#include <getopt.h>

int main(int argc, char **argv) {
	void *p;
	(void)argc; (void)argv;
	p=(void*)(getopt_long);
	return 0;
}
