#include <stdio.h>
#define MAX 100000
int main()
{
    //这里的N即为待测试的N皇后的N
    int N;
    int Queen[MAX];
    FILE *fp = NULL;
    fp = fopen("N QUEEN.txt", "r+");
    printf("Please input N value:\n");
    scanf("%d", &N);
    for (int i = 0; i < N; i++)
    {
        fscanf(fp, "%d ", &Queen[i]);
    }
    for (int i = 0; i < N; i++)
    {
        for (int j = i + 1; j < N; j++)
        {
            //判断是否冲突的条件
            if ((Queen[j] == Queen[i]) || ((j - Queen[j] + N - 1) == (i - Queen[i] + N - 1)) || ((j + Queen[j]) == (i + Queen[i])))
            {
                printf("Wrong Answer\n");
                system("pause");
                return 0;
            }
        }
    }
    printf("Right Answer\n");
    system("pause");
    return 0;
}