#include "elevator.c"

void Init(void)
{
    FiveFloorElevator = (ElevatorPtr)malloc((MAXFLOOR + 1) * sizeof(Elevator));
    FiveFloorElevator->activity = IDLE;
    FiveFloorElevator->activity_timer = elevator_max_wait_time;
    for (int i = 0; i <= MAXFLOOR; i++)
    {
        FiveFloorElevator->CallCar[i] = 0;
    }
    FiveFloorElevator->customer_in_out_timer = 0;
    FiveFloorElevator->CustomerNumber = 0;
    for (int i = 0; i <= MAXFLOOR; i++)
    {
        FiveFloorElevator->CustomerStack[i] = (CustomerStackPtr)malloc(sizeof(CustomerStack));
        InitStack(FiveFloorElevator->CustomerStack[i]);
    }
    FiveFloorElevator->D1 = 0;
    FiveFloorElevator->D2 = 0;
    FiveFloorElevator->D3 = 0;
    FiveFloorElevator->Floor = 1;
    FiveFloorElevator->State = idle;
    FiveFloorElevator->StateChange = 0;
    for (int i = 0; i <= MAXFLOOR; i++)
    {
        CallUp[i] = 0;
        CallDown[i] = 0;
    }
    for (int i = 0; i <= MAXFLOOR; i++)
    {
        CustomerUpQueue[i] = (CustomerWaitQueuePtr)malloc(sizeof(CustomerWaitQueue));
        InitQueue(CustomerUpQueue[i]);
    }
    for (int i = 0; i <= MAXFLOOR; i++)
    {
        CustomerDownQueue[i] = (CustomerWaitQueuePtr)malloc(sizeof(CustomerWaitQueue));
        InitQueue(CustomerDownQueue[i]);
    }
}

void SimulateElevator(void)
{
    Init();
    srand((unsigned)time(NULL));
    while (Time < MAXTIME)
    {
        if (CustomerInterTime == 0)
            CreateNewCustomer();
        else
            CustomerInterTime--;
        for (int i = 0; i <= MAXFLOOR; i++)
        {
            CheckUpQueueCustomerGiveUp(i);
            CheckDownQueueCustomerGiveUp(i);
        }
        ChangeIDLEActivity();
        if (FiveFloorElevator->activity == OPENED)
        {
            if (FiveFloorElevator->customer_in_out_timer == 0)
            {
                //先出后进
                if (CustomerOut())
                    FiveFloorElevator->customer_in_out_timer = customer_inout_time;
                else if (CustomerIn())
                    FiveFloorElevator->customer_in_out_timer = customer_inout_time;
            }
            else
                FiveFloorElevator->customer_in_out_timer--;
        }
        if (FiveFloorElevator->activity_timer == 0)
            ChangeElevatorActivity();
        else
            FiveFloorElevator->activity_timer--;

        Time++;
        Sleep(100);
    }
}

int main()
{
    SimulateElevator();
    system("pause");
    return 0;
}