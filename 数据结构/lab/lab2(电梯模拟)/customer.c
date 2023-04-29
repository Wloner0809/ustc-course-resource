#include "head.h"

//下面是电梯里的栈的有关操作
//构造一个空栈
bool InitStack(CustomerStackPtr S)
{
    S->base = (CustomerPtr)malloc(STACK_INIT_SIZE * sizeof(Customer));
    //存储空间分配失败
    if (!S->base)
        return false;
    S->top = S->base;
    S->stacksize = STACK_INIT_SIZE;
    return true;
}

//销毁一个栈
void DestroyStack(CustomerStackPtr S)
{
    CustomerPtr p = S->base;
    while (p != S->top)
    {
        free(p);
        ++p;
    }
}

//判断栈是否为空(判断电梯是否为空)
bool StackEmpty(CustomerStackPtr S)
{
    return S->base == S->top;
}

//入栈顶(进电梯)
void Push(CustomerStackPtr S, Customer e)
{
    if (S->top - S->base >= S->stacksize)
    {
        //栈满，追加空间
        S->base = (CustomerPtr)realloc(S->base, (S->stacksize + STACK_INCREMENT) * sizeof(Customer));
        S->top = S->base + S->stacksize;
        S->stacksize += STACK_INCREMENT;
    }
    *S->top++ = e;
}

//出栈顶(出电梯)
CustomerPtr Pop(CustomerStackPtr S)
{
    if (S->top == S->base)
        return NULL;
    return --S->top;
}

//下面是电梯门前的等待队列的有关操作
//构造一个空队列
void InitQueue(CustomerWaitQueuePtr Q)
{
    Q->front = Q->rear = (CustomerQueuePtr)malloc(sizeof(CustomerQueueNode));
    if (!Q->front)
    {
        printf("fail to distribute memory space");
        return;
    }
    Q->front->next = NULL;
    Q->CustomerNumber = 0;
}
//销毁队列
void DestroyQueue(CustomerWaitQueuePtr Q)
{
    while (Q->front)
    {
        Q->rear = Q->front->next;
        free(Q->front);
        Q->front = Q->rear;
    }
}
//插入乘客
void EnQueue(CustomerWaitQueuePtr Q, Customer e)
{
    CustomerQueuePtr p = (CustomerQueuePtr)malloc(sizeof(CustomerQueueNode));
    if (!p)
    {
        printf("fail to distribute memory space");
        return;
    }
    p->data = e;
    p->next = NULL;
    Q->rear->next = p;
    Q->rear = p;
    Q->CustomerNumber++; //插入乘客人数自增
}
//删除乘客,并返回乘客的信息
Customer DeQueue(CustomerWaitQueuePtr Q)
{
    Customer e = {0, 0, 0, 0, 0};
    if (Q->front == Q->rear)
    {
        printf("Empty Queue");
        return e;
    }
    CustomerQueuePtr p = Q->front->next;
    e = p->data;
    Q->front->next = p->next;
    if (Q->rear == p)
        Q->rear = Q->front;
    free(p);
    Q->CustomerNumber--;
    return e;
}
//判断是否为空队列
bool QueueEmpty(CustomerWaitQueuePtr Q)
{
    return Q->front == Q->rear;
}

//创建一个新的乘客
void CreateNewCustomer(void)
{
    CustomerPtr p = (CustomerPtr)malloc(sizeof(Customer));
    if (!p)
    {
        printf("fail to distribute memory space");
        return;
    }
    p->ID = ++CustomerID;
    p->InFloor = rand() % (MAXFLOOR + 1);
    p->OutFloor = rand() % (MAXFLOOR + 1);
    p->GiveupTime = rand() % max_give_up_time + 300;
    p->InterTime = rand() % max_inter_time + 50;
    CustomerInterTime = p->InterTime;
    //这里让乘客进入的楼层与将要去的楼层不同
    //因为如果相同乘客直接到达不需要乘坐电梯
    while (p->InFloor == p->OutFloor)
        p->InFloor = rand() % (MAXFLOOR + 1);

    //按电钮等候
    if (p->OutFloor > p->InFloor) //要去的楼层高于进入楼层,应进入上升队列
    {
        EnQueue(CustomerUpQueue[p->InFloor], *p);
        CallUp[p->InFloor] = 1;
    }
    else
    {
        EnQueue(CustomerDownQueue[p->InFloor], *p);
        CallDown[p->InFloor] = 1;
    }
    DisplayInfo(CREATE_NEW_CUSTOMER, p->ID, p->InFloor, p->OutFloor, FiveFloorElevator->Floor);
    printf("Other Info About Customer:Give up time:%d Inter time: %d\n", p->GiveupTime, p->InterTime);
}

