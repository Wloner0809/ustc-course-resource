#include <iostream>
#include <vector>
#include <algorithm>
int main()
{
    int N, result = 0;
    std::cin >> N;
    std::vector<int> dragon(N), minimum(N), reward(N);
    for (int i = 0; i < dragon.size(); i++)
    {
        std::cin >> dragon[i];
        std::vector<int> courage_value(dragon[i]);
        for (int j = 0; j < courage_value.size(); j++)
        {
            std::cin >> courage_value[j];
        }
        // calculate true min
        for (int j = 0; j < courage_value.size(); j++)
        {
            if (courage_value[j] != 0)
            {
                courage_value[j] -= j - 1;
            }
        }
        minimum[i] = *max_element(courage_value.begin(), courage_value.end());
        reward[i] = dragon[i];
    }
    int min, reward_max = 0, index = 0, courage_flower = 0;
    for (int i = 0; i < minimum.size();)
    {
        min = *min_element(minimum.begin(), minimum.end());
        for (int j = 0; j < minimum.size(); j++)
        {
            if (minimum[j] == min)
            {
                if (reward[j] >= reward_max)
                {
                    reward_max = reward[j];
                    index = j;
                }
            }
        }
        if (result == 0 && courage_flower == 0)
        {
            result = min;
            courage_flower = min + reward_max;
        }
        else if (courage_flower >= min) 
        {
            courage_flower += reward_max;
        }
        else if (courage_flower < min)
        {
            int need = min - courage_flower;
            result += need;
            courage_flower += need + reward_max;
        }
        minimum.erase(minimum.begin() + index);
        reward.erase(reward.begin() + index);
        index = 0;
        reward_max = 0;
    }
    std::cout << result;
    return 0;
}