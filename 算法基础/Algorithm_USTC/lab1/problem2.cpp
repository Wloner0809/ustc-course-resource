#include <iostream>
#include <array>
#define LENGTH 45
long long combination(int n, int m)
{
    // calculate C_n^m
    if (m == 0)
        return 1;
    int large = n, small = m < (n - m) ? m : n - m;
    long long denominator = small, numerator = large;
    std::array<int, LENGTH> array;
    array.fill(1);
    for (int i = small - 1; i > 0; i--)
    {
        denominator *= i;
    }
    // this is used to solve longlong overflow
    for (int i = large - 1; i > large - small; i--)
    {
        numerator *= i;
        for (int j = small; j > 0; j--)
        {
            if (numerator % j == 0 && array[j])
            {
                denominator /= j;
                numerator /= j;
                array[j] = 0;
            }
        }
    }
    return numerator / denominator;
}
int main()
{
    int N, two_num = 0, one_num = 0;
    long long result = 0;
    std::cin >> N;
    two_num = N / 2;
    for (int i = two_num; i >= 0; i--)
    {
        one_num = N - 2 * i;
        if (one_num == N)
        {
            result += 1;
        }
        else 
        {
            result += combination(one_num + i, one_num);
        }
    }
    std::cout << result;
    return 0;
}