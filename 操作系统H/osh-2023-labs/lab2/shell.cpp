// IO
#include <iostream>
// std::string
#include <string>
// std::vector
#include <vector>
// std::string 转 int
#include <sstream>
// PATH_MAX 等常量
#include <climits>
// POSIX API
#include <unistd.h>
// wait
#include <sys/wait.h>

#include <sys/types.h>

#include <sys/stat.h>

#include <fcntl.h>

#include <signal.h>

#include <setjmp.h>

#include <algorithm>

#include <stdlib.h>

#include <pwd.h>

#include "shell.h"

int main()
{
  // 不同步 iostream 和 cstdio 的 buffer
  std::ios::sync_with_stdio(false);

  signal(SIGINT, sighandler);

  // 用来存储读入的一行命令
  std::string cmd;
  while (true)
  {

    // 返回值：若直接调用则返回0，若从siglongjmp()调用返回则返回非0值
    while (sigsetjmp(env, 1) != 0)
      ;

    // 打印提示符
    std::cout << "# ";

    // handle ctrl d
    // sth. about peek() function:
    // cin.peek()的返回值是一个char型的字符，其返回值是指针指向的当前字符，但它只是观测
    // 指针停留在当前位置并不后移；如果要访问的字符是文件结束符，则函数值是EOF(-1)
    if (std::cin.peek() == EOF)
    {
      std::cout << "\nexit" << std::endl;
      exit(0);
    }

    // 读入一行。std::getline 结果不包含换行符。
    std::getline(std::cin, cmd);

    history_cmd.push_back(cmd);
    if (history_cmd.size() > 1)
    {
      if (cmd == history_cmd[history_cmd.size() - 2])
      {
        history_cmd.pop_back();
      }
    }

    if (alias_cmd.find(cmd) != alias_cmd.end())
    {
      cmd = alias_cmd[cmd];
    }

    // 按空格分割命令为单词
    std::vector<std::string> args = split(cmd, " ");

    if (args[0][0] == '!')
    {
      if (args[0][1] == '!')
      {
        history_cmd.pop_back();
        std::cout << history_cmd[history_cmd.size() - 1] << std::endl;
        cmd = history_cmd[history_cmd.size() - 1];
        args = split(cmd, " ");
      }
      else
      {
        history_cmd.pop_back();
        args[0] = args[0].substr(1);
        int num = atoi(args[0].c_str());
        history_cmd.push_back(history_cmd[num - 1]);
        std::cout << history_cmd[num - 1] << std::endl;
        cmd = history_cmd[num - 1];
        if (history_cmd.size() > 1)
        {
          if (cmd == history_cmd[history_cmd.size() - 2])
          {
            history_cmd.pop_back();
          }
        }
        args = split(cmd, " ");
      }
    }

    // cmd is background or not
    if (args[args.size() - 1] == "&")
    {
      is_background_cmd = true;
      args.pop_back();
    }
    else
      is_background_cmd = false;

    // 没有可处理的命令
    if (args.empty())
    {
      continue;
    }

    // 退出
    if (args[0] == "exit")
    {
      if (args.size() <= 1)
      {
        return 0;
      }

      // std::string 转 int
      std::stringstream code_stream(args[1]);
      int code = 0;
      code_stream >> code;

      // 转换失败
      if (!code_stream.eof() || code_stream.fail())
      {
        std::cout << "Invalid exit code\n";
        continue;
      }

      return code;
    }

    // pwd and cd are built-in cmd.
    if (args[0] == "pwd")
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }
      std::string path;
      path.resize(PATH_MAX);
      getcwd(&path[0], path.size());
      std::cout << path << std::endl;
      continue;
    }

    if (args[0] == "cd")
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }
      int ret;
      if (args.size() <= 1)
        ret = chdir(getenv("HOME"));
      else
        ret = chdir(args[1].c_str());

      if (ret < 0)
      {
        std::cout << "shell: " << "cd: " << args[1] << ": there is no such file or directory" << std::endl;
        continue;
      }
      else
      {
        std::string path;
        path.resize(PATH_MAX);
        getcwd(&path[0], path.size());
        std::cout << path << std::endl;
        continue;
      }
    }

    if (args[0] == "wait")
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }

      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        waitpid(bg_pid[i], NULL, 0);
      }
      // std::cout << bg_pid.size() << std::endl;
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        std::cout << bg_pid[i] << "    "
                  << "finish!"
                  << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        // bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
        // bg_cmd.erase(bg_pid[i]);
      }
      bg_pid.clear();
      bg_cmd.clear();
      continue;
    }

    if (args[0] == "echo")
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }
      // support echo $SHELL cmd
      if (args[1] == "$SHELL")
      {
        std::cout << getenv("SHELL") << "\n";
        continue;
      }
      // support echo ~root cmd
      else if (args[1] == "~root")
      {
        struct passwd *pw = getpwuid(0);
        std::cout << pw->pw_dir << std::endl;
        continue;
      }
      else if (args[1] == "$HOME")
      {
        std::cout << getenv("HOME") << std::endl;
        continue;
      }
    }

    // handle history cmd
    if (args[0] == "history")
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }
      // convert the string to int
      long unsigned num = atoi(args[1].c_str());
      // if num is larger than history_cmd.size(), output all cmds
      if (num > history_cmd.size())
        num = history_cmd.size();
      for (long unsigned i = history_cmd.size() - num; i <= history_cmd.size() - 1; i++)
      {
        std::cout << "  " << i + 1 << "  " << history_cmd[i] << std::endl;
      }
      continue;
    }

    // handle alias cmd
    if (args[0] == "alias")
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }
      size_t index = cmd.find("=");
      alias_cmd[cmd.substr(6, index - 6)] = cmd.substr(index + 2, cmd.size() - index - 3);
      // std::cout << cmd.substr(6, index - 6) << std::endl;
      // std::cout << cmd.substr(index + 2, cmd.size() - index - 3) << std::endl;
      continue;
    }

    if (args.size() > 1)
    {
      if (args[1] == "env")
      {
        setenv((args[0].substr(0, args[0].find("="))).c_str(), args[0].substr(args[0].find("=") + 1).c_str(), 0);
        system("env");
        continue;
      }
    }

    // 处理外部命令
    pid_t pid = fork();

    pid_t pgid;

    if (pid == 0)
    {
      // 这里只有子进程才会进入
      // std::cout << "child process\n";

      pgid = getpid();
      setpgid(pid, pgid);

      // std::cout << pgid << "\n";
      // std::cout << getpgid(pid) << "\n";
      // std::cout << getpgid(pgid) << "\n";
      run_pipe_cmd(cmd);
      // 所以这里直接报错
      exit(255);
    }

    // 这里只有父进程（原进程）才会进入
    // std::cout << "father process\n";

    // bg_pid is used in wait cmd
    if (is_background_cmd)
    {
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }

      bg_pid.push_back(pid);
      int index = cmd.find("&");
      std::string single_bg_cmd = cmd.substr(0, index - 1);
      bg_cmd[pid] = single_bg_cmd;
      std::cout << pid << "    " << single_bg_cmd << "               will execute in background" << std::endl;
    }

    pgid = pid;
    setpgid(pid, pgid);

    // std::cout << pid <<"\n";
    // std::cout << getpgid(pid) << "\n";
    // std::cout << getpid() << "\n";
    // std::cout << getppid() << "\n";
    // std::cout << getpgid(getppid()) << "\n";

    tcsetpgrp(0, pgid);
    kill(pid, SIGCONT);

    // std::cout << getpgid(pid) << "\n";

    if (is_background_cmd)
    {
      // WNOHANG option
      // 如果pid指定的子进程没有结束，则waitpid()函数立即返回0，
      // 而不是阻塞在这个函数上等待；如果结束了，则返回该子进程的进程号
      waitpid(pid, NULL, WNOHANG);
    }
    else
    {
      // std::cout << bg_pid.size() << std::endl;
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          std::cout << bg_pid[i] << "    "
                    << "finish!"
                    << "                   " << bg_cmd[bg_pid[i]] << std::endl;
        }
      }
      for (__SIZE_TYPE__ i = 0; i < bg_pid.size(); i++)
      {
        if (waitpid(bg_pid[i], NULL, WNOHANG) != 0)
        {
          bg_pid.erase(std::find(bg_pid.begin(), bg_pid.end(), bg_pid[i]));
          bg_cmd.erase(bg_pid[i]);
          i--;
        }
      }
      wait(nullptr);
    }

    // recover the old foreground process
    signal(SIGTTOU, SIG_IGN);
    tcsetpgrp(0, getpgid(getpid()));
    signal(SIGTTOU, SIG_DFL);
  }
}
