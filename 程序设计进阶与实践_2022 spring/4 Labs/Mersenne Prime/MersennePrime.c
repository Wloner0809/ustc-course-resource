#include <math.h>
#include <stdio.h>
#include <string.h>
// MAX_LEN是十进制用的，MAX_LEN1是二进制用的
#define MAX_LEN 400
#define MAX_LEN1 1010
// upper、lower分别对应的是梅森素数指数p的上界和下界
#define UPPER_BOUND 1000
#define LOWER_BOUND 2
typedef struct
{
    int Len;
    int Value[MAX_LEN]; //用于存放二进制数相应的十进制数
} BigInt, *PBigInt;
//此函数用于找到一千以内的素数
void IsPrime(int *a);
//将数字转化成二进制存放在数组中
void TransToBinaryNumber(int p, int *BinaryNumber);
//转十进制
void TransToDecimalism(PBigInt s, int BitValue);
//下面的几个函数用于实现求余数
int Length(int nMaxLen, int *an);
void Substract(int nMaxLen, int *an1, int *an2);
void ShiftLeft(int nMaxLen, int *an1, int *an2, int n);
//当an1中的值与an2中的值相等时，返回an1
int *Max(int nMaxLen, int *an1, int *an2);
//求余函数，余数存放在第一个参数里
void Remainder(int *an1, int *an2, int *tmpAn2);
void Multiply(int Len1, int *a1, int Len2, int *a2, int *aResult);
//此函数用于求卢卡斯·莱默余数
//第一个参数是待测数的十进制形式
//第二个参数是指数p
//第三个参数用于存放卢卡斯·莱默余数
//第四个参数是卢卡斯莱默算法中的数列表达式
//第五个参数是用于求余的中间数组
void L_L_Remainder(int *DecimalismMersenne, int p, int Result[], int L_L_Expression[], int Tmp[]);
int main()
{
    int BinaryNumber[MAX_LEN1] = {0};
    int Prime[MAX_LEN] = {0};
    int Tmp[MAX_LEN] = {0};
    int L_L_Expression[MAX_LEN] = {4};
    int Result[MAX_LEN * 2] = {0};
    BigInt Big;
    IsPrime(Prime); // Prime数组用于存放素数p
    for (int i = 0; Prime[i] && i < MAX_LEN; i++)
    {
        memset(&Big, 0, sizeof(Big));
        // BinaryNumber用于存放二进制形式
        TransToBinaryNumber(Prime[i], BinaryNumber);
        //此循环用于将二进制转化成十进制
        for (int j = 0; BinaryNumber[j]; j++)
        {
            TransToDecimalism(&Big, BinaryNumber[j] == 1 ? 1 : 0);
        }
        L_L_Remainder(Big.Value, Prime[i], Result, L_L_Expression, Tmp);
        //这里当Prime[0]=2时，它没有执行上述循环直接跳出，Result数组length为0
        //根据现有知识，2^2-1是素数，故这里直接把p=2打印出来
        if (Length(MAX_LEN, Result) == 0)
        {
            printf("P Value:%d\n", Prime[i]);
            printf("MersennePrime:");
            for (int n = Length(MAX_LEN, Big.Value) - 1; n >= 0; n--)
                printf("%d", Big.Value[n]);
            printf("\n");
        }
    }
    system("pause");
    return 0;
}
void IsPrime(int a[])
{
    int pos = 0, count, p;
    for (p = LOWER_BOUND; p <= UPPER_BOUND; p++)
    {
        for (count = 1; count <= (int)sqrt(p); count++)
        {
            if (p % count == 0 && count != 1)
            {
                break;
            }
            if (count == (int)sqrt(p))
            {
                a[pos++] = p;
            }
        }
    }
}
void TransToBinaryNumber(int p, int *BinaryNumber)
{
    int count;
    for (count = 0; count < p; count++)
    {
        BinaryNumber[count] = 1; //根据梅森素数的特点，指数p是多少就有多少个1
    }
}
void TransToDecimalism(PBigInt s, int BitValue)
{
    int count;
    for (count = 0; count < s->Len; count++)
    {
        s->Value[count] *= 2;
    }
    s->Value[0] += BitValue;
    for (count = 0; count < s->Len; count++)
    {
        s->Value[count + 1] += s->Value[count] / 10;
        s->Value[count] %= 10;
    }
    if (s->Value[s->Len])
    {
        s->Len++;
    }
}
int Length(int nMaxLen, int *an)
{
    int i;
    for (i = nMaxLen - 1; an[i] == 0 && i >= 0; i--)
        ;
    if (i >= 0)
    {
        return i + 1;
    }
    return 0;
}
void Substract(int nMaxLen, int *an1, int *an2)
{
    for (int i = 0; i < nMaxLen; i++)
    {
        an1[i] -= an2[i];
        if (an1[i] < 0)
        {
            an1[i] += 10;
            an1[i + 1]--;
        }
    }
}
void ShiftLeft(int nMaxLen, int *an1, int *an2, int n)
{
    memcpy(an2, an1, nMaxLen * sizeof(int));
    if (n <= 0)
    {
        return;
    }
    for (int i = Length(MAX_LEN, an1) + n; i >= 0; i--)
    {
        if (i - n >= 0)
        {
            an2[i] = an1[i - n];
        }
        else
        {
            an2[i] = 0;
        }
    }
}
int *Max(int nMaxLen, int *an1, int *an2)
{
    int BothZero = 1;
    for (int i = nMaxLen - 1; i >= 0; i--)
    {
        if (an1[i] > an2[i])
        {
            return an1;
        }
        else if (an1[i] < an2[i])
        {
            return an2;
        }
        else if (an1[i])
        {
            BothZero = 0;
        }
    }
    if (BothZero)
    {
        return NULL;
    }
    return an1;
}
void Remainder(int *an1, int *an2, int *tmpAn2)
{
    while (Max(MAX_LEN, an1, an2) == an1)
    {
        int nShiftLen = Length(MAX_LEN, an1) - Length(MAX_LEN, an2) - 1;
        ShiftLeft(MAX_LEN, an2, tmpAn2, nShiftLen);
        while (Max(MAX_LEN, an1, tmpAn2) == an1)
        {
            Substract(MAX_LEN, an1, tmpAn2);
        }
    }
}
//尝试Lucas–Lehmer算法
//先写一个高精度乘法
void Multiply(int Len1, int *a1, int Len2, int *a2, int *aResult)
{
    for (int i = 0; i < Len2; i++)
    {
        for (int j = 0; j < Len1; j++)
        {
            aResult[i + j] += a1[j] * a2[i];
        }
    }
    aResult[0] -= 2;
    for (int i = 0; i < Len1 * 2; i++)
    {
        if (aResult[i] >= 10)
        {
            aResult[i + 1] += aResult[i] / 10;
            aResult[i] %= 10;
        }
        if (aResult[i] < 0)
        {
            aResult[i + 1]--;
            aResult[i] += 10;
        }
    }
}
//此函数用于求卢卡斯·莱默余数
//第一个参数是待测数的十进制形式
//第二个参数是指数p
//第三个参数用于存放卢卡斯·莱默余数
//第四个参数是卢卡斯莱默算法中的数列表达式
//第五个参数是用于求余的中间数组
void L_L_Remainder(int *DecimalismMersenne, int p, int Result[], int L_L_Expression[], int Tmp[])
{
    for (int k = 0; k < p - 2; k++)
    {
        memset(L_L_Expression, 0, MAX_LEN * sizeof(int));
        if (k != 0)
        {
            for (int m = 0; m < MAX_LEN; m++)
            {
                L_L_Expression[m] = Result[m];
            }
            memset(Result, 0, 2 * MAX_LEN * sizeof(int));
        }
        else
        {
            memset(Result, 0, 2 * MAX_LEN * sizeof(int));
            L_L_Expression[0] = 4;
        }
        Multiply(Length(MAX_LEN, L_L_Expression), L_L_Expression, Length(MAX_LEN, L_L_Expression), L_L_Expression, Result);
        Remainder(Result, DecimalismMersenne, Tmp);
    }
}


