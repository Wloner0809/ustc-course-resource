#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

int main()
{
    int n;
    std::cin >> n;
    std::string s;
    std::cin >> s;
    // odd[i]表示以i为中心的最长奇数回文串的半径长度
    std::vector<int> odd(n);
    for (int i = 0, left = 0, right = -1; i < n; i++)
    {
        int j = (i > right) ? 1 : std::min(odd[left + right - i], right - i + 1);
        while ((i - j >= 0) && (i + j < n) && (s[i - j] == s[i + j]))
            j++;
        odd[i] = j--;
        if (i + j > right)
        {
            left = i - j;
            right = i + j;
        }
    }
    // even[i]表示以i为中心的最长偶数回文串的半径长度
    std::vector<int> even(n);
    for (int i = 0, left = 0, right = -1; i < n; i++)
    {
        int j = (i > right) ? 0 : std::min(even[left + right - i + 1], right - i + 1);
        while ((i - j - 1 >= 0) && (i + j < n) && (s[i - j - 1] == s[i + j]))
            j++;
        even[i] = j--;
        if (i + j > right)
        {
            left = i - j - 1;
            right = i + j;
        }
    }
    int max = std::max(*max_element(odd.begin(), odd.end()), *max_element(even.begin(), even.end()));
    if (max == *max_element(odd.begin(), odd.end()))
    {
        // 如果是奇数回文串更长
        std::cout << 2 * max - 1;
    }
    else
    {
        // 如果是偶数回文串更长
        std::cout << 2 * max;
    }
    return 0;
}