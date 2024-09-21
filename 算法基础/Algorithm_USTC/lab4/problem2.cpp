#include <iostream>
#include <vector>
const int MOD = 1e9 + 7;
typedef std::vector<std::vector<int>> matrix;

matrix multiply(matrix &A, matrix &B)
{
    matrix C(A.size(), std::vector<int>(B[0].size()));
    for (int i = 0; i < A.size(); i++)
        for (int j = 0; j < B[0].size(); j++)
            for (int k = 0; k < B.size(); k++)
                C[i][j] = (C[i][j] + (long long)A[i][k] * B[k][j]) % MOD;
    return C;
}

matrix power(matrix A, long long p)
{
    matrix B(A.size(), std::vector<int>(A.size()));
    for (int i = 0; i < A.size(); i++)
        B[i][i] = 1;
    while (p > 0)
    {
        if (p & 1)
            B = multiply(B, A);
        A = multiply(A, A);
        p >>= 1;
    }
    return B;
}

int main()
{
    int n;
    std::cin >> n;
    matrix A(2, std::vector<int>(2));
    A[0][0] = 1;
    A[0][1] = 1;
    A[1][0] = 1;
    A[1][1] = 0;
    A = power(A, n);
    std::cout << A[1][0] << std::endl;
    return 0;
}