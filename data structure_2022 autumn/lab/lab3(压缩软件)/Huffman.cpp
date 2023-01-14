#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int StringLength(unsigned char *str)
{
    int i;
    for (i = 0; *(str + i) != '\0'; ++i)
        ;
    return i;
}

unsigned char *StringInsert(unsigned char *dst, unsigned char *src)
{
    int i = StringLength(dst);
    int j = 0;
    while ((dst[i++] = src[j++]))
        ;
    return dst;
}

unsigned char *StringCopy(unsigned char *dst, unsigned char *src)
{
    unsigned char *dst_copy = dst;
    while ((*dst++ = *src++))
        ;
    return dst_copy;
}

typedef struct
{
    unsigned char ch;                    //结点对应的字符
    unsigned int weight;                 //权值
    unsigned int parent, lchild, rchild; //父节点，左孩子，右孩子
} HTNode, *HuffmanTree;                  //动态分配数组存储Huffman树

typedef struct
{
    unsigned char ch;
    unsigned int weight;
} Node;

typedef unsigned char **HuffmanCode; //动态分配数组存储Huffman编码表

//求没有双亲的weight最小的两个结点
void Select(HuffmanTree HT, int i, int &s1, int &s2)
{
    unsigned int min = UINT_MAX;
    for (int cnt = 1; cnt <= i; ++cnt)
    {
        for (int j = 1; j < i; ++j)
        {
            if (HT[cnt].parent == 0 && HT[j].parent == 0 && cnt != j)
            {
                if (HT[cnt].weight + HT[j].weight < min)
                {
                    min = HT[cnt].weight + HT[j].weight;
                    s1 = cnt;
                    s2 = j;
                }
            }
        }
    }
}

