#include <iostream>
#include <vector>
const int MAX = 48000;
const int LENGTH = 1000000;
int main()
{
    long long int L, R;
    int count = 0;
    std::cin >> L >> R;
    L = (L == 1) ? 2 : L;
    std::vector<bool> no_prime(LENGTH, false);
    std::vector<int> prime;
    for (int i = 2; i <= MAX; i++)
    {
        if (!no_prime[i])
        {
            prime.push_back(i);
            for (int j = 0; i * prime[j] <= MAX; j++)
            {
                no_prime[i * prime[j]] = true;
                if (i % prime[j] == 0)
                    break;
            }
        }
    }
    std::vector<bool> not_prime(LENGTH, false);
    for (int i = 0; i < prime.size(); i++)
    {
        int p = prime[i];
        long long int start = (L + p - 1) / p * p > 2 * p ? (L + p - 1) / p * p : 2 * p;
        for (long long int j = start; j <= R; j += p)
            not_prime[j - L] = true;
    }
    for (int i = 0; i <= R - L; i++)
        if (!not_prime[i])
        {
            count++;
        }
    std::cout << count << std::endl;
    return 0;
}