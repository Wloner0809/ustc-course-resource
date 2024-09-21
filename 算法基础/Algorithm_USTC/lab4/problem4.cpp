#include <iostream>
#include <string>
#include <vector>
int main()
{
    int N, M;
    std::cin >> N >> M;
    std::string S, T;
    std::cin >> S >> T;
    std::vector<int> position;
    int count = 0;
    // KMP算法
    std::vector<int> next(M);
    next[0] = -1;
    for (int i = 1, j = -1; i < M; ++i)
    {
        while (j != -1 && T[i] != T[j + 1])
            j = next[j];
        if (T[i] == T[j + 1])
            ++j;
        next[i] = j;
    }
    for (int i = 0, j = -1; i < N; ++i)
    {
        while (j != -1 && S[i] != T[j + 1])
            j = next[j];
        if (S[i] == T[j + 1])
            ++j;
        if (j == M - 1)
        {
            position.push_back(i - M + 1);
            count++;
            j = next[j];
        }
    }
    std::cout << count << std::endl;
    for (int k = 0; k <= position.size() - 1; k++)
    {
        std::cout << position[k];
        if (k != position.size() - 1)
            std::cout << " ";
    }
    return 0;
}