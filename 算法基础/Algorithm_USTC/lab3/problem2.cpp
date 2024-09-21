#include <iostream>
#include <memory.h>
#define MAX 555
int n, m, e;
int g[MAX][MAX];
int match[MAX];
bool visit[MAX];
bool dfs(int u)
{
    for (int v = 1; v <= m; v++)
    {
        if (g[u][v] && !visit[v])
        {
            visit[v] = true;
            if (match[v] == 0 || dfs(match[v]))
            {
                match[v] = u;
                return true;
            }
        }
    }
    return false;
}
int main()
{
    std::cin >> n >> m >> e;
    for (int i = 1; i <= e; i++)
    {
        int u, v;
        std::cin >> u >> v;
        g[u][v] = 1;
    }
    int ans = 0;
    for (int i = 1; i <= n; i++)
    {
        memset(visit, 0, sizeof(visit));
        if (dfs(i))
            ans++;
    }
    std::cout << ans << std::endl;
    return 0;
}