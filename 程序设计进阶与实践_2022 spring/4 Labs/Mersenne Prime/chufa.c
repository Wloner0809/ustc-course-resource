#include<stdio.h>
#include<string.h>
#define MAX_LEN 110
int an1[MAX_LEN];
int an2[MAX_LEN];
int tmpAn2[MAX_LEN];
int anResult[MAX_LEN];
char szLine1[MAX_LEN];
char szLine2[MAX_LEN];
char szN[MAX_LEN];
int Substract(int nMaxLen,int *an1,int *an2)
{
    int nStartPos = 0;
    for (int i = 0; i < nMaxLen;i++)
    {
        an1[i] -= an2[i];
        if(an1[i]<0)
        {
            an1[i] += 10;
            an1[i + 1]--;
        }
        if (an1[i])
        {
            nStartPos = i;
        }
    }
    return nStartPos;
}
int Length(int nMaxLen,int *an)
{
    int i;
    for (i = nMaxLen - 1; an[i] == 0 && i >= 0;i--)
        ;
    if(i>=0)
    {
        return i + 1;
    }
    return 0;
}
void ShiftLeft(int nMaxLen,int *an1,int *an2,int n)
{
    memcpy(an2, an1, nMaxLen * sizeof(int));
    if(n<=0)
    {
        return;
    }
    for (int i = nMaxLen - 1; i >= 0;i--)
    {
        if(i-n>=0)
        {
            an2[i] = an1[i - n];
        }
        else
        {
            an2[i] = 0;
        }
    }
}
int *Max(int nMaxLen,int *an1,int *an2)
{
    int bBothZero = 1;
    for (int i = nMaxLen - 1; i >= 0;i--)
    {
        if(an1[i]>an2[i])
        {
            return an1;
        }
        else if (an1[i] < an2[i])
        {
             return an2;
        }
        else if(an1[i])
        {
            bBothZero = 0;
        }
    }
    if(bBothZero)
    {
        return NULL;
    }
    return an1;
}
int main()
{
    int n;

        gets(szLine1);
        gets(szLine2);
        int i, j;
        memset(an1, 0, sizeof(an1));
        memset(an2, 0, sizeof(an2));
        int nLen1 = strlen(szLine1);
        for (j = 0, i = nLen1 - 1; i >= 0;i--)
        {
            an1[j++] = szLine1[i] - '0';
        }
        int nLen2 = strlen(szLine2);
        for (j = 0, i = nLen2 - 1; i >= 0;i--)
        {
            an2[j++] = szLine2[i] - '0';
        }
        int nHighestPos = 0;
        memset(anResult, 0, sizeof(anResult));
        int nShiftLen = Length(MAX_LEN, an1) - Length(MAX_LEN, an2);
        while(Max(MAX_LEN,an1,an2)==an1)
        {
            ShiftLeft(MAX_LEN, an2, tmpAn2, nShiftLen);
            while(Max(MAX_LEN,an1,tmpAn2)==an1)
            {
                Substract(MAX_LEN, an1, tmpAn2);
                anResult[nShiftLen]++;
            }
            if(nHighestPos==0&&anResult[nShiftLen])
            {
                nHighestPos = nShiftLen;
            }
            nShiftLen--;
        }
        for (i = nHighestPos; i >= 0;i--)
        {
            printf("%d", anResult[i]);
        }
        printf("\n");
    system("pause");
    return 0;
}