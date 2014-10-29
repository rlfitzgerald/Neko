#include <time.h>

int main(int argc, char **argv) {
	void *p;
	(void)argc; (void)argv;
	p=(void*)(localtime_r);
	return 0;
}
