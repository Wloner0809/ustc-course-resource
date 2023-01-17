#include<cstdint>
#include<iostream>
#include<fstream>

#define MAXLEN  100
#ifndef  LENGTH
#define LENGTH  3
#endif

int16_t lab1(int16_t a, int16_t b)
{
    int16_t cnt = 0;
    int16_t and_bit = 1;
    while(b)
    {
        if(a & and_bit)
            cnt++;
        and_bit = and_bit + and_bit;
        --b;
    }
    return cnt;
}

int16_t lab2(int16_t p, int16_t q, int16_t n)
{
    int16_t result1 = 1, result2 = 1, result;   //result1是F(N-2),result2是F(N-1)
    int16_t result1_mod, result2_mod;
    int16_t mod_p = p - 1;
    while(n >= 2)
    {
        result1_mod = result1 & mod_p;
        result2_mod = result2 - q;
        while(result2_mod > 0)
        {
            result2_mod = result2_mod - q;
        }
        //result2_mod小于0的情况
        if(result2_mod)
            result2_mod = result2_mod + q;
        result = result1_mod + result2_mod;
        result1 = result2;
        result2 = result;
        n--;
    }
    return result;
}

int16_t lab3(int16_t n, char s[])
{
    int16_t max = 0, max_mid = 0;
    char letter = s[0];
    for (int i = 0; i < n; ++i)
    {
        if(s[i] == letter)
            max_mid++;
        else
        {
            letter = s[i];
            if(max < max_mid)
                max = max_mid;
            max_mid = 1;
        }
    }
    return max > max_mid ? max : max_mid;
}

void lab4(int16_t score[], int16_t *a, int16_t *b)
{
    int16_t temp, min;
    *a = 0;
    *b = 0;
    for (int i = 0; i < 15; ++i)
    {
        min = i;
        for (int j = i + 1; j < 16; ++j)
        {
            if(score[j] < score[min])
            {
                min = j;
            }
        }
        if (min != i)
        {
            temp = score[i];
            score[i] = score[min];
            score[min] = temp;
        }
    }
    for (int i = 15; i >= 8; --i)
    {
        if(score[i] >= 85)
        {
            if(*a < 4)
                ++*a;
            else if(*a == 4)
                ++*b;
        }
        else if(score[i] >= 75)
        {
            ++*b;
        }
    }
}

int main()
{
    std::fstream file;
    //在我的电脑上相对路径不太好用，所以我用了绝对路径
    //助教可能要修改一下路径
    file.open("E:\\vscode.c\\ICS\\Lab6\\test.txt", std::ios::in);

    //lab1
    int16_t a = 0, b = 0;
    for (int i = 0; i < LENGTH; ++i)
    {
        file >> a >> b;
        std::cout << lab1(a, b) << std::endl;
    }

    //lab2
    int16_t p = 0, q = 0, n = 0;
    for (int i = 0; i < LENGTH; ++i)
    {
        file >> p >> q >> n;
        std::cout << lab2(p, q, n) << std::endl;
    }

    //lab3
    char s[MAXLEN];
    for (int i = 0; i < LENGTH; ++i)
    {
        file >> n >> s;
        std::cout << lab3(n, s) << std::endl;
    }

    //lab4
    int16_t score[16];
    for (int i = 0; i < LENGTH; ++i)
    {
        for (int j = 0; j < 16; ++j)
        {
            file >> score[j];
        }
        lab4(score, &a, &b);
        for (int j = 0; j < 16; ++j)
        {
            std::cout << score[j] << " ";
        }
        std::cout << std::endl
                  << a << " " << b << std::endl;
    }

    file.close();
    system("pause");
    return 0;
}