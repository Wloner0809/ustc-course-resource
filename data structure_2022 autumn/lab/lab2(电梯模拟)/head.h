#include <malloc.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>
#define MAXFLOOR 4
#define CAPACITY 20 //电梯容量
#define MAXTIME 2000
#define STACK_INIT_SIZE 100
#define STACK_INCREMENT 10
int Time = 0; //模拟时钟
int CustomerInterTime = 0;
int CustomerID = 0;
int CallUp[MAXFLOOR + 1];   //电梯外上按钮,每层楼外有一个
int CallDown[MAXFLOOR + 1]; //电梯外下按钮,每层楼外有一个

enum ElevatorTime
{
    door_test_time = 40,          //关门检查D1的时间间隔
    open_close_door_time = 20,    //开关门的时间(opening到open需要20t)
    customer_inout_time = 25,     //乘客进出电梯的时间
    elevator_max_wait_time = 300, //电梯最大停候时间
    up_wait_time = 51,            //上升时的等候时间
    down_wait_time = 61,          //下降时的等候时间
    up_slow_time = 14,            //上升时需要改变状态所需要的时间
    down_slow_time = 23,          //下降时需要改变状态所需要的时间
    accelerate_time = 15          //电梯加速时间
};

enum ElevatorState
{
    going_up = 1,
    going_down = -1,
    idle = 0
};

enum ElevatorActivity
{
    OPENING, //正在开门
    OPENED,  //已经开门
    CLOSING, //正在关门
    CLOSED,  //已经关门
    ACCELERATING,
    SLOWING,
    MOVING,
    IDLE
};

enum CustomerTime
{
    max_give_up_time = 200, //最长的放弃时间
    max_inter_time = 60     //最长的间隔时间
};

enum DisplayInfo
{
    CREATE_NEW_CUSTOMER,
    CUSTOMER_IN,
    CUSTOMER_OUT,
    CUSTOMER_GIVE_UP,
    ELEVATOR_OPENING,
    ELEVATOR_OPENED,
    ELEVATOR_CLOSING,
    ELEVATOR_CLOSED,
    ELEVATOR_ACCELERATING,
    ELEVATOR_MOVING,
    ELEVATOR_SLOWING,
    ELEVATOR_IDLE,
    ELEVATOR_IDLE_TO_OPENING,
    ELEVATOR_IDLE_TO_ACCELERATING
};

typedef struct customer
{
    int ID;         //标记乘客
    int InFloor;    //进入了哪层楼
    int OutFloor;   //将要去哪层楼
    int GiveupTime; //能容忍的等待时间
    int InterTime;  //下一个人出现的时间间隔
} Customer, *CustomerPtr;

//电梯里的乘客栈
typedef struct
{
    CustomerPtr base;
    CustomerPtr top;
    int stacksize;
} CustomerStack, *CustomerStackPtr;

//电梯门前的等待队列
typedef struct CustomerQueueNode
{
    Customer data;
    struct CustomerQueueNode *next;
} CustomerQueueNode, *CustomerQueuePtr;

typedef struct
{
    CustomerQueuePtr front; //队头指针
    CustomerQueuePtr rear;  //队尾指针
    int CustomerNumber;
} CustomerWaitQueue, *CustomerWaitQueuePtr;

CustomerWaitQueuePtr CustomerUpQueue[MAXFLOOR + 1];   //上升队列,每层都有一个上升队列
CustomerWaitQueuePtr CustomerDownQueue[MAXFLOOR + 1]; //下降队列,每层都有一个下降队列

typedef struct
{
    int Floor;                 //电梯当前位置
    int D1;                    //电梯无人进出则D1为0
    int D2;                    //电梯在某层停300t以上则D2为0
    int D3;                    //电梯门开并且无人进出电梯则D3等于0
    enum ElevatorState State;  //电梯的当前状态(going_up/going_down/idle)
    int CallCar[MAXFLOOR + 1]; //电梯内按钮,有人按下按钮置为1，否则置为0
    int CustomerNumber;
    CustomerStackPtr CustomerStack[MAXFLOOR + 1]; //乘客栈
    enum ElevatorActivity activity;               //电梯的几个活动
    int activity_timer;                           //活动计时器
    int customer_in_out_timer;                    //乘客进出时间计时器
    int StateChange;                              //判断状态是否需要改变
} Elevator, *ElevatorPtr;

ElevatorPtr FiveFloorElevator;

void DisplayInfo(int info, int customer_id, int in_floor, int out_floor, int elevator_floor)
{
    switch (info)
    {
    case CREATE_NEW_CUSTOMER:
    {
        printf("Current time is %d\n", Time);
        printf("Customer%d comes to floor%d and wants to go to floor%d\n", customer_id, in_floor, out_floor);
        break;
    }
    case CUSTOMER_IN:
    {
        printf("Current time is %d\n", Time);
        printf("Customer%d enters into the FiveFloorElevator in floor%d\n", customer_id, elevator_floor);
        break;
    }
    case CUSTOMER_OUT:
    {
        printf("Current time is %d\n", Time);
        printf("Customer%d leaves the FiveFloorElevator in floor%d\n", customer_id, elevator_floor);
        break;
    }
    case CUSTOMER_GIVE_UP:
    {
        printf("Current time is %d\n", Time);
        printf("Customer%d gives up in floor%d\n", customer_id, in_floor);
        break;
    }
    case ELEVATOR_OPENING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is opening the door in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_OPENED:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator door is open in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_CLOSING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is closing the door in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_CLOSED:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator door is closed in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_ACCELERATING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is speeding up and ");
        if (FiveFloorElevator->State == going_up)
        {
            printf("going up from floor%d\n", elevator_floor);
        }
        else if (FiveFloorElevator->State == going_down)
        {
            printf("going down from floor%d\n", elevator_floor);
        }
        break;
    }
    case ELEVATOR_MOVING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is moving from floor%d to floor", elevator_floor);
        if (FiveFloorElevator->State == going_up)
        {
            printf("%d\n", elevator_floor + 1);
        }
        else if (FiveFloorElevator->State == going_down)
        {
            printf("%d\n", elevator_floor - 1);
        }
        break;
    }
    case ELEVATOR_SLOWING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is slowing in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_IDLE:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is idle in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_IDLE_TO_ACCELERATING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is changing IDLE to ACCELERATING in floor%d\n", elevator_floor);
        break;
    }
    case ELEVATOR_IDLE_TO_OPENING:
    {
        printf("Current time is %d\n", Time);
        printf("FiveFloorElevator is changing IDLE to OPENING in floor%d\n", elevator_floor);
        break;
    }
    }
}