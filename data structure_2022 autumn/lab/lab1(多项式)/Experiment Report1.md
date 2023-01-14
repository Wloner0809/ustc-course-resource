#
#
#
#
<font face="方正粗黑宋简体" size=6><center>DataStucture-一元多项式计算器</font></center>

<center>
    <img src="https://img0.baidu.com/it/u=2517586580,3516754870&fm=253&fmt=auto&app=138&f=PNG?w=524&h=500" width="400">
</center>
<font face="方正粗黑宋简体" size=6><center>王昱-PB21030814</center></font>

###
<font face="方正粗黑宋简体" size=5><center>USTC2021级CS专业</center></font>
<div style="page-break-after: always;"></div>


<font face="方正粗黑宋简体" size=5><p align = "left">一.需求分析</p></font>
##
* <font face="方正粗黑宋简体" size=4>1.1问题描述</font>
<font face="方正粗黑宋简体" size=4>利用线性表这一数据结构，设计一个一元稀疏多项式简单计算器。</font>
###
* <font face="方正粗黑宋简体" size=4>1.2交互模式</font>
<font face="方正粗黑宋简体" size=4>本程序设计了一个简易的菜单。用户通过菜单上的提示信息，在键盘上输入需要演示的功能，相应的数据及其运算结果显示在其后。</font>
###
* <font face="方正粗黑宋简体" size=4>1.3基本功能</font>
<font face="方正粗黑宋简体" size=4>①创建多项式②输出多项式③输出多项式的类数学表达式④多项式相加⑤多项式相减⑥计算多项式在给定变量下的值⑦多项式求导</font>
###
* <font face="方正粗黑宋简体" size=4>1.4测试数据</font>

<font size=5>

```
创建多项式：11x^9-5x^8+7
多项式相加：x^100+x 和 x^200+x^100
多项式相减：x^100+x 和 x^200+x^100

```

</font>



#
<font face="方正粗黑宋简体" size=5>二.设计思路</font>

* <font face="方正粗黑宋简体" size=4>考虑到可能出现指数变化很大的情况，为了尽可能的利用空间，采用链表的形式设计该计算器。结构体定义如下：</font>
<font size=5>
```
typedef struct Item
{
    double coefficient; //系数
    int exponent;       //指数
    struct Item *next;  //指针域
} Item;
```
</font>

* <font face="方正粗黑宋简体" size=4>主函数是用一个switch语句完成的，通过switch语句的不同case来执行不同的函数，实现不同功能。</font>
#

<font face="方正粗黑宋简体" size=5>三.核心代码实现</font>

* <font face="方正粗黑宋简体" size=4>1.1创建多项式</font>
<font size=5>
```
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
```
</font>

><font face="方正粗黑宋简体" size=4>代码解释：①创建的是带头结点的有序链表，头结点系数设为0，指数设为-1。②创建结束的条件是<u>输入指数为-1(一元多项式的指数是自然数)</u>③创建时是先输入，读取后判断指数是否已存在，<u>若已存在则直接将系数加进去；若不存在再创建结点</u>，并插入使链表有序。</font>

* <font face="方正粗黑宋简体" size=4>1.2输出多项式</font>
<font size=5>
```
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
```
</font>

><font face="方正粗黑宋简体" size=4>代码解释：这里输出的依次是<u>项数，系数，指数</u>。其中对系数保留两位小数。</font>

* <font face="方正粗黑宋简体" size=4>1.3多项式相加</font>
<font size=5>
```
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
```
</font>

><font face="方正粗黑宋简体" size=4>代码解释：①为保证运算多项式的完整性，创建一个新的多项式记录相加的结果。②因为创建的多项式是按照指数大小递减排列的有序多项式，所以在相加时调用Compare()函数比较要相加项的指数大小，用switch语句转到相应的结果中。<u>(这里注意case后加大括号是由于作用域的问题，case后本不能定义变量)</u>③特别注意指数相等的情况，只有在系数相加不为零的时候才会创建结点<u>(同时这里系数是double型数据，不能直接用==来比较大小)</u>④在插入新结点时，如果是第一次插入则用head指向新结点，并将r指针指向新结点；如果不是第一次插入则更新r指针即可，最后再更新指向两个多项式的指针。如果有一个多项式没有加完，则利用循环遍历该多项式并把系数指数赋值给新多项式。</font>

