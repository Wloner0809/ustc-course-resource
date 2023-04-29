#include"customer.c"

//电梯在某层楼上停留时是否有乘客进出
bool NoCustomerInOut(void)
{
    if (!StackEmpty(FiveFloorElevator->CustomerStack[FiveFloorElevator->Floor]))
        return false; //当前楼层上的栈不为空,说明有人要出电梯
    if (CustomerUpQueue[FiveFloorElevator->Floor]->CustomerNumber && FiveFloorElevator->CustomerNumber < CAPACITY && FiveFloorElevator->State == going_up)
        return false; //当前楼层上升队列不为空,且电梯人未满,且电梯上行,说明有人进电梯
    if (CustomerDownQueue[FiveFloorElevator->Floor]->CustomerNumber && FiveFloorElevator->CustomerNumber < CAPACITY && FiveFloorElevator->State == going_down)
        return false;
    if (FiveFloorElevator->customer_in_out_timer > 0)
        return false; //说明正在有人进出
    return true;
}

void ChangeElevatorActivity(void)
{
    int cnt;        //用于计数
    int signal = 1; //用在MOVING中
    switch (FiveFloorElevator->activity)
    {
    case OPENING:
    {
        //开门时置D1和D2非0值
        FiveFloorElevator->D1 = 1;
        FiveFloorElevator->D2 = 1;
        FiveFloorElevator->activity = OPENED;
        FiveFloorElevator->activity_timer = door_test_time;
        DisplayInfo(ELEVATOR_OPENED, 0, 0, 0, FiveFloorElevator->Floor);
        break;
    }
    case OPENED:
    {
        if (NoCustomerInOut())
        {
            //无人进出D1为0,D3为0
            FiveFloorElevator->D1 = 0;
            FiveFloorElevator->D3 = 0;
            FiveFloorElevator->activity = CLOSING;
            FiveFloorElevator->activity_timer = open_close_door_time;
            DisplayInfo(ELEVATOR_CLOSING, 0, 0, 0, FiveFloorElevator->Floor);
        }
        else
        {
            //有人进出时电梯每隔40t测试一次
            FiveFloorElevator->activity_timer = door_test_time;
        }
        break;
    }
    case CLOSING:
    {
        if (FiveFloorElevator->D1 == 0)
        {
            FiveFloorElevator->D3 = 1;
            FiveFloorElevator->activity = CLOSED;
            DisplayInfo(ELEVATOR_CLOSED, 0, 0, 0, FiveFloorElevator->Floor);
        }
        else
        { //在关门期间有人到来
            FiveFloorElevator->D3 = 1;
            FiveFloorElevator->activity = OPENING;
            FiveFloorElevator->activity_timer = open_close_door_time;
            DisplayInfo(ELEVATOR_OPENING, 0, 0, 0, FiveFloorElevator->Floor);
        }
        break;
    }
    //门已经关闭
    case CLOSED:
    { //准备移动
        FiveFloorElevator->CallCar[FiveFloorElevator->Floor] = 0;
        if (!NoCustomerInOut())
        {
            FiveFloorElevator->D3 = 1;
            FiveFloorElevator->activity = OPENING;
            FiveFloorElevator->activity_timer = open_close_door_time;
            DisplayInfo(ELEVATOR_OPENING, 0, 0, 0, FiveFloorElevator->Floor);
            break;
        }
        if (FiveFloorElevator->State == going_up)
        {
            if (CustomerUpQueue[FiveFloorElevator->Floor]->CustomerNumber)
                CallUp[FiveFloorElevator->Floor] = 1;
            else
                CallUp[FiveFloorElevator->Floor] = 0;

            //如果有CallCar[cnt]成立则加速上升
            for (cnt = FiveFloorElevator->Floor + 1; cnt <= MAXFLOOR; cnt++)
            {
                if (FiveFloorElevator->CallCar[cnt])
                {
                    FiveFloorElevator->activity = ACCELERATING;
                    FiveFloorElevator->activity_timer = accelerate_time;
                    DisplayInfo(ELEVATOR_ACCELERATING, 0, 0, 0, FiveFloorElevator->Floor);
                    break;
                }
            }
            //没有则停下
            if (cnt == MAXFLOOR + 1)
            {
                FiveFloorElevator->activity = IDLE;
                FiveFloorElevator->activity_timer = elevator_max_wait_time;
                FiveFloorElevator->State = idle;
                DisplayInfo(ELEVATOR_IDLE, 0, 0, 0, FiveFloorElevator->Floor);
            }
        }
        else if (FiveFloorElevator->State == going_down)
        {
            if (CustomerDownQueue[FiveFloorElevator->Floor]->CustomerNumber)
                CallDown[FiveFloorElevator->Floor] = 1;
            else
                CallDown[FiveFloorElevator->Floor] = 0;
            for (cnt = FiveFloorElevator->Floor - 1; cnt >= 0; cnt--)
            {
                if (FiveFloorElevator->CallCar[cnt])
                {
                    FiveFloorElevator->activity = ACCELERATING;
                    FiveFloorElevator->activity_timer = accelerate_time;
                    DisplayInfo(ELEVATOR_ACCELERATING, 0, 0, 0, FiveFloorElevator->Floor);
                    break;
                }
            }
            if (cnt == -1)
            {
                FiveFloorElevator->activity = IDLE;
                FiveFloorElevator->activity_timer = elevator_max_wait_time;
                FiveFloorElevator->State = idle;
                DisplayInfo(ELEVATOR_IDLE, 0, 0, 0, FiveFloorElevator->Floor);
            }
        }
        else
            ;
        break;
    }
    case ACCELERATING:
    {
        FiveFloorElevator->activity = MOVING;
        if (FiveFloorElevator->State == going_up)
            FiveFloorElevator->activity_timer = up_wait_time;
        else
            FiveFloorElevator->activity_timer = down_wait_time;
        DisplayInfo(ELEVATOR_MOVING, 0, 0, 0, FiveFloorElevator->Floor);
        break;
    }
    case MOVING:
    {
        if (FiveFloorElevator->State == going_up)
        {
            if (FiveFloorElevator->Floor < MAXFLOOR)
            {
                ++(FiveFloorElevator->Floor);
                if (FiveFloorElevator->Floor == MAXFLOOR)
                {
                    FiveFloorElevator->StateChange = 1; //状态需要改变
                    FiveFloorElevator->activity = SLOWING;
                    FiveFloorElevator->activity_timer = up_slow_time;
                    DisplayInfo(ELEVATOR_SLOWING, 0, 0, 0, FiveFloorElevator->Floor);
                }
                else
                {
                    // signal默认值是1
                    for (int i = FiveFloorElevator->Floor + 1; i <= MAXFLOOR; i++)
                    {
                        if (!(CallUp[i] == 0 && CallDown[i] == 0 && FiveFloorElevator->CallCar[i] == 0))
                        {
                            signal = 0;
                            break;
                        }
                        signal = 1;
                    }
                    if (CallUp[FiveFloorElevator->Floor] == 1 || FiveFloorElevator->CallCar[FiveFloorElevator->Floor] == 1 || ((FiveFloorElevator->Floor == 1 || CallDown[FiveFloorElevator->Floor] == 1) && signal))
                    {
                        if (CallDown[FiveFloorElevator->Floor] == 1 && signal)
                        {
                            FiveFloorElevator->StateChange = 1; //状态需要改变，状态是上、下、停
                        }
                        FiveFloorElevator->activity = SLOWING;
                        FiveFloorElevator->activity_timer = up_slow_time;
                        DisplayInfo(ELEVATOR_SLOWING, 0, 0, 0, FiveFloorElevator->Floor);
                    }
                    else
                    {
                        FiveFloorElevator->activity_timer = up_wait_time;
                        DisplayInfo(ELEVATOR_MOVING, 0, 0, 0, FiveFloorElevator->Floor);
                    }
                }
            }
            //下面是已经到达最高层的情况
            else
            {
                FiveFloorElevator->StateChange = 1; //状态需要改变
                FiveFloorElevator->activity = SLOWING;
                FiveFloorElevator->activity_timer = up_slow_time;
                DisplayInfo(ELEVATOR_SLOWING, 0, 0, 0, FiveFloorElevator->Floor);
            }
        }
        else if (FiveFloorElevator->State == going_down)
        {
            if (FiveFloorElevator->Floor > 0)
            {
                --(FiveFloorElevator->Floor);
                if (FiveFloorElevator->Floor == 0)
                {
                    FiveFloorElevator->StateChange = 1; //状态需要改变
                    FiveFloorElevator->activity = SLOWING;
                    FiveFloorElevator->activity_timer = down_slow_time;
                    DisplayInfo(ELEVATOR_SLOWING, 0, 0, 0, FiveFloorElevator->Floor);
                }

                else
                {
                    for (int i = FiveFloorElevator->Floor - 1; i >= 0; i--)
                    {
                        if (!(CallUp[i] == 0 && CallDown[i] == 0 && FiveFloorElevator->CallCar[i] == 0))
                        {
                            signal = 0;
                            break;
                        }
                        signal = 1;
                    }
                    if (CallDown[FiveFloorElevator->Floor] == 1 || FiveFloorElevator->CallCar[FiveFloorElevator->Floor] == 1 || ((FiveFloorElevator->Floor == 1 || CallUp[FiveFloorElevator->Floor] == 1) && signal))
                    {
                        if (CallUp[FiveFloorElevator->Floor] == 1 && signal)
                        {
                            FiveFloorElevator->StateChange = 1; //状态需要改变
                        }
                        FiveFloorElevator->activity = SLOWING;
                        FiveFloorElevator->activity_timer = down_slow_time;
                        DisplayInfo(ELEVATOR_SLOWING, 0, 0, 0, FiveFloorElevator->Floor);
                    }
                    else
                    {
                        FiveFloorElevator->activity_timer = down_wait_time;
                        DisplayInfo(ELEVATOR_MOVING, 0, 0, 0, FiveFloorElevator->Floor);
                    }
                }
            }
            //下面是电梯到达最低层的情况
            else
            {
                FiveFloorElevator->StateChange = 1; //状态需要改变
                FiveFloorElevator->activity = SLOWING;
                FiveFloorElevator->activity_timer = down_slow_time;
                DisplayInfo(ELEVATOR_SLOWING, 0, 0, 0, FiveFloorElevator->Floor);
            }
        }
        else
            ;
        break;
    }
    case SLOWING:
    {
        //进到SLOWING下一个活动就是OPENING
        FiveFloorElevator->CallCar[FiveFloorElevator->Floor] = 0;
        FiveFloorElevator->activity = OPENING;
        FiveFloorElevator->activity_timer = open_close_door_time;
        DisplayInfo(ELEVATOR_OPENING, 0, 0, 0, FiveFloorElevator->Floor);
        if (FiveFloorElevator->State == going_up)
        {
            if (FiveFloorElevator->StateChange) //状态需要改变
                FiveFloorElevator->State = going_down;
            FiveFloorElevator->StateChange = 0;
        }
        else if (FiveFloorElevator->State == going_down)
        {
            if (FiveFloorElevator->StateChange)
                FiveFloorElevator->State = going_up;
            FiveFloorElevator->StateChange = 0;
        }
        else
            ;
    }
    case IDLE:
    {
        if (FiveFloorElevator->Floor == 1)
        {
            //在一层的话保持IDLE等300t
            FiveFloorElevator->activity_timer = elevator_max_wait_time;
        }
        else
        {
            //在别的层需要返回到一层IDLE
            if (FiveFloorElevator->Floor > 1)
                FiveFloorElevator->State = going_down;
            else
                FiveFloorElevator->State = going_up;
            FiveFloorElevator->CallCar[1] = 1;
            FiveFloorElevator->activity = ACCELERATING;
            FiveFloorElevator->activity_timer = accelerate_time;
            DisplayInfo(ELEVATOR_ACCELERATING, 0, 0, 0, FiveFloorElevator->Floor);
        }
        break;
    }
    }
}

