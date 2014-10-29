
#include <stdio.h>
int isBigEndian()
{
    long one = 1;
    return !(*((char *)(&one)));
}
int main()
{
    if (isBigEndian()) printf("bigendian=True\n");
    else printf("bigendian=False\n");
    printf("sizeof_int=%d\n", sizeof(int));
    printf("sizeof_short=%d\n", sizeof(short));
    printf("sizeof_long=%d\n", sizeof(long));
    printf("sizeof_long_long=%d\n", sizeof(long long));
    printf("sizeof_float=%d\n", sizeof(float));
    printf("sizeof_double=%d\n", sizeof(double));
    return 0;
}
