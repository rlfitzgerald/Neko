#include <strings.h>

int main(int argc, char **argv) {
	void *p;
	(void)argc; (void)argv;
	p=(void*)(bcopy);
	return 0;
}
