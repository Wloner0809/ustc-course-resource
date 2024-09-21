#include <iostream>
#include <vector>
#include <queue>
#define MOD 1000000007

int main()
{
    int N, M;
    std::cin >> N >> M;
    std::vector<std::vector<int>> adjacent(N + 1, std::vector<int>(N + 1, 0));
    std::vector<int> in_degree(N + 1, 0);
    std::vector<int> out_degree(N + 1, 0);
    std::queue<int> Q;
    std::vector<int> path(N + 1, 0);
    for (int i = 1; i <= M; i++)
    {
        int u, v;
        std::cin >> u >> v;
        adjacent[u].push_back(v);
        in_degree[v]++;
        out_degree[u]++;
    }
    for (int i = 1; i <= N; i++)
    {
        if (in_degree[i] == 0)
        {
            Q.push(i);
            path[i] = 1;
        }
    }
    while (!Q.empty())
    {
        int top = Q.front();
        Q.pop();
        for (int i = 0; i < adjacent[top].size(); i++)
        {
            int v = adjacent[top][i];
            in_degree[v]--;
            path[v] = (path[v] + path[top]) % MOD;
            if (in_degree[v] == 0)
                Q.push(v);
        }
    }
    int count = 0;
    for (int i = 1; i <= N; i++)
    {
        if (out_degree[i] == 0)
        {
            count = (count + path[i]) % MOD;
        }
    }
    std::cout << count;
    return 0;
}