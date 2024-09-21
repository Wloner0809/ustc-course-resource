#include <iostream>
#include <stack>
using namespace std;

int main()
{
    int N;
    cin >> N;
    int *G = new int[N];
    int *num = new int[N];
    for (int i = 0; i < N; i++)
    {
        cin >> G[i];
        num[i] = 0;
    }
    stack<int> stack1;
    // 相当于每个位置向左看
    for (int i = 0; i < N; i++)
    {
        while (!stack1.empty() && stack1.top() > G[i])
        {
            stack1.pop();
        }
        stack1.push(G[i]);
        if (i == 0)
        {
            num[i] += 0;
        }
        else
        {
            num[i] += stack1.size() - 1;
        
        }
    }
    stack<int> stack2;
    // 相当于每个位置向右看
    for (int i = N - 1; i >= 0; i--)
    {
        while (!stack2.empty() && stack2.top() > G[i])
        {
            stack2.pop();
        }
        stack2.push(G[i]);
        if (i == N - 1)
        {
            num[i] += 0;
        }
        else
        {
            num[i] += stack2.size() - 1;
        }
    }
    for (int i = 0; i < N; i++)
    {
        cout << num[i];
        if (i != N - 1)
            cout << " ";
    }
    return 0;
}