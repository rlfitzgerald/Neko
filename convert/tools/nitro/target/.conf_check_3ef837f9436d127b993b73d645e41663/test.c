#include <sys/time.h>

int main(int argc, char **argv) {
	void *p;
	(void)argc; (void)argv;
	p=(void*)(BSDgettimeofday);
	return 0;
}
