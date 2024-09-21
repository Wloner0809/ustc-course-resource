#include <iostream>
int main()
{
    long long int N;
    std::cin >> N;
    long long int *salary = new long long int[N];
    long long int *dp = new long long int[N];
    for (long long int i = 0; i < N; i++)
    {
        std::cin >> salary[i];
    }
    if (N == 0)
    {
        std::cout << 0 << std::endl;
        return 0;
    }
    else if (N == 1)
    {
        std::cout << salary[0] << std::endl;
        return 0;
    }
    else
    {
        dp[0] = salary[0];
        dp[1] = std::max(salary[0], salary[1]);
        for (long long int i = 2; i < N; i++)
        {
            dp[i] = std::max(dp[i - 1], dp[i - 2] + salary[i]);
        }
        std::cout << dp[N - 1] << std::endl;
        return 0;
    }
}