//当在电梯停候时,寻找最近的被按下的按钮
//该按钮不在本层中
int FindClosestButton(int floor)
{
    int i, j, close;
    //这里单独讨论floor为0和4的情况
    if (floor == MAXFLOOR)
    {
        for (i = MAXFLOOR - 1; i >= 0; --i)
        {
            if (CallUp[i] || CallDown[i])
            {
                close = i;
                break;
            }
        }
    }
    else if (floor == 0)
    {
        for (i = 1; i <= MAXFLOOR; ++i)
        {
            if (CallUp[i] || CallDown[i])
            {
                close = i;
                break;
            }
        }
    }
    else
    {
        for (i = floor + 1; i <= MAXFLOOR; i++)
        {
            if (CallUp[i] || CallDown[i])
                break;
        }
        for (j = floor - 1; j >= 0; j--)
        {
            if (CallUp[j] || CallDown[j])
                break;
        }
        if (i == MAXFLOOR + 1 && j == -1)
            close = -1;
        else if (i == MAXFLOOR + 1)
        {
            close = j;
        }
        else if (j == -1)
        {
            close = i;
        }
        else
        {
            close = (abs(floor - i) <= abs(floor - j) ? i : j);
        }
    }
    return close;
}

//电梯处于IDLE活动中
//改变此时的电梯状态和活动
void ChangeIDLEActivity(void)
{
    if (FiveFloorElevator->activity == IDLE)
    {
        if (CallUp[FiveFloorElevator->Floor])
        {
            //当前楼层有向上按钮被按下
            CallUp[FiveFloorElevator->Floor] = 0;
            FiveFloorElevator->activity = OPENING;
            FiveFloorElevator->activity_timer = open_close_door_time;
            FiveFloorElevator->State = going_up;
            DisplayInfo(ELEVATOR_IDLE_TO_OPENING, 0, 0, 0, FiveFloorElevator->Floor);
        }
        else if (CallDown[FiveFloorElevator->Floor])
        {
            //当前楼层有向下按钮被按下
            CallDown[FiveFloorElevator->Floor] = 0;
            FiveFloorElevator->activity = OPENING;
            FiveFloorElevator->activity_timer = open_close_door_time;
            FiveFloorElevator->State = going_down;
            DisplayInfo(ELEVATOR_IDLE_TO_OPENING, 0, 0, 0, FiveFloorElevator->Floor);
        }
        else
        {
            int closest_button = FindClosestButton(FiveFloorElevator->Floor);
            // closest_button不是-1说明临近的楼层有按钮被按下
            if (closest_button != -1)
            {
                if (closest_button < FiveFloorElevator->Floor)
                {
                    //当前楼层大于将要去的楼层
                    FiveFloorElevator->State = going_down;
                    FiveFloorElevator->activity = ACCELERATING;
                    FiveFloorElevator->activity_timer = accelerate_time;
                    DisplayInfo(ELEVATOR_IDLE_TO_ACCELERATING, 0, 0, 0, FiveFloorElevator->Floor);
                }
                else
                {
                    FiveFloorElevator->activity = ACCELERATING;
                    FiveFloorElevator->activity_timer = accelerate_time;
                    FiveFloorElevator->State = going_up;
                    DisplayInfo(ELEVATOR_IDLE_TO_ACCELERATING, 0, 0, 0, FiveFloorElevator->Floor);
                }
            }
        }
    }
}