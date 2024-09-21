// server.c
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <pthread.h>

#define BIND_IP_ADDR "127.0.0.1"
#define BIND_PORT 8000
#define MAX_RECV_LEN 1048576
#define MAX_SEND_LEN 1048576
// 路径长度最大为4096
#define MAX_PATH_LEN 4096
#define MAX_CONN 1024

#define HTTP_STATUS_200 "200 OK"
#define HTTP_STATUS_404 "404 Not Found"
#define HTTP_STATUS_500 "500 Internal Server Error"

// 任务队列的大小
#define QUEUE_SIZE 40960
// 线程数目
#define THREAD_NUM 100

typedef struct
{
    pthread_mutex_t mutex;

    // 两个条件变量
    pthread_cond_t task_queue_not_full;
    pthread_cond_t task_queue_not_empty;

    int *task_queue;
    int task_queue_front;
    int task_queue_tail;
    int task_queue_cur_size; // 当前的队列大小

    int thread_num; // 线程池中开启的线程数
    pthread_t *threads;

} threadpool;

// 错误处理函数
void sol_error(char *error_msg)
{
    perror(error_msg);
    exit(EXIT_FAILURE);
}

int parse_request(char *request, char *path)
{
    // 返回值为-1时，说明遇到本实验未定义的错误
    // 返回值为0时，说明在该函数中没有遇到错误
    char *req = request;
    ssize_t index = 5;
    // 访问路径不会跳出当前路径
    req[3] = '.';
    // 该标志用于判断路径是否会跳出当前路径
    // 遇到"../"则标志自减，遇到"/"标志自增
    int sig_for_path = 0;
    while ((index - 3) <= MAX_PATH_LEN && req[index] != ' ')
    {
        if (req[index] == '/')
        {
            if (req[index - 1] == '.' && req[index - 2] == '.')
                sig_for_path--;
            else
                sig_for_path++;
        }
        if (sig_for_path < 0)
        {
            // 说明已经跳出当前路径
            return -1;
        }
        index++;
    }
    if ((index - 3) > MAX_PATH_LEN)
        // 说明路径超过最大
        return -1;

    memcpy(path, req + 3, (index - 2) * sizeof(char));
    path[index - 3] = '\0';

    // for(int i = 0; i < strlen("HTTP/1.0\r\nHost: 127.0.0.1:8000"); i++)
    // {
    //     printf("%c",req[index + i + 1]);
    // }
    // printf("\n");

    if (strncmp(req + index + 1, "HTTP/1.0\r\nHost: 127.0.0.1:8000\r\n", strlen("HTTP/1.0\r\nHost: 127.0.0.1:8000\r\n")) != 0 && strncmp(req + index + 1, "HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n", strlen("HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n")) != 0)
    {
        //请求头不完整
        return -1;
    }

    return 0;
}

