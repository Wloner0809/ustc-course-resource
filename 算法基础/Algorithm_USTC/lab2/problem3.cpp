#include <iostream>
#define MAX_NODE 1111
#define CASE 2
struct edge
{
    int v, next;
} edge[MAX_NODE];

int visit[MAX_NODE], a[MAX_NODE], dp[MAX_NODE][CASE];

void dfs(int node)
{
    visit[node] = 1;
    for (int i = a[node]; i; i = edge[i].next)
    {
        int v = edge[i].v;
        if (!visit[v])
        {
            dfs(v);
            dp[node][1] += dp[v][0];
            dp[node][0] += std::max(dp[v][0], dp[v][1]);
        }
    }
}

int main()
{
    int N;
    std::cin >> N;
    int count = 0;
    for (int i = 1; i <= N; i++)
    {
        std::cin >> dp[i][1];
    }
    bool root[MAX_NODE];
    for (int i = 1; i <= N; i++)
    {
        root[i] = true;
    }
    for (int i = 1; i <= N - 1; i++)
    {
        int u, v;
        std::cin >> u >> v;
        edge[++count].v = u;
        edge[count].next = a[v];
        a[v] = count;
        root[u] = false;
    }
    for (int i = 1; i <= N; i++)
    {
        if (root[i])
        {
            dfs(i);
            std::cout << std::max(dp[i][0], dp[i][1]) << std::endl;
            return 0;
        }
    }
}