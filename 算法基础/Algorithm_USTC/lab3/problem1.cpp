#include <iostream>
#include <climits>
#include <vector>
#include <queue>
typedef std::pair<int, int> Pair;

class Graph
{
    int V;
    std::vector<Pair> *adjacent;

public:
    Graph(int V);
    void add_edge(int u, int v, int w);
    void prim_mst();
};

Graph::Graph(int V)
{
    this->V = V;
    adjacent = new std::vector<Pair>[V];
}

void Graph::add_edge(int u, int v, int w)
{
    adjacent[u].push_back(std::make_pair(v, w));
    adjacent[v].push_back(std::make_pair(u, w));
}

void Graph::prim_mst()
{
    std::priority_queue<Pair, std::vector<Pair>, std::greater<Pair>> Q; // 小根堆
    int src = 0;                                                        // 从0号顶点开始
    std::vector<int> weight(V, INT_MAX);                                // 用于存储顶点权值, 初始化为无穷大
    std::vector<int> parent(V, -1);                                     // 用于存储顶点的父节点, 初始化为-1
    std::vector<bool> node_in_mst(V, false);                            // 用于存储顶点是否已经在mst中, 初始化为false
    Q.push(std::make_pair(0, src));                                     // 将0号顶点加入小根堆
    weight[src] = 0;
    while (!Q.empty())
    {
        int u = Q.top().second; // 取出堆顶元素
        Q.pop();
        node_in_mst[u] = true; // 将顶点加入mst
        for (auto i = adjacent[u].begin(); i != adjacent[u].end(); i++)
        {
            int v = (*i).first;
            int w = (*i).second;
            if (node_in_mst[v] == false && weight[v] > w)
            {
                weight[v] = w;
                Q.push(std::make_pair(weight[v], v));
                parent[v] = u;
            }
        }
    }
    int weight_sum = 0;
    for (int i = 1; i < V; i++)
    {
        if (weight[i] != INT_MAX)
        {
            weight_sum += weight[i];
        }
        else // 有顶点不可达
        {
            std::cout << "-1" << std::endl;
            return;
        }
    }
    std::cout << weight_sum << std::endl;
    return;
}

int main()
{
    int N, M;
    std::cin >> N >> M;
    Graph g(N);
    for (int i = 0; i < M; i++)
    {
        int u, v, w;
        std::cin >> u >> v >> w;
        g.add_edge(u - 1, v - 1, w);
    }
    g.prim_mst();
    return 0;
}