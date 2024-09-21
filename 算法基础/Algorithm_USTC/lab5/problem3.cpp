#include <iostream>
#include <queue>
#include <algorithm>
#define MAX 555555
#define MAX_ 3000
const int inf = 0x3fffffff;
using namespace std;
int  visit[MAX], pre[MAX], head[MAX];
long long distances[MAX];

long long max_flow = 0, c;
int N, M, S, T, u, v, total = 1, flag[MAX_][MAX_];

struct node
{
    long long val;
    int to;
    int net;
} edge[MAX];

// bfs寻找增广路
bool bfs();

int main()
{
    cin >> N >> M >> S >> T;
    for (int i = 1; i <= M; i++)
    {
        cin >> u >> v >> c;
        // 处理重边的操作
        if (flag[u][v] == 0)
        {
            total++;
            edge[total].val = c;
            edge[total].to = v;
            edge[total].net = head[u];
            head[u] = total;

            total++;
            edge[total].val = 0;
            edge[total].to = u;
            edge[total].net = head[v];
            head[v] = total;
            flag[u][v] = total;
        }
        else
        {
            edge[flag[u][v] - 1].val += c;
        }
    }
    while (bfs())
    {
        int node = T;
        while (node != S)
        {
            int v = pre[node];
            edge[v].val -= distances[T];
            edge[v ^ 1].val += distances[T];
            node = edge[v ^ 1].to;
        }
        max_flow += distances[T]; // 累加每一条增广路经的最小流量值
    }
    cout << max_flow << endl;
    return 0;
}

bool bfs()
{
    for (int i = 1; i <= N; i++)
        visit[i] = 0;
    queue<int> q;
    q.push(S);
    visit[S] = 1;
    distances[S] = inf;
    while (!q.empty())
    {
        int node = q.front();
        q.pop();
        for (int i = head[node]; i; i = edge[i].net)
        {
            if (edge[i].val == 0)
                continue;
            int v = edge[i].to;
            if (visit[v] == 1)
                continue;
            distances[v] = min(edge[i].val, distances[node]);
            pre[v] = i;
            q.push(v);
            visit[v] = 1;
            if (v == T)
                return true;
        }
    }
    return false;
}