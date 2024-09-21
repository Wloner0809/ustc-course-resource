#include <iostream>
#include <vector>
bool jump(std::vector<int> distance, int M, int max_distance, int L)
{
    int cnt = 0, pre_stone = 0;
    for (int i = 0; i < distance.size(); i++)
    {
        if (distance[i] - pre_stone < max_distance && distance[i] != 0)
        {
            cnt++;
        }
        else 
        {
            pre_stone = distance[i];
        }
        if (i == distance.size() - 1 && L - pre_stone < max_distance)
        {
            cnt++;
        }
    }
    return cnt <= M;
}

int max_jump(int L, int N, int M, std::vector<int> distance)
{
    int left = 1, right = L;
    while (left < right)
    {
        int mid = (left + right + 1) / 2;
        if (jump(distance, M, mid, L))
        {
            left = mid;
        }
        else 
        {
            right = mid - 1;
        }
    }
    return left;
}

int main()
{
    int L, N, M;
    std::cin >> L >> N >> M;
    std::vector<int> distance(N);
    for (int i = 0; i < distance.size(); i++)
    {
        std::cin >> distance[i];
    }
    std::cout << max_jump(L, N, M, distance);
    return 0;
}