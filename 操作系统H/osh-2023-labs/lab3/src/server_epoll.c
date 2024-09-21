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
#include <sys/epoll.h>
#include <limits.h>
#include <sys/sendfile.h>

#define BIND_IP_ADDR "127.0.0.1"
#define BIND_PORT 8000
#define MAX_RECV_LEN 1048576
#define MAX_SEND_LEN 1048576
// 路径长度最大为4096
#define MAX_PATH_LEN 4096
#define MAX_HOST_LEN 1024
#define MAX_CONN 1024

#define MAX_EVENTS 100

#define HTTP_STATUS_200 "200 OK"
#define HTTP_STATUS_404 "404 Not Found"
#define HTTP_STATUS_500 "500 Internal Server Error"

int sock_2_fd[INT_MAX];

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
        // 请求头不完整
        return -1;
    }

    return 0;
}

int handle_clnt(int clnt_sock)
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
                // 释放内存
                free(req_buf_tmp);
                free(buffer_tmp);
                free(response_tmp);
                return 0;
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
        // 释放内存
        free(req_buf_tmp);
        free(buffer_tmp);
        free(response_tmp);
        free(path_tmp);
        return 0;
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
            // 释放内存
            free(req_buf_tmp);
            free(buffer_tmp);
            free(response_tmp);
            free(path_tmp);
            return 0;
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
                // 释放内存
                free(req_buf_tmp);
                free(buffer_tmp);
                free(response_tmp);
                free(path_tmp);
                return 0;
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
            // 释放内存
            free(req_buf_tmp);
            free(path_tmp);
            free(response_tmp);
            free(buffer_tmp);
            return fd;
        }
    }
}

void handle_file(int fd, int clnt_sock)
{
    // test
    // printf("%d\n",fd);
    // printf("%d\n",clnt_sock);
    struct stat buf;
    fstat(fd, &buf);
    sendfile(clnt_sock, fd, NULL, buf.st_size);
}

void handle_epoll(int serv_sock)
{
    int epfd = epoll_create1(0);
    struct epoll_event ev, ep_event_list[MAX_EVENTS];
    // 接收客户端请求，获得一个可以与客户端通信的新的生成的套接字clnt_sock
    struct sockaddr_in clnt_addr;
    socklen_t clnt_addr_size = sizeof(clnt_addr);

    ev.data.fd = serv_sock;
    epoll_ctl(epfd, EPOLL_CTL_ADD, serv_sock, &ev);

    while (1)
    {
        int cnt = epoll_wait(epfd, ep_event_list, MAX_EVENTS, -1);

        for (int i = 0; i < cnt; i++)
        {
            if (ep_event_list[i].data.fd == serv_sock)
            {
                // 当没有客户端连接时，accept()会阻塞程序执行，直到有客户端连接进来
                int clnt_sock = accept(serv_sock, (struct sockaddr *)&clnt_addr, &clnt_addr_size);
                ev.events = EPOLLIN;
                ev.data.fd = clnt_sock;
                epoll_ctl(epfd, EPOLL_CTL_ADD, clnt_sock, &ev);
            }
            else if (ep_event_list[i].events == EPOLLIN)
            {
                int ret = 0;
                if ((ret = handle_clnt(ep_event_list[i].data.fd)) != 0)
                {
                    sock_2_fd[ep_event_list[i].data.fd] = ret;
                    ev.events = EPOLLOUT;
                    ev.data.fd = ep_event_list[i].data.fd;
                    epoll_ctl(epfd, EPOLL_CTL_MOD, ep_event_list[i].data.fd, &ev);
                }
            }
            else if (ep_event_list[i].events == EPOLLOUT)
            {
                // test
                //  printf("%d\n",sock_2_fd[ep_event_list[i].data.fd]);
                handle_file(sock_2_fd[ep_event_list[i].data.fd], ep_event_list[i].data.fd);
                sock_2_fd[ep_event_list[i].data.fd] = 0;
                close(ep_event_list[i].data.fd);
            }
            else
            {
                close(ep_event_list[i].data.fd);
            }
        }
    }
}

int main()
{
    // 创建套接字，参数说明：
    // AF_INET: 使用IPv4
    // SOCK_STREAM: 面向连接的数据传输方式
    // IPPROTO_TCP: 使用TCP协议
    int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    
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
    listen(serv_sock, MAX_CONN);

    handle_epoll(serv_sock);

    // 实际上这里的代码不可到达，可以在while循环中收到SIGINT信号时主动break
    // 关闭套接字
    close(serv_sock);
    return 0;
}