* <font face="方正粗黑宋简体" size=4>1.4类数学形式多项式</font>
<font size=5>
```
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
```
</font>

><font face="方正粗黑宋简体" size=4>代码解释：该函数用了较多的if语句来讨论在输出表达式时会出现的特殊情况——==多项式系数为1，指数为1，指数为0==。对于这些特殊情况，直接输出即可。同时为了输出美观，==这里的系数全部保留整数。==</font>

* <font face="方正粗黑宋简体" size=4>1.5多项式求导</font>
<font size=5>
```
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
```
</font>

* <font face="方正粗黑宋简体" size=4>1.6主函数</font>
<font size=5>
```
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
```
</font>

><font face="方正粗黑宋简体" size=4>代码解释：主函数就是用switch语句制作了一个简易的菜单，同时提供清屏和退出功能。</font>

#
<font face="方正粗黑宋简体" size=5>四.调试分析及测试结果</font>

* <font face="方正粗黑宋简体" size=4>在前几次调试运行时，好几处因为忘记更新指针而导致运行出错。说明对链表的相关操作还是不熟悉。</font>
* <font face="方正粗黑宋简体" size=4>一开始不熟悉switch语句，导致case没加{}直接定义了变量而导致运行出错。</font>
* <font face="方正粗黑宋简体" size=4>在写输出类数学表达式的时候，由于if语句过多导致最开始漏掉了某些情况从而使得输出出现错误。</font>
* <font face="方正粗黑宋简体" size=4>写多项式求导函数时一开始忘记考虑常数项导数为0的特殊情况导致出现错误，以及出现野指针而出现错误。</font>
#

><font face="方正粗黑宋简体" size=5>下面是测试结果</font>
<font size=5>

```
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
1
enter 0 -1 to quit
7 0 -5 8 11 9 0 -1
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
2
3,11.00,9,-5.00,8,7.00,0
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
3
11x^9-5x^8+7
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
4
Please input items in Polynomial A of (A+B)
enter 0 -1 to quit
1 1 1 100 0 -1
Please input items in Polynomial B of (A+B)
enter 0 -1 to quit
1 100 1 200 0 -1
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
2
3,1.00,200,2.00,100,1.00,1
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
3
x^200+2x^100+x
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
5
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
2
2,-1.00,200,1.00,1
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
1
enter 0 -1 to quit
1 0 1 1 1 2 1 3 1 4 1 5 0 -1
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
3
x^5+x^4+x^3+x^2+x+1
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
6
Please input x value
-1
Value is 0.00
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
7
**********Welcome to W.loner's Unary polynomial calculator**********
**********Please choose Number 1-9 to achieve your goals  **********
**********1.Create Polynomial                             **********
**********2.Print Polynomial                              **********
**********3.Print Polynomial In Math                      **********
**********4.Add Polynomial                                **********
**********5.Subtract Polynomial                           **********
**********6.Calculate Polynomial with given x             **********
**********7.Derivative Polynomial                         **********
**********8.Clean the window                              **********
**********9.exit                                          **********
3
5x^4+4x^3+3x^2+2x+1
```

</font>

#

<font face="方正粗黑宋简体" size=5>五.总结和收获</font>

* <font face="方正粗黑宋简体" size=4>通过本次实验熟悉了线性表中链表的有关操作，尤其是利用指针对结点进行的操作。</font>
* <font face="方正粗黑宋简体" size=4>通过此次实验，重新熟悉了C语言和markdown语法。</font>
* <font face="方正粗黑宋简体" size=4>本次实验的内容相对简单，并没有遇到太大的困难。即使如此也有许多需要优化的地方，尤其是对时空复杂度的优化。</font>
