
void run_cmd(std::vector<std::string>);
void run_redi_cmd(std::vector<std::string>);
void run_pipe_cmd(std::string);
void sighandler(int);
std::vector<std::string> split(std::string s, const std::string &delimiter);

// used in handling ctrl c
sigjmp_buf env;
// a sign for background cmd
bool is_background_cmd;
// store bg_pid
std::vector<pid_t> bg_pid;
// used in history cmd
std::vector<std::string> history_cmd;
// used in alias cmd
std::unordered_map<std::string, std::string> alias_cmd;
// store bg cmd
std::unordered_map<pid_t, std::string> bg_cmd;

// 经典的 cpp string split 实现
// https://stackoverflow.com/a/14266139/11691878
std::vector<std::string> split(std::string s, const std::string &delimiter)
{
  std::vector<std::string> res;
  size_t pos = 0;
  std::string token;
  while ((pos = s.find(delimiter)) != std::string::npos)
  {
    token = s.substr(0, pos);
    res.push_back(token);
    s = s.substr(pos + delimiter.length());
  }
  res.push_back(s);
  return res;
}

void run_cmd(std::vector<std::string> args)
{
  // std::vector<std::string> 转 char **
  char *arg_ptrs[args.size() + 1];
  for (__SIZE_TYPE__ i = 0; i < args.size(); i++)
  {
    arg_ptrs[i] = &args[i][0];
  }
  // exec p 系列的 argv 需要以 nullptr 结尾
  arg_ptrs[args.size()] = nullptr;
  execvp(args[0].c_str(), arg_ptrs);
}

void run_redi_cmd(std::vector<std::string> args)
{
  std::vector<std::string>::iterator index;
  while (find(args.begin(), args.end(), ">") != args.end() || find(args.begin(), args.end(), ">>") != args.end() || find(args.begin(), args.end(), "<") != args.end())
  {
    if (find(args.begin(), args.end(), ">") != args.end())
    {
      index = find(args.begin(), args.end(), ">");
      int fd = open((*(index + 1)).c_str(), O_WRONLY | O_TRUNC | O_CREAT, S_IRWXU | S_IRWXG | S_IRWXO);
      dup2(fd, 1);
      close(fd);
      // "%" is regarded as a sign
      // which can help delete.
      *index = "%";
      *(index + 1) = "%";
    }
    else if (find(args.begin(), args.end(), ">>") != args.end())
    {
      index = find(args.begin(), args.end(), ">>");
      int fd = open((*(index + 1)).c_str(), O_APPEND | O_RDWR | O_CREAT, S_IRWXU | S_IRWXG | S_IRWXO);
      dup2(fd, 1);
      close(fd);
      *index = "%";
      *(index + 1) = "%";
    }
    else if (find(args.begin(), args.end(), "<") != args.end())
    {
      index = find(args.begin(), args.end(), "<");
      int fd = open((*(index + 1)).c_str(), O_RDONLY);
      dup2(fd, 0);
      close(fd);
      *index = "%";
      *(index + 1) = "%";
    }
  }
  args.erase(remove(args.begin(), args.end(), "%"), args.end());
  run_cmd(args);
  return;
}

void run_pipe_cmd(std::string cmd)
{
  // split the cmd with " | ", pay attention to space.
  // In fact, I just let "|" have one space before "|" and after "|"
  std::vector<std::string> pipe_args = split(cmd, " | ");

  // note that cmd may have "&"
  // so I need to judge if there is "&"
  // if it does, I will pop it

  if (pipe_args.size() == 1)
  {
    // there is no "|"
    std::vector<std::string> args = split(cmd, " ");
    if (args[args.size() - 1] == "&")
      args.pop_back();
    run_redi_cmd(args);
  }
  else
  {
    // let read_end's default value = STDIN_FILENO
    int read_end = 0;
    for (__SIZE_TYPE__ i = 0; i < pipe_args.size(); i++)
    {
      int fd[2];
      // the number of "|" is pipe_args.size() - 1
      if (i < pipe_args.size() - 1)
      {
        pipe(fd);
      }
      pid_t pid = fork();
      if (pid == 0)
      {
        dup2(read_end, 0);
        if (i < pipe_args.size() - 1)
        {
          dup2(fd[1], 1);
        }
        std::vector<std::string> args = split(pipe_args[i], " ");
        if (args[args.size() - 1] == "&")
          args.pop_back();
        run_redi_cmd(args);
      }
      else
      {
        close(fd[1]);
        if (i > 0)
          close(read_end);
        if (i < pipe_args.size() - 1)
          read_end = fd[0];
      }
    }
    while (wait(nullptr) > 0)
      ;
  }
}

void sighandler(int sig)
{
  if (sig == SIGINT)
  {
    std::cout << std::endl;
    // the result of STFW:
    // https://stackoverflow.com/questions/16828378/readline-get-a-new-prompt-on-sigint
    siglongjmp(env, 1);
  }
}
