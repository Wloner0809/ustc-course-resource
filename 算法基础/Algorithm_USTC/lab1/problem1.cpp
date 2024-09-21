#include <iostream>
#include <vector>
int main()
{
    int N, M;
    int num = 0;
    std::cin >> N >> M;
    std::vector<int> array1, array2;
    for (int i = 0; i < N; i++)
    {
        std::cin >> num;
        array1.push_back(num);
    }
    for (int i = 0; i < M; i++)
    {
        std::cin >> num;
        array2.push_back(num);
    } 
    int index1 = 0, index2 = 0;
    while(index1 < N && index2 < M)
    {
        if (array1[index1] <= array2[index2])
        {
            std::cout << array1[index1++] << " ";
        }
        else 
        {
            std::cout << array2[index2++] << " ";
        }
    }
    while (index1 < N)
    {
        std::cout << array1[index1];
        if (index1 != N - 1)
        {
            std::cout << " ";
        }
        index1++;
    }
    while (index2 < M)
    {
        std::cout << array2[index2];
        if (index2 != M - 1)
        {
            std::cout << " ";
        }
        index2++;
    }
    return 0;
}