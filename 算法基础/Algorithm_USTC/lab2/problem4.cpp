#include <iostream>
#include <vector>
#define MAX 500
int main()
{
    int N;
    std::cin >> N;
    std::vector<int> sum(MAX);
    std::vector<std::vector<int>> dp(MAX, std::vector<int>(MAX, 0x7fffffff));
    for (int i = 1; i <= N; i++)
    {
        std::cin >> sum[i];
        dp[i][i] = 0;
    }
    for (int i = 2; i <= N; i++)
    {
        sum[i] = sum[i - 1] + sum[i];
    }
    for (int l = 2; l <= N; l++)
    {
        for (int i = 1; i <= N - l + 1; i++)
        {
            int j = i + l - 1;
            for (int k = i; k <= j - 1; k++)
            {
                dp[i][j] = std::min(dp[i][j], dp[i][k] + dp[k + 1][j] + sum[j] - sum[i - 1]);
            }
        }
    }
    std::cout << dp[1][N] << std::endl;
}