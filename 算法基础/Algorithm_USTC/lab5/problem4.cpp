#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
#define MAX1 55555
#define MAX2 11111
std::vector<int> Graph[MAX1];
int scc_cnt = 0;
int scc[MAX2];
int visit[MAX2];
void dfs(int);

int main()
{
    int N, M, u, v;
    int in[MAX2], out[MAX2]; // in[i]表示第i个强连通分量的入度，out[i]表示第i个强连通分量的出度
    std::cin >> N >> M;
    for (int i = 0; i < M; i++)
    {
        std::cin >> u >> v;
        Graph[u].push_back(v);
    }
    for (int i = 1; i <= N; i++)
    {
        if (!visit[i])
            dfs(i);
    }
    for (int i = 1; i <= N; i++)
    {
        for (int j = 0; j < Graph[i].size(); j++)
        {
            //(i,G[i][j])是一条边
            if (scc[i] != scc[Graph[i][j]])
            {
                in[scc[Graph[i][j]]]++; // 不是同一个块，则j的入度++
                out[scc[i]]++;          // 不是同一个块，则i的出度++
            }
        }
    }
    int eat = 0;
    for (int i = 1; i <= scc_cnt; i++)
    {
        if (in[i] == 0)
            eat++;
    }
    if (eat > 1)
        std::cout << "0 ";
    else
    {
        eat = 0;
        for (int i = 1; i <= N; i++)
        {
            if (in[scc[i]] == 0)
                eat++; // 输出入度0的块内所有点
        }
        std::cout << eat << " ";
    }
    int be_eaten = 0;
    for (int i = 1; i <= scc_cnt; i++)
    {
        if (out[i] == 0)
            be_eaten++;
    }
    if (be_eaten > 1)
        std::cout << 0;
    else
    {
        be_eaten = 0;
        for (int i = 1; i <= N; i++)
        {
            if (out[scc[i]] == 0)
                be_eaten++; // 输出出度0的块内所有点
        }
        std::cout << be_eaten;
    }
    return 0;
}

std::stack<int> stack;
int dfs_time = 0;
int low[MAX2];
void dfs(int u)
{
    visit[u] = low[u] = ++dfs_time;
    stack.push(u);
    for (int i = 0; i < Graph[u].size(); i++)
    {
        int v = Graph[u][i];
        if (!visit[v])
        {
            dfs(v);
            low[u] = std::min(low[u], low[v]);
        }
        else if (!scc[v])
        {
            low[u] = std::min(low[u], visit[v]);
        }
    }
    if (low[u] == visit[u])
    {
        scc_cnt = scc_cnt + 1;
        while (1)
        {
            int node = stack.top();
            stack.pop();
            scc[node] = scc_cnt;
            if (node == u)
                break;
        }
    }
}