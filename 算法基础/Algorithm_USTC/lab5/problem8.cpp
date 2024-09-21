#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <queue>
using namespace std;

int count_unique_substrings(string s, int n)
{
    long long base = 131;
    long long mod = 1e9 + 7;
    long long prime = 233317;

    vector<long long> b_pow(n);
    b_pow[0] = 1;
    for (int i = 1; i < n; i++)
        b_pow[i] = (b_pow[i - 1] * base) % mod;

    vector<long long> h(n + 1, 0);
    for (int i = 0; i < n; i++)
        h[i + 1] = (h[i] + (s[i] - 'a' + 1) * b_pow[i]) % mod;

    vector<long long> maximum(n);
    for (int l = 1; l <= n; l++)
    {
        unordered_map<long long, long long> map;
        for (int i = 0; i <= n - l; i++)
        {
            long long cur_h = (h[i + l] + mod - h[i]) % mod;
            cur_h = (cur_h * b_pow[n - i - 1]) % mod + prime;
            map[cur_h]++; // 记录每个长度为l的子串出现的次数
        }
        // 把map里面的最大值放进去
        for (auto it : map)
            maximum[l - 1] = max(maximum[l - 1], it.second);
        maximum[l - 1] = maximum[l - 1] * l;
        map.clear();
    }
    return *max_element(maximum.begin(), maximum.end());
}

int main()
{
    int n;
    cin >> n;
    string s;
    cin >> s;
    cout << count_unique_substrings(s, n);
    return 0;
}