#include <iostream>
#include <vector>
#include <algorithm>
#define MAX 0x7fffffff
int main()
{
    int L = 0, N = 0, M = 0;
    std::cin >> L >> N >> M;
    // input distances between stones and Start point
    std::vector<int> distance_S(N);
    for (int i = 0; i < N; i++)
    {
        std::cin >> distance_S[i];
    }
    // init: calculate distances between stones
    std::vector<int> distance_stone(N + 1);
    // solve the stone on the start point or on the end point
    for (int i = 0; i <= N; i++)
    {
        if (i == 0)
        {
            if (distance_S[0] == 0)
            {
                distance_stone[0] = L;
            }
            else 
            {
                distance_stone[0] = distance_S[0];
            }
        }
        else if (i == N)
        {
            if (distance_S[N - 1] == L)
            {
                distance_stone[N] = L;
            }
            else 
            {
                distance_stone[N] = L - distance_S[N - 1];
            }
        }
        else 
            distance_stone[i] = distance_S[i] - distance_S[i - 1];
    }
    std::vector<int> suitable_stone(N + 1, MAX);
    int loop = M;
    while (loop > 0)
    {
        int min = *min_element(distance_stone.begin(), distance_stone.end());
        for (int i = 0; i < distance_stone.size(); i++)
        {
            if (i == distance_stone.size() - 1 && distance_stone[i] == min)
            {
                suitable_stone[i] = min + distance_stone[i - 1];
            }
            else if (distance_stone[i] == min)
            {
                suitable_stone[i] = min + distance_stone[i + 1];
            }
        }
        min = *min_element(suitable_stone.begin(), suitable_stone.end());
        for (int i = 0; i < suitable_stone.size(); i++)
        {
            if (min == suitable_stone[i] && distance_stone[i] != L)
            {
                if (i == suitable_stone.size() - 1)
                {
                    distance_stone[distance_stone.size() - 2] += distance_stone[distance_stone.size() - 1];
                    distance_stone.erase(distance_stone.begin() + i);
                }
                else if (i == suitable_stone.size() - 2 && distance_stone[i + 1] == L)
                {
                    if (i - 1 >= 0)
                    {
                        distance_stone[i - 1] += distance_stone[i];
                        distance_stone.erase(distance_stone.begin() + i);
                    }
                    else 
                    {
                        distance_stone.erase(distance_stone.begin() + i);
                    }
                }
                else
                {
                    distance_stone[i + 1] += distance_stone[i];
                    distance_stone.erase(distance_stone.begin() + i);
                }
                suitable_stone.erase(suitable_stone.begin() + i);
                break;
            }
            else if (min == suitable_stone[i] && distance_stone[i] == L)
            {
                distance_stone.erase(distance_stone.begin() + i);
                suitable_stone.erase(suitable_stone.begin() + i);
                break;
            }
        }
        std::fill(suitable_stone.begin(), suitable_stone.end(), MAX);
        loop--;
    }
    std::cout << *min_element(distance_stone.begin(), distance_stone.end());
    return 0;
}

