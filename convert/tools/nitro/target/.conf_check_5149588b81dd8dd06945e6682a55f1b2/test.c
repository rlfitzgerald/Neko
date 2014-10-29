#include <time.h>

int main(int argc, char **argv) {
	void *p;
	(void)argc; (void)argv;
	p=(void*)(gmtime_r);
	return 0;
}