//求Huffman编码并返回
// Weight数组存放n种字符的权值(要求均大于0)
void HuffmanCoding(HuffmanTree &HT, int *Weight, int n, HuffmanCode &HC)
{
    if (n <= 1)
    {
        //将要压缩的文件中字符种类过少
        //压缩没有意义，所以直接返回
        return;
    }
    int cnt = 1;
    int nodes_in_total = 2 * n - 1;                                  // n个叶子结点的Huffman树一共有2n-1个结点
    HT = (HuffmanTree)malloc((nodes_in_total + 1) * sizeof(HTNode)); // 0号单元未用
    HuffmanTree p = HT + 1;
    for (; cnt <= n; ++cnt, ++p, ++Weight)
    {
        //一开始没有父节点，左孩子，右孩子
        //故全为0
        p->ch = '0';
        p->weight = *Weight;
        p->parent = 0;
        p->lchild = 0;
        p->rchild = 0;
    }
    for (; cnt <= nodes_in_total; ++cnt, ++p)
    {
        //非叶子节点没有权值
        p->ch = '0';
        p->weight = 0;
        p->parent = 0;
        p->lchild = 0;
        p->rchild = 0;
    }
    for (cnt = n + 1; cnt <= nodes_in_total; ++cnt)
    {
        //建立Huffman树
        //在HT[1...cnt-1]中选择parent为0并且weight最小的两个结点,序号分别是s1和s2
        int s1, s2;
        Select(HT, cnt - 1, s1, s2);
        HT[s1].parent = cnt;
        HT[s2].parent = cnt;
        HT[cnt].lchild = s1;
        HT[cnt].rchild = s2;
        HT[cnt].weight = HT[s1].weight + HT[s2].weight;
    }
    //展示Huffman树
    for (int i = 1; i <= nodes_in_total; ++i)
    {
        printf("Parent:%d,Lchild:%d,Rchild:%d,Weight:%d\n", HT[i].parent, HT[i].lchild, HT[i].rchild,HT[i].weight);
    }
    // 由叶子到根逆向求Huffman编码
    HC = (HuffmanCode)malloc((n + 1) * sizeof(unsigned char *));        // 分配n个编码的头指针
    unsigned char *cd = (unsigned char *)malloc(n * sizeof(unsigned char)); //分配求编码的工作空间
    cd[n - 1] = '\0';                                                       //编码结束符
    for (cnt = 1; cnt <= n; ++cnt)
    {
        int start = n - 1;
        for (unsigned int child = cnt, parents = HT[cnt].parent; parents != 0; child = parents, parents = HT[parents].parent)
        {
            if (HT[parents].lchild == child)
                cd[--start] = '0';
            else
                cd[--start] = '1';
            HC[cnt] = (unsigned char *)malloc((n - start) * sizeof(unsigned char)); //为第cnt个字符编码分配存储空间
            StringCopy(HC[cnt], &cd[start]);
        }
    }
    free(cd);
}
//统计字符种类、频次等
int CalCharNum(int *&Weight, char *filename, unsigned char *&byte_content, int &byte_total)
{
    FILE *fp;
    unsigned char buffer[1024];
    Node byte_info[256]; //每个字符的ASCII码值等于数组元素下标
    int n = 0;           //返回字符个数
    for (int i = 0; i < 256; i++)
    {
        byte_info[i].weight = 0;
        byte_info[i].ch = '0';
    }

    fp = fopen(filename, "rb");
    if (fp == NULL)
        return -1;

    while (1)
    {
        int read_size = fread(buffer, 1, 1024, fp);
        byte_total = byte_total + read_size; //总的字节数
        if (read_size == 0)
            break;
        else
        {
            for (int i = 0; i < read_size; ++i)
            {
                byte_info[(int)buffer[i]].weight++;
                byte_info[(int)buffer[i]].ch = buffer[i];
            }
        }
    }
    for (int i = 0; i < 256; i++)
    {
        for (int j = 0; j < 255 - i; j++)
        {
            if (byte_info[j].weight <= byte_info[j + 1].weight)
            {
                Node temp;
                temp = byte_info[j];
                byte_info[j] = byte_info[j + 1];
                byte_info[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < 256 && byte_info[i].weight; ++i)
    {
        //计算出字符的种类
        //便于后续开辟内存空间
        ++n;
    }
    Weight = (int *)malloc(n * sizeof(int));
    byte_content = (unsigned char *)malloc(n * sizeof(unsigned char));
    for (int i = 0; i < n; ++i)
    {
        Weight[i] = byte_info[i].weight;
        byte_content[i] = byte_info[i].ch;
    }
    fclose(fp);
    return n;
}
int *Weight = NULL;
//压缩文件
void CompressFile(char *filename, char *compressed_filename)
{
    unsigned char ch;          //写文件的时候会用到
    unsigned char buffer[256]; //该数组用于存放在读文件的时候获取的Huffman编码
    for (int i = 0; i < 256; ++i)
    {
        //对buffer进行初始化
        buffer[i] = '\0';
    }
    unsigned char *byte_content = NULL;
    int byte_total = 0;
    FILE *fp, *fp1;
    HuffmanTree HT = NULL;
    HuffmanCode HC;
    // n代表字符种类数
    int n = CalCharNum(Weight, filename, byte_content, byte_total);
    HuffmanCoding(HT, Weight, n, HC);
    fp = fopen(compressed_filename, "wb");
    if (fp == NULL)
        return;
    fwrite(&n, sizeof(int), 1, fp); //写入字符种类数
    for (int i = 0; i < n; ++i)
    {
        //写入字符和它的权值
        fwrite(&byte_content[i], sizeof(unsigned char), 1, fp);
        fwrite(&Weight[i], sizeof(int), 1, fp);
    }
    fwrite(&byte_total, sizeof(int), 1, fp); //写入文件的总字节数
    fp1 = fopen(filename, "rb");
    if (fp1 == NULL)
        return;

    for (int i = 0; i < byte_total; ++i)
    {
        fread(&ch, sizeof(unsigned char), 1, fp1);
        for (int i = 0; i < n; ++i)
        {
            if (ch == byte_content[i])
                StringInsert(buffer, HC[i + 1]); // HC的0号单元未使用
        }
        while (StringLength(buffer) >= 8)
        {
            ch = '\0';
            for (int i = 0; i < 8; ++i)
            {
                ch <<= 1; //首先让ch左移一位
                if (buffer[i] == '1')
                    ch |= 1; // ch和1进行或运算
            }
            fwrite(&ch, sizeof(unsigned char), 1, fp);
            StringCopy(buffer, buffer + 8); //更新buffer的内容
        }
    }
    if (StringLength(buffer) > 0)
    {
        //未满1字节的情况
        ch = '\0';
        for (size_t i = 0; i < (size_t)StringLength(buffer); ++i)
        {
            ch <<= 1;
            if (buffer[i] == '1')
                ch |= 1;
        }
        ch <<= (8 - StringLength(buffer));
        fwrite(&ch, sizeof(unsigned char), 1, fp);
    }
    fclose(fp);
    fclose(fp1);
}

void UncompressFile(char *filename, char *uncompressed_filename)
{
    FILE *fp1, *fp2;            // fp1用于读，fp2用于写
    int byte_total;             //文件长度
    int byte_written_total = 0; //已经写入的字节数
    int n;                      //字符种类数
    int m;                      //结点总数
    int cnt = 1;                //循环变量
    unsigned char ch;           //读的Huffman编码
    int root;                   //根节点
    fp1 = fopen(filename, "rb");
    if (fp1 == NULL)
    {
        return;
    }
    fread(&n, sizeof(int), 1, fp1);
    //课本上n<=1直接返回，这里也这么用
    //字符种类太少，压缩解压缩毫无意义
    if (n <= 1)
        return;
    m = 2 * n - 1;
    root = m;                                           //根节点的初始化
    HuffmanTree HT = NULL;                              //字节的内容
    HT = (HuffmanTree)malloc((m + 1) * sizeof(HTNode)); // 0号单元未用
    HuffmanTree p = HT + 1;                             //循环变量
    //初始化结点信息
    for (; cnt <= n; ++cnt, ++p)
    {
        fread(&p->ch, sizeof(unsigned char), 1, fp1);
        fread(&p->weight, sizeof(int), 1, fp1);
        p->parent = 0;
        p->lchild = 0;
        p->rchild = 0;
    }
    for (; cnt <= m; ++cnt, ++p)
    {
        p->ch = '0';
        p->weight = 0;
        p->lchild = 0;
        p->rchild = 0;
        p->parent = 0;
    }
    //建立Huffman树
    for (cnt = n + 1; cnt <= m; ++cnt)
    {
        int s1, s2;
        Select(HT, cnt - 1, s1, s2);
        HT[s1].parent = cnt;
        HT[s2].parent = cnt;
        HT[cnt].lchild = s1;
        HT[cnt].rchild = s2;
        HT[cnt].weight = HT[s1].weight + HT[s2].weight;
    }
    fread(&byte_total, sizeof(int), 1, fp1);

    fp2 = fopen(uncompressed_filename, "wb");
    if (fp2 == NULL)
        return;
    while (1)
    {
        fread(&ch, sizeof(unsigned char), 1, fp1);
        for (int i = 0; i < 8; ++i)
        {
            if (ch & 0x80)
            {
                root = HT[root].rchild;
            }
            else
            {
                root = HT[root].lchild;
            }
            if (root <= n)
            {
                //此时说明已经到达了叶子结点
                fwrite(&HT[root].ch, sizeof(unsigned char), 1, fp2);
                ++byte_written_total;
                if (byte_written_total == byte_total)
                {
                    break;
                }
                root = m; //回到根节点
            }
            ch <<= 1;
        }
        if (byte_written_total == byte_total)
            break;
    }
    free(HT);
    fclose(fp1);
    fclose(fp2);
}

int main()
{
    while(1)
    {
        char sel;
        char FileName1[1000], FileName2[1000];
        printf("C-COMPRESS\n");
        printf("U-UNCOMPRESS\n");
        printf("Q-QUIT\n");
        do
        {
            printf("Please select the function:\n");
            scanf("%c", &sel);
            getchar();
        } while (sel != 'C' && sel != 'U' && sel != 'Q');
        if(sel == 'C')
        {
            printf("Input File needed to compress:\n");
            gets(FileName1);
            putchar('\n');
            printf("Input Compressed File:\n");
            gets(FileName2);
            putchar('\n');
            CompressFile(FileName1, FileName2);
        }
        else if(sel == 'U')
        {
            printf("Input Compressed File:\n");
            gets(FileName2);
            putchar('\n');
            printf("Input Uncompressed File:\n");
            gets(FileName1);
            putchar('\n');
            UncompressFile(FileName2, FileName1);
        }
        else
        {
            break;
        }
    }
    system("pause");
    return 0;
}