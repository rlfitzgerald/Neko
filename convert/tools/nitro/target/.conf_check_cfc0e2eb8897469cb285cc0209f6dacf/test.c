#include <sys/mman.h>

int main(int argc, char **argv) {
	void *p;
	(void)argc; (void)argv;
	p=(void*)(mmap);
	return 0;
}
