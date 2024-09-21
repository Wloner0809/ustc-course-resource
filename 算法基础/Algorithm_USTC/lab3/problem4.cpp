#include <iostream>
#include <vector>
#include <queue>
#define MOD 1000000007

int main()
{
    int N, M;
    std::cin >> N >> M;
    std::vector<int> g[N + 1];
    bool visit[N + 1] = {false};
    int dist[N + 1] = {0};
    int count[N + 1] = {0};
    for (int i = 1; i <= M; i++)
    {
        int u, v;
        std::cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    std::queue<int> Q;
    Q.push(1);
    visit[1] = true;
    dist[1] = 0;
    count[1] = 1;
    while (!Q.empty())
    {
        int u = Q.front();
        Q.pop();
        for (int i = 0; i < g[u].size(); i++)
        {
            int v = g[u][i];
            if (!visit[v])
            {
                visit[v] = true;
                dist[v] = dist[u] + 1;
                count[v] = count[u];
                Q.push(v);
            }
            else if (dist[v] == dist[u] + 1)
            {
                count[v] = (count[v] + count[u]) % MOD;
            }
        }
    }
    for (int i = 2; i <= N; i++)
    {
        std::cout << count[i] << std::endl;
    }
    return 0;
}