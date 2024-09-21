#include <iostream>
#include <vector>
int main()
{
    int N, M;
    std::string S, T;
    std::cin >> N >> S >> M >> T;
    std::vector<std::vector<int>> dp(N + 1, std::vector<int>(M + 1, 0));
    std::vector<std::vector<char>> path(N + 1, std::vector<char>(M + 1, ' '));
    for (int i = 1; i <= N; i++)
    {
        for (int j = 1; j <= M; j++)
        {
            if (S[i - 1] == T[j - 1])
            {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                path[i][j] = 'D';
            }
            else if (dp[i - 1][j] >= dp[i][j - 1])
            {
                dp[i][j] = dp[i - 1][j];
                path[i][j] = 'U';
            }
            else
            {
                dp[i][j] = dp[i][j - 1];
                path[i][j] = 'L';
            }
        }
    }
    int cnt = 0;
    for (int i = N; i > 0;)
    {
        for (int j = M; j > 0;)
        {
            if (path[i][j] == 'D')
            {
                cnt++;
                i--;
                j--;
            }
            else if (path[i][j] == 'U')
            {
                i--;
            }
            else
            {
                j--;
            }
        }
    }
    std::cout << cnt << std::endl;
}