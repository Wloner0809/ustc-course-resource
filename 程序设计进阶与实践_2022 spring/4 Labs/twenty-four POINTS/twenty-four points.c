#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#define EPSILON 1e-6
#define VALUE 24
#define LEN1 4
#define LEN2 3
#define LEN3 64
//这里使用带参宏equal来表征值为24的情况
#define equal(a, b) fabs(a - b) <= EPSILON
// Sign数组存放四个运算符
// number数组存放对输入的数的排列组合
// sign数组存放运算符的排列组合
// isASolution用来判断是否为解
char Sign[LEN1] = {'+', '-', '*', '/'};
double number[VALUE][LEN1];
char sign[LEN3][LEN2];
bool isASolution = false;
// calculate函数返回一次加减乘除运算的结果
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
}
// arrangedNumber函数用于求4个数的排列组合存放在number数组中
void arrangedNumber(double num[], double number[VALUE][LEN1])
{
    int count = 0;
    for (int a = 0; a < LEN1; a++)
    {
        for (int b = 0; b < LEN1; b++)
        {
            if (b == a)
                continue;
            for (int c = 0; c < LEN1; c++)
            {
                if (c == a || c == b)
                    continue;
                int d = 6 - a - b - c; // a+b+c+d=6（四个下标）
                number[count][0] = num[a];
                number[count][1] = num[b];
                number[count][2] = num[c];
                number[count][3] = num[d];
                count++;
            }
        }
    }
}
// arrangedOperationalCharacter函数用于求运算符的排列组合存放在sign数组中
void arrangedOperationalCharacter(char sign[LEN3][LEN2])
{
    int count = 0;
    for (int a = 0; a < LEN1; a++)
    {
        for (int b = 0; b < LEN1; b++)
        {
            for (int c = 0; c < LEN1; c++)
            {
                sign[count][0] = Sign[a];
                sign[count][1] = Sign[b];
                sign[count][2] = Sign[c];
                count++;
            }
        }
    }
}
//下面五个函数是五种加括号的方式
//用A、B、C、D表示数，￥表示运算符
//（（A￥B）￥C）￥D
void expression1(double number[], char sign[])
{
    double expression = 0;
    expression = calculate(number[0], number[1], sign[0]);
    expression = calculate(expression, number[2], sign[1]);
    expression = calculate(expression, number[3], sign[2]);
    if (equal(expression, VALUE))
    {
        isASolution = true;
        printf("((%.0lf%c%.0lf)%c%.0lf)%c%.0lf\n", number[0], sign[0], number[1], sign[1], number[2], sign[2], number[3]);
    }
}
//（A￥（B￥C））￥D
void expression2(double number[], char sign[])
{
    double expression = 0;
    expression = calculate(number[1], number[2], sign[1]);
    expression = calculate(number[0], expression, sign[0]);
    expression = calculate(expression, number[3], sign[2]);
    if (equal(expression, VALUE))
    {
        isASolution = true;
        printf("(%.0lf%c(%.0lf%c%.0lf))%c%.0lf\n", number[0], sign[0], number[1], sign[1], number[2], sign[2], number[3]);
    }
} 
// A￥（（B￥C）￥D）
void expression3(double number[], char sign[])
{
    double expression = 0;
    expression = calculate(number[1], number[2], sign[1]);
    expression = calculate(expression, number[3], sign[2]);
    expression = calculate(number[0], expression, sign[0]);
    if (equal(expression, VALUE))
    {
        isASolution = true;
        printf("%.0lf%c((%.0lf%c%.0lf)%c%.0lf)\n", number[0], sign[0], number[1], sign[1], number[2], sign[2], number[3]);
    }
}
// A￥（B￥（C￥D））
void expression4(double number[], char sign[])
{
    double expression = 0;
    expression = calculate(number[2], number[3], sign[2]);
    expression = calculate(number[1], expression, sign[1]);
    expression = calculate(number[0], expression, sign[0]);
    if (equal(expression, VALUE))
    {
        isASolution = true;
        printf("%.0lf%c(%.0lf%c(%.0lf%c%.0lf))\n", number[0], sign[0], number[1], sign[1], number[2], sign[2], number[3]);
    }
}
//（A￥B）￥（C￥D）
void expression5(double number[], char sign[])
{
    double expression = 0;
    expression = calculate(number[0], number[1], sign[0]);
    expression = calculate(expression, calculate(number[2], number[3], sign[2]), sign[1]);
    if (equal(expression, VALUE))
    {
        isASolution = true;
        printf("(%.0lf%c%.0lf)%c(%.0lf%c%.0lf)\n", number[0], sign[0], number[1], sign[1], number[2], sign[2], number[3]);
    }
}
int main()
{
    double num[LEN1];
    printf("请输入四个不大于20的正整数:(以空格作为间隔)\n");
    scanf("%lf%lf%lf%lf", &num[0], &num[1], &num[2], &num[3]);
    arrangedNumber(num, number);
    arrangedOperationalCharacter(sign);
    //通过双层循环实现数和运算符的排列组合
    for (int i = 0; i < VALUE; i++)
    {
        for (int j = 0; j < LEN3; j++)
        {
            expression1(number[i], sign[j]);
            expression2(number[i], sign[j]);
            expression3(number[i], sign[j]);
            expression4(number[i], sign[j]);
            expression5(number[i], sign[j]);
        }
    }
    if (!isASolution)
        printf("No Answer!\n");
    else
    {
        printf("The Answer Is Above!\nSome Answers may be repeated!\n");
    }
    system("pause");
    return 0;
}