//乘客准备进入电梯
bool CustomerIn(void)
{
    Customer customer_entering_lift;
    if (FiveFloorElevator->CustomerNumber == CAPACITY)
        return false;
    switch (FiveFloorElevator->State)
    {
    case going_up:
    {
        //电梯门前上升队列乘客人数为0，而此时电梯上行
        if (!CustomerUpQueue[FiveFloorElevator->Floor]->CustomerNumber)
            return false;
        FiveFloorElevator->CustomerNumber++;
        //记录下正要进电梯的乘客信息，并让他离开队列
        customer_entering_lift = DeQueue(CustomerUpQueue[FiveFloorElevator->Floor]);
        //将乘客压入电梯栈中
        Push(FiveFloorElevator->CustomerStack[customer_entering_lift.OutFloor], customer_entering_lift);
        //将电梯内的按钮修改
        FiveFloorElevator->CallCar[customer_entering_lift.OutFloor] = 1;
        DisplayInfo(CUSTOMER_IN, customer_entering_lift.ID, customer_entering_lift.InFloor, customer_entering_lift.OutFloor, FiveFloorElevator->Floor);
        return true;
    }
    case going_down:
    {
        if (!CustomerDownQueue[FiveFloorElevator->Floor]->CustomerNumber)
            return false;
        FiveFloorElevator->CustomerNumber++;
        customer_entering_lift = DeQueue(CustomerDownQueue[FiveFloorElevator->Floor]);
        Push(FiveFloorElevator->CustomerStack[customer_entering_lift.OutFloor], customer_entering_lift);
        FiveFloorElevator->CallCar[customer_entering_lift.OutFloor] = 1;
        DisplayInfo(CUSTOMER_IN, customer_entering_lift.ID, customer_entering_lift.InFloor, customer_entering_lift.OutFloor, FiveFloorElevator->Floor);
        return true;
    }
    //前面已经按电钮等候了，而且乘客进入的楼层和目标楼层不同
    //所以电梯只可能是going_up或者going_down
    default:
        return false;
    }
}

//乘客准备离开电梯
bool CustomerOut(void)
{
    if (!StackEmpty(FiveFloorElevator->CustomerStack[FiveFloorElevator->Floor]))
    {
        FiveFloorElevator->CustomerNumber--;
        CustomerPtr customer_leaving_lift = Pop(FiveFloorElevator->CustomerStack[FiveFloorElevator->Floor]);
        DisplayInfo(CUSTOMER_OUT, customer_leaving_lift->ID, customer_leaving_lift->InFloor, customer_leaving_lift->OutFloor, FiveFloorElevator->Floor);
        return true;
    }
    return false;
}
//计算队列中元素P前面有多少元素
int CustomerInQueueNumber(CustomerWaitQueuePtr Q, CustomerQueuePtr P)
{
    int cnt = 0;
    CustomerQueuePtr p = Q->front;
    while (p->next && p->next != P)
    {
        ++cnt;
        p = p->next;
    }
    return cnt;
}
//检查某一层的上升队列中是否有乘客放弃
void CheckUpQueueCustomerGiveUp(int floor)
{
    CustomerQueuePtr p = CustomerUpQueue[floor]->front;
    CustomerQueuePtr q = NULL;
    // if里面的是还可以等到电梯的
    while (p->next)
    {
        if (p->next->data.GiveupTime > 0)
        {
            p = p->next;
            p->data.GiveupTime--;
        }
        else
        {
            //如果电梯在本层且D1不等于0且没有满载
            if (floor == FiveFloorElevator->Floor && FiveFloorElevator->D1 && (FiveFloorElevator->CustomerNumber + CustomerInQueueNumber(CustomerUpQueue[floor], p)) < CAPACITY)
            {
                p = p->next;
            }
            //否则乘客就要放弃
            else
            {
                --CustomerUpQueue[floor]->CustomerNumber;
                q = p->next;
                DisplayInfo(CUSTOMER_GIVE_UP, q->data.ID, q->data.InFloor, q->data.OutFloor, FiveFloorElevator->Floor);
                p->next = q->next;
                if (q == CustomerUpQueue[floor]->rear)
                    CustomerUpQueue[floor]->rear = p;
                free(q);
            }
        }
    }
}

//检查某一层中的下降队列中是否有乘客放弃
void CheckDownQueueCustomerGiveUp(int floor)
{
    CustomerQueuePtr p = CustomerDownQueue[floor]->front;
    CustomerQueuePtr q = NULL;
    // if里面的是还可以等到电梯的
    while (p->next)
    {
        if (p->next->data.GiveupTime > 0)
        {
            p = p->next;
            p->data.GiveupTime--;
        }
        else
        {
            //如果电梯在本层且D1不等于0且没有满载
            if (floor == FiveFloorElevator->Floor && FiveFloorElevator->D1 && (FiveFloorElevator->CustomerNumber + CustomerInQueueNumber(CustomerDownQueue[floor], p)) < CAPACITY)
            {
                p = p->next;
            }
            //否则乘客就要放弃
            else
            {
                --CustomerDownQueue[floor]->CustomerNumber;
                q = p->next;
                DisplayInfo(CUSTOMER_GIVE_UP, q->data.ID, q->data.InFloor, q->data.OutFloor, FiveFloorElevator->Floor);
                p->next = q->next;
                if (q == CustomerDownQueue[floor]->rear)
                    CustomerDownQueue[floor]->rear = p;
                free(q);
            }
        }
    }
}