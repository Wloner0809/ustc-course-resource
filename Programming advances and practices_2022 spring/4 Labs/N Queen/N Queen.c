#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
// MAX代表N皇后最大的N值
#define MAX 100000
//带参宏swap用来交换a、b并能够保存下来
#define swap(a, b) \
    {              \
        int t = a; \
        a = b;     \
        b = t;     \
    }
int N;
// Row数组代表某行的皇后数
// Col数组代表某列的皇后数
int Row[MAX];
int Col[MAX];
// MainDiagonal[i]代表的是从左上到右下的编号为i对角线（主对角线）上的皇后数
// CounterDiagonal[i]代表的是从右上到左下的编号为i对角线（副对角线）上的皇后数
int MainDiagonal[2*MAX];
int CounterDiagonal[2*MAX];
// QueenPosition[row]=col代表的是（row，col）处有皇后
int QueenPosition[MAX];
//这里GetMainDiagonalPosition和GetCounterDiagonalPosition是返回对角线编号的函数
//一条主对角线上row-col是相同的，为了使编号的值为正，故加上N-1
//一条副对角线上row+col是相同的，故用row+col作为编号
int GetMainDiagonalPosition(int Row, int Col)
{
    return Row - Col + N - 1;
}
int GetCounterDiagonalPosition(int Row, int Col)
{
    return Row + Col;
}
// RandomNumber函数用于产生随机数
int RandomNumber(int begin, int end)
{
    return rand() % (end - begin) + begin;
}
//随机化N皇后的位置（randomize in place）
void Randomize(int a[], int begin, int end)
{
    for (int i = begin; i < end - 1; i++)
    {
        int x = RandomNumber(i, end);
        swap(a[i], a[x]);
    }
}
//判断是否为解的函数
bool A_Solution(void)
{
    for (int i = 0; i < N; i++)
    {
        if (Col[QueenPosition[i]] != 1 || 
        MainDiagonal[GetMainDiagonalPosition(i, QueenPosition[i])] != 1 || 
        CounterDiagonal[GetCounterDiagonalPosition(i, QueenPosition[i])] != 1)
        {
            return false;
        }
    }
    return true;
}
//初始化QueenPosition的函数
void Initialize(void)
{
    for (int i = 0; i < N; i++)
    {
        QueenPosition[i] = i;
    }
    Randomize(QueenPosition, 0, N);
    for (int i = 0; i < N; i++)
    {
        Row[i] = 1;
        Col[i] = 1;
    }
    for (int i = 0; i <2* N-1; i++)
    {
        MainDiagonal[i] = 0;
        CounterDiagonal[i] = 0;
    }
    for (int i = 0; i < N; i++)
    {
        MainDiagonal[GetMainDiagonalPosition(i, QueenPosition[i])]++;
        CounterDiagonal[GetCounterDiagonalPosition(i, QueenPosition[i])]++;
    }
}
//利用最小冲突算法调整每一行
bool Adjust(int Row)
{
    int CurrentCol = QueenPosition[Row];
    int PerfectCol = CurrentCol;
    int MinConflict = Col[PerfectCol] +
     MainDiagonal[GetMainDiagonalPosition(Row, PerfectCol)] - 1 +
      CounterDiagonal[GetCounterDiagonalPosition(Row, PerfectCol)] - 1;
    for (int i = 0; i < N; i++)
    {
        if (i == CurrentCol)
        {
            continue;
        }
        int Conflict = Col[i] +
         MainDiagonal[GetMainDiagonalPosition(Row, i)] +
         CounterDiagonal[GetCounterDiagonalPosition(Row, i)];
        if (Conflict < MinConflict)
        {
            MinConflict = Conflict;
            PerfectCol = i;
        }
    }
    if (PerfectCol != CurrentCol)
    {
        Col[CurrentCol]--;
        MainDiagonal[GetMainDiagonalPosition(Row, CurrentCol)]--;
        CounterDiagonal[GetCounterDiagonalPosition(Row, CurrentCol)]--;
        Col[PerfectCol]++;
        MainDiagonal[GetMainDiagonalPosition(Row, PerfectCol)]++;
        CounterDiagonal[GetCounterDiagonalPosition(Row, PerfectCol)]++;
        QueenPosition[Row] = PerfectCol;
        if (Col[CurrentCol] == 1 &&
         Col[PerfectCol] == 1 &&  
         MainDiagonal[GetMainDiagonalPosition(Row, PerfectCol)] == 1 && 
         CounterDiagonal[GetCounterDiagonalPosition(Row, PerfectCol)] == 1)
        {
            return A_Solution();
        }
    }
    return false;
}
//打印结果
void Print(void)
{
    FILE *fp = NULL;
    fp = fopen("N QUEEN.txt", "w+");
    for (int i = 0; i < N; i++)
    {
        fprintf(fp, "%d ", QueenPosition[i]);
    }
}
int main()
{
    srand((unsigned)time(NULL));
    printf("N Value:\n");
    scanf("%d", &N);
    Initialize();
    // 如果第一次初始化就成功，不需要调整行
    if (A_Solution()) 
    {
        Print();
        system("pause");
        return 0;
    }
    bool CanExit = false;
    while (!CanExit)
    {
        for (int i = 0; i < N; i++)
        {
            if (Adjust(i))
            {
                CanExit = true;
                break;
            }
        }
    }
    Print();
    system("pause");
    return 0;
}