#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define EPSILON 1e-6
typedef struct Item
{
    double coefficient; //系数
    int exponent;       //指数
    struct Item *next;  //指针域
} Item;
void clear(void)
{
    while (getchar() != '\n')
        ;
}
//比较大小
int Compare(int a, int b)
{
    if (a < b)
        return -1;
    else if (a == b)
        return 0;
    else
        return 1;
}
//该函数用于创建一个表示一元多项式的有序链表
Item *CreatePolynomial(void)
{
    Item *head = (Item *)malloc(sizeof(Item));
    head->coefficient = 0.0;
    head->exponent = -1;
    head->next = NULL;
    printf("enter 0 -1 to quit\n");
    while (1)
    {
        double item_coefficient;
        int item_exponent;
        scanf("%lf %d", &item_coefficient, &item_exponent);
        if (item_exponent == -1)
        {
            break;
        }
        Item *p = head;
        //如果原链表中有刚输入的指数则不用创建结点，直接将系数加起来。
        while (p)
        {
            if (p->exponent == item_exponent)
            {
                p->coefficient += item_coefficient;
                break;
            }
            p = p->next;
        }
        //如果原链表中没有刚输入的指数则创建结点。
        if (p == NULL)
        {
            Item *item = (Item *)malloc(sizeof(Item));
            item->coefficient = item_coefficient;
            item->exponent = item_exponent;
            //下面的操作是为了将项插入到合适的位置使得多项式有序。
            Item *q, *r;
            q = head;
            r = head->next;
            while (r && item->exponent < r->exponent)
            {
                r = r->next;
                q = q->next;
            }
            q->next = item;
            item->next = r;
        }
    }
    return head;
}
//该函数用于打印多项式
void PrintPolynomial(Item *head)
{
    //初值设为-1是因为头结点不算在项数里
    int length = -1;
    Item *p = head;
    while (p)
    {
        length++;
        p = p->next;
    }
    printf("%d", length);
    p = head->next;
    if(p == NULL)
    {
        printf(",0\n");
    }
    else
    {
        while (p)
        {
            //这里对系数保留两位小数输出
            printf(",%.2lf,%d", p->coefficient, p->exponent);
            p = p->next;
        }
        printf("\n");
    }
}
//该函数用于有序一元多项式的相加
Item *AddPolynomial(Item *head1, Item *head2)
{
    Item *pa = head1, *pb = head2, *qa = head1->next, *qb = head2->next;
    //创建一个头结点，将运算结果保存在新的链当中。
    Item *head3 = (Item *)malloc(sizeof(Item));
    head3->coefficient = 0;
    head3->exponent = -1;
    head3->next = NULL;
    Item *r = NULL;
    while (qa && qb)
    {
        //这里case后面加大括号是因为考虑到变量的作用域问题。
        // case后面不能直接定义变量
        switch (Compare(qa->exponent, qb->exponent))
        {
        case -1:
        {
            Item *item1 = (Item *)malloc(sizeof(Item));
            item1->coefficient = qb->coefficient;
            item1->exponent = qb->exponent;
            item1->next = NULL;
            if (head3->next == NULL)
            {
                head3->next = item1;
                r = item1;
            }
            else
            {
                r->next = item1;
                r = r->next;
            }
            qb = qb->next;
            pb = pb->next;
            break;
        }
        case 0:
        {
            //系数相加不为零才创建新节点
            //浮点数不能直接看是否为零
            //故宏定义一个EPSILON
            if (fabs(qb->coefficient + qa->coefficient) > EPSILON)
            {
                Item *item2 = (Item *)malloc(sizeof(Item));
                item2->coefficient = qb->coefficient + qa->coefficient;
                item2->exponent = qa->exponent;
                item2->next = NULL;
                if (head3->next == NULL)
                {
                    head3->next = item2;
                    r = item2;
                }
                else
                {
                    r->next = item2;
                    r = r->next;
                }
                qb = qb->next;
                pb = pb->next;
                qa = qa->next;
                pa = pa->next;
            }
            else
            {
                qb = qb->next;
                pb = pb->next;
                qa = qa->next;
                pa = pa->next;
            }
            break;
        }
        case 1:
        {
            Item *item3 = (Item *)malloc(sizeof(Item));
            item3->coefficient = qa->coefficient;
            item3->exponent = qa->exponent;
            item3->next = NULL;
            if (head3->next == NULL)
            {
                head3->next = item3;
                r = item3;
            }
            else
            {
                r->next = item3;
                r = r->next;
            }
            qa = qa->next;
            pa = pa->next;
            break;
        }
        }
    }
    //处理剩余的结点
    Item *s = qa ? qa : qb;
    while (s)
    {
        Item *item = (Item *)malloc(sizeof(Item));
        item->coefficient = s->coefficient;
        item->exponent = s->exponent;
        item->next = NULL;
        r->next = item;
        r = r->next;
        s = s->next;
    }
    return head3;
}
//该函数用于有序的一元多项式的减法
Item *SubtractPolynomial(Item *head1, Item *head2)
{
    Item *p = head2;
    while (p)
    {
        p->coefficient = -1 * p->coefficient;
        p = p->next;
    }
    Item *head3 = AddPolynomial(head1, head2);
    p = head2;
    while (p)
    {
        p->coefficient = -1 * p->coefficient;
        p = p->next;
    }
    return head3;
}
//该函数用于计算一元有序多项式在某处的值
double CalculatePolynomial(Item *head, double x)
{
    double sum = 0;
    Item *p = head->next;
    while (p)
    {
        sum += pow(x, p->exponent) * p->coefficient;
        p = p->next;
    }
    return sum;
}
//该函数用于输出数学形式的一元多项式
void PrintPolynomialInMath(Item *head)
{
    Item *p = NULL;
    p = head->next;
    if (p == NULL)
    {
        printf("0\n");
        return;
    }
    while (p)
    {
        //分别讨论系数为1、指数为1、指数为0的情况
        if (abs(p->coefficient - 1) < EPSILON || abs(p->coefficient + 1) < EPSILON)
        {
            if (p->exponent != 0 && p->exponent != 1)
            {
                if (abs(p->coefficient - 1) < EPSILON)
                    printf("x^%d", p->exponent);
                else
                    printf("-x^%d", p->exponent);
                //+号加或者不加
                if (p->next != NULL && p->next->coefficient > 0)
                {
                    printf("+");
                }
            }
            else if (p->exponent == 1)
            {
                if (abs(p->coefficient - 1) < EPSILON)
                    printf("x");
                else
                    printf("-x");
                if (p->next != NULL && p->next->coefficient > 0)
                {
                    printf("+");
                }
            }
            else
            {
                if (abs(p->coefficient - 1) < EPSILON)
                    printf("%.0lf", p->coefficient);
                else
                    printf("%.0lf", p->coefficient);
                if (p->next != NULL && p->next->coefficient > 0)
                {
                    printf("+");
                }
            }
            //调整p指针的指向并跳出此次循环
            p = p->next;
            continue;
        }
        if (p->exponent == 1)
        {
            printf("%.0lfx", p->coefficient);
            if (p->next != NULL && p->next->coefficient > 0)
            {
                printf("+");
            }
            p = p->next;
            continue;
        }
        if (p->exponent == 0)
        {
            printf("%.0lf", p->coefficient);
            if (p->next != NULL && p->next->coefficient > 0)
            {
                printf("+");
            }
            p = p->next;
            continue;
        }
        printf("%.0lfx^%d", p->coefficient, p->exponent);
        if (p->next != NULL && p->next->coefficient > 0)
        {
            printf("+");
        }
        p = p->next;
    }
    printf("\n");
}
//该函数用于求一元有序多项式的导数
Item *DerivativePolynomial(Item *head)
{
    Item *p = head->next;
    //这里的s指针指向新链表，用于更新结点
    Item *s = NULL;
    Item *head1 = (Item *)malloc(sizeof(Item));
    head1->coefficient = 0;
    head1->exponent = -1;
    head1->next = NULL;
    while (p)
    {
        //常数项的导数为零，故不需要单独创建结点直接跳出循环
        if (p->exponent == 0)
        {
            p = p->next;
            continue;
        }
        Item *item = (Item *)malloc(sizeof(Item));
        item->coefficient = p->coefficient * p->exponent;
        item->exponent = p->exponent - 1;
        if (head1->next == NULL)
        {
            head1->next = item;
            item->next = NULL;
            s = item;
            p = p->next;
            continue;
        }
        else
        {
            s->next = item;
            //注意这里一定要把item->next置为空
            //否则会在打印多项式时出现segmentation fault
            item->next = NULL;
            s = item;
            p = p->next;
            continue;
        }
    }
    return head1;
}
int main()
{
    double x = 0;
    Item *head1 = NULL;
    Item *head2 = NULL;
    Item *head3 = NULL;
    while (1)
    {
        printf("**********Welcome to W.loner's Unary polynomial calculator**********\n");
        printf("**********Please choose Number 1-9 to achieve your goals  **********\n");
        printf("**********1.Create Polynomial                             **********\n");
        printf("**********2.Print Polynomial                              **********\n");
        printf("**********3.Print Polynomial In Math                      **********\n");
        printf("**********4.Add Polynomial                                **********\n");
        printf("**********5.Subtract Polynomial                           **********\n");
        printf("**********6.Calculate Polynomial with given x             **********\n");
        printf("**********7.Derivative Polynomial                         **********\n");
        printf("**********8.Clean the window                              **********\n");
        printf("**********9.exit                                          **********\n");
        int ch = 9;
        scanf("%d", &ch);
        clear();
        if (ch == 9)
            break;
        switch (ch)
        {
        case 1:
            head3 = CreatePolynomial();
            break;
        case 2:
            PrintPolynomial(head3);
            break;
        case 3:
            PrintPolynomialInMath(head3);
            break;
        case 4:
            if (head1 == NULL)
            {
                printf("Please input items in Polynomial A of (A+B)\n");
                head1 = CreatePolynomial();
            }
            if (head2 == NULL)
            {
                printf("Please input items in Polynomial B of (A+B)\n");
                head2 = CreatePolynomial();
            }
            head3 = AddPolynomial(head1, head2);
            break;
        case 5:
            if (head1 == NULL)
            {
                printf("Please input items in Polynomial A of (A-B)\n");
                head1 = CreatePolynomial();
            }
            if (head2 == NULL)
            {
                printf("Please input in Polynomial B of (A-B)\n");
                head2 = CreatePolynomial();
            }
            head3 = SubtractPolynomial(head1, head2);
            break;
        case 6:
            printf("Please input x value\n");
            scanf("%lf", &x);
            clear();
            //保留两位小数
            printf("Value is %.2lf\n", CalculatePolynomial(head3, x));
            break;
        case 7:
            head3 = DerivativePolynomial(head3);
            break;
        case 8:
            system("cls");
            break;
        default:
            break;
        }
    }
    system("pause");
    return 0;
}