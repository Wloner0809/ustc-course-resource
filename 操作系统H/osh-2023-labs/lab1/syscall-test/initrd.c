
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>

int main()
{
    char buffer1[40] = "\0";
    char buffer2[30] = "\0";

    //测试buffer长度充足时的情况
    long int sign1 = syscall(548, buffer1, 40);
    printf("buffer_size:40, return_value:%ld, buffer_content:%s\n",sign1, buffer1);

    //测试buffer长度不足时的情况
    long int sign2 = syscall(548, buffer2, 30);
    printf("buffer_size:30, return_value:%ld, buffer_content:%s\n",sign2, buffer2);

    return 0;
}
