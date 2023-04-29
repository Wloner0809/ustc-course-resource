#include <math.h>
#include <stdio.h>
#include<stdbool.h>
#define EPSILON 1e-6
#define VALUE 24
#define equal(a, b) fabs(a - b) <= EPSILON
char Sign[4] = {'+', '-', '*', '/'};
bool isASolution = false;
double calculate(double a, double b, char sign)
{
    switch (sign)
    {
    case '+':
        return a + b;
        break;
    case '-':
        return a - b;
        break;
    case '*':
        return a * b;
        break;
    case '/':
        return a / b;
        break;
    }
    return 10000;
}
bool expression(int pos[],char sign[],double number[])
{
    double expression = 0;
    //加括号一共有五种情况
    //用A、B、C、D表示数，￥表示运算符
    //（（A￥B）￥C）￥D
    expression = calculate(number[pos[0]], number[pos[1]],  sign[0]);
    expression = calculate(expression, number[pos[2]], sign[1]);
    expression = calculate(expression, number[pos[3]], sign[2]);
    if(equal(expression,VALUE))
        return true;
    //（A￥（B￥C））￥D
    expression = calculate(number[pos[1]], number[pos[2]], sign[1]);
    expression = calculate(number[pos[0]],expression, sign[0]);
    expression = calculate(expression, number[pos[3]], sign[2]);
    if (equal(expression, VALUE))
        return true;
    //A￥（（B￥C）￥D）
    expression = calculate(number[pos[1]], number[pos[2]], sign[1]);
    expression = calculate(expression, number[pos[3]], sign[2]);
    expression = calculate(number[pos[0]], expression, sign[0]);
    if (equal(expression, VALUE))
        return true;
    //A￥（B￥（C￥D））
    expression = calculate(number[pos[2]], number[pos[3]], sign[2]);
    expression = calculate(number[pos[1]], expression, sign[1]);
    expression = calculate(number[pos[0]], expression, sign[0]);
    if (equal(expression, VALUE))
        return true;
    //（A￥B）￥（C￥D）
    expression = calculate(number[pos[0]], number[pos[1]], sign[0]);
    expression = calculate(expression, calculate(number[pos[2]], number[pos[3]], sign[2]), sign[1]);
    if (equal(expression, VALUE))
        return true;
    return false;
}
void operationalCharacter(double number[],int pos,char sign[],int temp[])
{
    if(pos==3)
    {
        if(expression(temp,sign,number))
        {
            isASolution = true;
        }
        return;
    }
    for (int i = 0; i < 4;i++)
    {
        sign[pos] = Sign[i];
        operationalCharacter(number, pos + 1, sign, temp);
        if(isASolution)
            return;
    }
}
void arrangeNumber(double number[],int temp[],int pos)
{
    if(pos==4)
    {
        char sign[3];
        operationalCharacter(number, 0, sign, temp);
        return;
    }
    for (int i = 0; i < 4;i++)
    {
        int count;
        for ( count = 0; count < pos;count++)
        {
            if(temp[count]==i)
                break;
        }
        if(count==pos)
        {
            temp[pos] = i;
            arrangeNumber(number, temp, pos + 1);
            if(isASolution)
                return;
        }
    }
}
int main()
{
    double number[4];
    int temp[4];
    scanf("%lf%lf%lf%lf", &number[0], &number[1], &number[2], &number[3]);
    arrangeNumber(number, temp, 0);
    if(isASolution)
        printf("PASS!\n");
    system("pause");
    return 0;
}