void handle_clnt(int clnt_sock)
{
    // 读取客户端发送来的数据，并解析
    // 将clnt_sock作为一个文件描述符，读取最多MAX_RECV_LEN个字符
    char *req_buf = (char *)malloc(MAX_RECV_LEN * sizeof(char));
    // 对malloc的错误处理
    if (req_buf == NULL)
        sol_error("malloc fails!\n");
    // 此指针用于后续动态释放内存
    // 防止原指针变化，导致free()出错
    // 后面几个指向malloc分配的内存区域的指针同理
    char *req_buf_tmp = req_buf;
    req_buf[0] = '\0';
    ssize_t req_len = 0;
    ssize_t len = 0;
    // buffer存储中间过程读的内容
    char *buffer = (char *)malloc(MAX_RECV_LEN * sizeof(char));
    if (buffer == NULL)
        sol_error("malloc fails!\n");
    char *buffer_tmp = buffer;
    // 构造要返回的数据
    char *response = (char *)malloc(MAX_SEND_LEN * sizeof(char));
    if (response == NULL)
        sol_error("malloc fails!\n");
    char *response_tmp = response;
    // 分析文件
    struct stat buf;
    // 标志变量
    // 用于标志第一次循环
    int sig_for_while_loop = 0;

    while (1)
    {
        if ((len = read(clnt_sock, buffer, MAX_RECV_LEN - 1)) < 0)
            sol_error("reading clnt_sock fails!\n");
        buffer[len] = '\0';
        strcat(req_buf, buffer);

        if (sig_for_while_loop == 0)
        {
            // 处理POST请求
            if (strlen(buffer) < 5 || strncmp(buffer, "GET /", 5) != 0)
            {
                // 请求method不是GET
                sprintf(response, "HTTP/1.0 %s\r\nContent-Length: %zd\r\n\r\n", HTTP_STATUS_500, (ssize_t)0);
                ssize_t response_len = strlen(response);
                ssize_t write_len = 0;
                while (response_len > 0)
                {
                    // 通过clnt_sock向客户端发送信息
                    // 将clnt_sock作为文件描述符写内容
                    if ((write_len = write(clnt_sock, response, response_len)) < 0)
                    {
                        sol_error("writing clnt_sock fails!\n");
                    }
                    response = response + write_len;
                    response_len = response_len - write_len;
                }
                // 关闭客户端套接字
                close(clnt_sock);
                // 释放内存
                free(req_buf_tmp);
                free(buffer_tmp);
                free(response_tmp);
                return;
            }
        }

        if (!strcmp(buffer + strlen(buffer) - 4, "\r\n\r\n"))
            break;
        sig_for_while_loop = 1;
    }
    sig_for_while_loop = 0;
    req_len = strlen(req_buf);

    // 根据HTTP请求的内容，解析资源路径和Host头
    char *path = (char *)malloc(MAX_PATH_LEN * sizeof(char));
    if (path == NULL)
        sol_error("malloc fails!\n");
    char *path_tmp = path;
    int sign = parse_request(req_buf, path);

    if (sign == -1)
    {
        sprintf(response, "HTTP/1.0 %s\r\nContent-Length: %zd\r\n\r\n", HTTP_STATUS_500, (ssize_t)0);
        ssize_t response_len = strlen(response);
        ssize_t write_len = 0;
        while (response_len > 0)
        {
            if ((write_len = write(clnt_sock, response, response_len)) < 0)
                sol_error("writing clnt_sock fails!\n");
            response = response + write_len;
            response_len = response_len - write_len;
        }
        // 关闭客户端套接字
        close(clnt_sock);
        // 释放内存
        free(req_buf_tmp);
        free(buffer_tmp);
        free(response_tmp);
        free(path_tmp);
        return;
    }
    else
    {
        int fd = open(path, O_RDONLY);
        if (fd < 0)
        {
            // 说明文件打开失败
            // 对应于404 Not Found
            sprintf(response, "HTTP/1.0 %s\r\nContent-Length: %zd\r\n\r\n", HTTP_STATUS_404, (ssize_t)0);
            ssize_t response_len = strlen(response);
            ssize_t write_len = 0;
            while (response_len > 0)
            {
                if ((write_len = write(clnt_sock, response, response_len)) < 0)
                    sol_error("writing clnt_sock fails!\n");
                response = response + write_len;
                response_len = response_len - write_len;
            }
            // 关闭客户端套接字
            close(clnt_sock);
            // 释放内存
            free(req_buf_tmp);
            free(buffer_tmp);
            free(response_tmp);
            free(path_tmp);
            return;
        }
        else
        {
            if (fstat(fd, &buf) < 0)
                sol_error("Getting file attributes fails!\n");
            if (S_ISDIR(buf.st_mode))
            {
                // 说明是目录
                sprintf(response, "HTTP/1.0 %s\r\nContent-Length: %zd\r\n\r\n", HTTP_STATUS_500, (ssize_t)0);
                ssize_t response_len = strlen(response);
                ssize_t write_len = 0;
                while (response_len > 0)
                {
                    if ((write_len = write(clnt_sock, response, response_len)) < 0)
                        sol_error("writing clnt_sock fails!\n");
                    response = response + write_len;
                    response_len = response_len - write_len;
                }
                // 关闭客户端套接字
                close(clnt_sock);
                // 释放内存
                free(req_buf_tmp);
                free(buffer_tmp);
                free(response_tmp);
                free(path_tmp);
                return;
            }
            // 下面是正常读取的情况
            sprintf(response, "HTTP/1.0 %s\r\nContent-Length: %zd\r\n\r\n", HTTP_STATUS_200, (ssize_t)buf.st_size);
            ssize_t response_len = strlen(response);
            ssize_t write_len = 0;
            while (response_len > 0)
            {
                if ((write_len = write(clnt_sock, response, response_len)) < 0)
                    sol_error("writing clnt_sock fails!\n");
                response = response + write_len;
                response_len = response_len - write_len;
            }

            // 读取文件内容
            // 这里要满足文件大于1MB时也能正确读取
            char *read_file = (char *)malloc(buf.st_size * sizeof(char));
            if (read_file == NULL)
                sol_error("malloc fails!\n");
            char *read_file_tmp = read_file;
            if (read(fd, read_file, buf.st_size) < 0)
                sol_error("read file fails!\n");

            response_len = strlen(read_file);
            write_len = 0;
            while (response_len > 0)
            {
                if ((write_len = write(clnt_sock, read_file, response_len)) < 0)
                    sol_error("writing clnt_sock fails!\n");
                read_file = read_file + write_len;
                response_len = response_len - write_len;
            }
            free(read_file_tmp);
        }
    }
    // 关闭客户端套接字
    close(clnt_sock);
    // 释放内存
    free(req_buf_tmp);
    free(path_tmp);
    free(response_tmp);
    free(buffer_tmp);
}