//下面是测试代码
/*#include "MersennePrime.c"
int main()
{
    int BinaryNumber[MAX_LEN1] = {0};
    int Prime[MAX_LEN] = {0};
    int Tmp[MAX_LEN] = {0};
    int L_L_Expression[MAX_LEN] = {4};
    int Result[MAX_LEN * 2] = {0};
    BigInt Big;
    IsPrime(Prime); //测试五组数据
    for (int count = 2; count < 100; count = count + 20)
    {
        printf("测试数据p的值:%d\n", Prime[count]);
        TransToBinaryNumber(Prime[count], BinaryNumber);
        for (int i = 0; BinaryNumber[i]; i++)
            TransToDecimalism(&Big, 1);
        printf("二进制表示:\n");
        for (int i = 0; i < Prime[count]; i++)
            printf("%d", BinaryNumber[i]);
        printf("\n十进制表示:\n");
        for (int j = Length(MAX_LEN, Big.Value) - 1; j >= 0; j--)
            printf("%d", Big.Value[j]);
        L_L_Remainder(Big.Value, Prime[count], Result, L_L_Expression, Tmp);
        printf("\n卢卡斯·莱默余数长度:%d\n", Length(MAX_LEN, Result));
        printf("卢卡斯·莱默余数十进制表示:");
        if (Length(MAX_LEN, Result) == 0)
            printf("0");
        else
            for (int j = Length(MAX_LEN, Result) - 1; j >= 0; j--)
                printf("%d", Result[j]);
        printf("\n\n");
    }
    system("pause");
    return 0;
}*/