void *threadpool_func(void *thread_pool)
{
    threadpool *pool = (threadpool *)thread_pool;
    while (1)
    {
        pthread_mutex_lock(&(pool->mutex));

        // 如果队列为空，则等待队列为非空
        while (pool->task_queue_cur_size == 0)
            pthread_cond_wait(&(pool->task_queue_not_empty), &(pool->mutex));

        // 下面取出task,相当于出队
        pool->task_queue_cur_size--;
        int clnt_sock = pool->task_queue[pool->task_queue_front];
        pool->task_queue_front = (pool->task_queue_front + 1) % QUEUE_SIZE;

        if (pool->task_queue_cur_size == (QUEUE_SIZE - 1))
            // 队列由满变为不满
            // 可以有新的task加入
            pthread_cond_broadcast(&(pool->task_queue_not_full));

        pthread_mutex_unlock(&(pool->mutex));

        // 执行task
        handle_clnt(clnt_sock);
    }
}

threadpool *threadpool_create(int thread_num, int queue_size)
{
    // 创建线程池，并初始化
    threadpool *pool = (threadpool *)malloc(sizeof(threadpool));
    if (pool == NULL)
        sol_error("malloc fails!\n");

    // if successful, return value = 0.
    if (pthread_mutex_init(&(pool->mutex), NULL))
        sol_error("init mutex fails!\n");

    if (pthread_cond_init(&(pool->task_queue_not_full), NULL))
        sol_error("init task_queue_not_full fails!\n");
    if (pthread_cond_init(&(pool->task_queue_not_empty), NULL))
        sol_error("init task_queue_not_empty fails!\n");

    pool->task_queue = (int *)malloc(sizeof(int) * queue_size);
    if (pool->task_queue == NULL)
        sol_error("malloc fails!\n");
    pool->task_queue_front = 0;
    pool->task_queue_tail = 0;
    pool->task_queue_cur_size = 0;

    pool->thread_num = thread_num;
    pool->threads = (pthread_t *)malloc(sizeof(pthread_t) * thread_num);
    if (pool->threads == NULL)
        sol_error("malloc fails!\n");

    for (int i = 0; i < thread_num; i++)
        pthread_create(&(pool->threads[i]), NULL, threadpool_func, (void *)pool);

    return pool;
}

void threadpool_add_a_task(int clnt_sock, threadpool *pool)
{
    pthread_mutex_lock(&(pool->mutex));

    while (pool->task_queue_cur_size == (QUEUE_SIZE - 1))
        // 队列满
        pthread_cond_wait(&(pool->task_queue_not_full), &(pool->mutex));

    // 下面加入task，相当于入队
    pool->task_queue_cur_size++;
    pool->task_queue[pool->task_queue_tail] = clnt_sock;
    pool->task_queue_tail = (pool->task_queue_tail + 1) % QUEUE_SIZE;

    if (pool->task_queue_cur_size > 0)
        // 队列不为空
        pthread_cond_broadcast(&(pool->task_queue_not_empty));

    pthread_mutex_unlock(&(pool->mutex));
}

int main()
{
    // 创建套接字，参数说明：
    // AF_INET: 使用IPv4
    // SOCK_STREAM: 面向连接的数据传输方式
    // IPPROTO_TCP: 使用TCP协议
    int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (serv_sock == -1)
        sol_error("creating socket fails!\n");

    // 创建线程池
    threadpool *pool = threadpool_create(THREAD_NUM, QUEUE_SIZE);

    // 将套接字和指定的IP、端口绑定
    // 用0填充serv_addr（它是一个sockaddr_in结构体）
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    // 设置IPv4
    // 设置IP地址
    // 设置端口
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(BIND_IP_ADDR);
    serv_addr.sin_port = htons(BIND_PORT);
    // 绑定
    bind(serv_sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr));

    // 使得serv_sock套接字进入监听状态，开始等待客户端发起请求
    int listen_test = listen(serv_sock, MAX_CONN);
    if (listen_test == -1)
        sol_error("listen fails!\n");

    // 接收客户端请求，获得一个可以与客户端通信的新的生成的套接字clnt_sock
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size = sizeof(clnt_addr);

    while (1) // 一直循环
    {
        // 当没有客户端连接时，accept()会阻塞程序执行，直到有客户端连接进来
        int clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_addr, &clnt_addr_size);
        if (clnt_sock == -1)
            sol_error("accept fails!\n");
        // 处理客户端的请求
        threadpool_add_a_task(clnt_sock, pool);
    }

    // 实际上这里的代码不可到达，可以在while循环中收到SIGINT信号时主动break
    // 关闭套接字
    close(serv_sock);
    return 0;
}