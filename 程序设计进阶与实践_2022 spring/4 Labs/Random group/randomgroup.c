#include <stdio.h>
#include <stdlib.h>
#include<string.h>
#include <time.h>
#define NAME 15
#define PROJECT 6
#define STUDENTNUMBER 200
#define COUNT 300 //随机打乱数组的次数，数字越大打得越乱
//分组的下限是20上限是40
#define LOWERLIMIT 20
#define UPPERLIMIT 40
//如果人数少于20移动的人的位置
#define POSITION 10
//意向值占比0.25
//熟悉程度占比0.75
#define I_Percent 0.25
#define P_percent 0.75
struct randomgroup
{
    char studentName[NAME];
    int studentID;
    int intention[PROJECT];   //对每个项目的意向值
    int banID;                //一定不组队的人的编号
    int proficiency[PROJECT]; //对项目的熟练程度
    double weightedValue;     //意向值和对项目的熟练程度的加权值
} student[STUDENTNUMBER];
//用来存放对感兴趣项目的学生ID
int projectIntention[PROJECT][STUDENTNUMBER];
int projectStudentNumber[PROJECT];
int ProjectGroupInfo[PROJECT][8][6];
//意向考量(判断意向值作为初筛)
//将其放在意向高的那一个项目
//如果对多个项目意向相同且最大，任选一个即可
void chooseAGroup(void)
{
    int Project[PROJECT] = {0};
    for (int i = 0; i < STUDENTNUMBER; i++)
    {
        int maxIntention = 0;
        int project = 0;
        int count = 0;
        for (; count < PROJECT; count++)
        {
            if (maxIntention <= student[i].intention[count])
            {
                maxIntention = student[i].intention[count];
                project = count;
            }
        }
        //把学生的编号放在projectIntention数组里面
        //方便之后调用学生信息
        projectIntention[project][Project[project]++] = i;
        projectStudentNumber[project]++;
    }
}
//计算人数爆掉的某个项目中成员的加权值
void calculateWeightedValue(int project)
{
    for (int i = 0; i < projectStudentNumber[project]; i++)
    {
        student[projectIntention[project][i]].weightedValue = student[projectIntention[project][i]].intention[i] * I_Percent + student[projectIntention[project][i]].proficiency[i] * P_percent;
    }
}
//从人数爆掉的组里踢人并丢进人数最少的组
int Min_Person(void)
{
    int min = UPPERLIMIT;
    int Min_Group = -1;
    for (int i = 0; i < PROJECT; i++)
    {
        if (projectStudentNumber[i] < min)
        {
            min = projectStudentNumber[i];
            Min_Group = i;
        }
    }
    return Min_Group;
}
int Max_Person(void)
{
    int max = LOWERLIMIT;
    int Max_Group = -1;
    for (int i = 0; i < PROJECT; i++)
    {
        if (projectStudentNumber[i] > max)
        {
            max = projectStudentNumber[i];
            Max_Group = i;
        }
    }
    return Max_Group;
}
//从porject1中的STU_ID号的学生放在project2的末尾
//并改变对应项目的学生人数
void Move(int project1, int project2, int STU_ID)
{
    projectIntention[project2][projectStudentNumber[project2]] = projectIntention[project1][STU_ID];
    projectStudentNumber[project2]++;
    for (int i = STU_ID; i < projectStudentNumber[project1] - 1; i++)
    {
        projectIntention[project1][i] = projectIntention[project1][i + 1];
    }
    projectStudentNumber[project1]--;
}
void BorrowPerson(int project)
{
    while (projectStudentNumber[project] < LOWERLIMIT)
    {
        Move(Max_Person(), project, POSITION);
    }
}
//通过权重选出分数最低的学生并移动到人数最少的组
void KickPerson(int project)
{
    double Rank[STUDENTNUMBER][2];
    int i, min, student_mark;
    calculateWeightedValue(project);
    for (int i = 0; i < projectStudentNumber[project]; i++)
    {
        Rank[i][0] = projectIntention[project][i];
        Rank[i][1] = student[projectIntention[project][i]].weightedValue;
    }
    while (projectStudentNumber[project] > UPPERLIMIT)
    {
        min = 10;
        student_mark = -1;
        for (i = 0; i < projectStudentNumber[project]; i++)
        {
            if (Rank[i][1] < min)
            {
                min = Rank[i][1];
                student_mark = i;
            }
        }
        Move(project, Min_Person(), student_mark);
    }
}
void clean()
{
    memset(projectStudentNumber, 0, PROJECT * sizeof(int));
    memset(projectIntention, -1, PROJECT * STUDENTNUMBER * sizeof(int));
    memset(ProjectGroupInfo, -1, PROJECT * 8 * 6 * sizeof(int));
}
//检查是否有与banID冲突的分组方式
int Check(int Temp[])
{
    int i, j;
    int mark = 0;
    for (i = 0; i < 49; i++)
    {
        if (Temp[i] == -1)
        {
            mark = i;
            continue;
        }
        for (j = mark + 1; j < mark + 7; j++)
        {
            if (Temp[j] == -1)
                break;
            if (Temp[j] == student[Temp[i]].banID)
                return 0;
        }
    }
    return 1;
}
void swap(int Swap[], int a, int b)
{
    int temp;
    temp = Swap[a];
    Swap[a] = Swap[b];
    Swap[b] = temp;
}
//计算出各组的人数和组数并通过交换随机位号打乱学生顺序然后顺次填入
void Group(int project)
{
    srand((unsigned)time(NULL));
    int Swap[40];
    int Temp[50];
    int r1, r2, mark;
    int i, j, k;
    memset(Temp, -1, 50 * sizeof(int));
    memset(Swap, -1, 40 * sizeof(int));
    int Group_Num = projectStudentNumber[project] / 5;
    int Six_Num = projectStudentNumber[project] - 5 * Group_Num;
    while (1)
    {
        for (int i = 0; i < projectStudentNumber[project]; i++)
        {
            Swap[i] = projectIntention[project][i];
        }
        memset(Temp, -1, 50 * sizeof(int));
        for (int count = 0; count < COUNT; count++)
        {
            r1 = rand() % (projectStudentNumber[project] - 1);
            r2 = rand() % (projectStudentNumber[project] - 1);
            swap(Swap, r1, r2);
        }
        mark = 0;
        Temp[0] = -1;
        for (i = 0; i < Six_Num; i++)
        {
            for (j = 1; j <= 6; j++)
            {
                Temp[mark + j] = Swap[6 * i + j - 1];
            }
            Temp[mark + 7] = -1;
            mark += 7;
        }
        for (i = 0; i < Group_Num - Six_Num; i++)
        {
            for (j = 1; j <= 5; j++)
            {
                Temp[mark + j] = Swap[6 * Six_Num + 5 * i + j - 1];
            }
            Temp[mark + 6] = -1;
            mark += 6;
        }
        memset(Swap, -1, 40 * sizeof(int));
        if (Check(Temp))
            break;
    }
    j = 0;
    k = 0;
    for (i = 1; i < 50; i++)
    {
        if (Temp[i] == -1 && j < 7)
        {
            j++;
            k = 0;
            continue;
        }
        ProjectGroupInfo[project][j][k++] = Temp[i];
    }
}
void generateInfo(void)
{
    srand((unsigned)time(NULL));
    char studentName[STUDENTNUMBER][NAME];
    int studentID;
    int intention[PROJECT];
    int banID;
    int proficiency[PROJECT];
    double weightedValue;
    FILE *fp1 = fopen("name.txt", "r");
    FILE *fp2 = fopen("Info.xls", "w+");
    for (int i = 0; i < STUDENTNUMBER; i++)
    {
        fscanf(fp1, "%s", studentName[i]);
    }
    for (int i = 0; i < STUDENTNUMBER; i++)
    {
        studentID = i;
        //学号整除20的人有banID
        if (i % 20 == 0)
        {
            banID = rand() % 200;
        }
        else
        {
            banID = -1;
        }
        weightedValue = 0;
        for (int j = 0; j < PROJECT; j++)
        {
            intention[j] = rand() % 11;
            proficiency[j] = rand() % 11;
        }
        fprintf(fp2, "%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%lf\n", studentName[i], studentID,
                intention[0], intention[1], intention[2], intention[3], intention[4], intention[5], banID, proficiency[0], proficiency[1],
                proficiency[2], proficiency[3], proficiency[4], proficiency[5], weightedValue);
    }
    fclose(fp1);
    fclose(fp2);
}
void ReadInfo(void)
{
    FILE *fp = fopen("Info.xls", "r");
    for (int i = 0; i < STUDENTNUMBER; i++)
    {
        fscanf(fp, "%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d %lf", student[i].studentName, &student[i].studentID,
               &student[i].intention[0], &student[i].intention[1], &student[i].intention[2], &student[i].intention[3], &student[i].intention[4],
               &student[i].intention[5], &student[i].banID, &student[i].proficiency[0], &student[i].proficiency[1],
               &student[i].proficiency[2], &student[i].proficiency[3], &student[i].proficiency[4], &student[i].proficiency[5], &student[i].weightedValue);
    }
}
void Output()
{
    int i, j, k;
    FILE *fp3 = fopen("Output.xls", "w+");
    for (i = 0; i < 6; i++)
    {
        fprintf(fp3, "Project %d\n", i + 1);
        for (j = 0; j < 8; j++)
        {
            if (ProjectGroupInfo[i][j][0] == -1)
            {
                continue;
            }
            else
            {
                fprintf(fp3, "Group %d\n", j + 1);
            }
            for (k = 0; k < 6; k++)
            {
                if (ProjectGroupInfo[i][j][k] != -1)
                {
                    fprintf(fp3, "%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n", student[ProjectGroupInfo[i][j][k]].studentName, student[ProjectGroupInfo[i][j][k]].studentID,
                            student[ProjectGroupInfo[i][j][k]].intention[0], student[ProjectGroupInfo[i][j][k]].intention[1], student[ProjectGroupInfo[i][j][k]].intention[2], student[ProjectGroupInfo[i][j][k]].intention[3], student[ProjectGroupInfo[i][j][k]].intention[4],
                            student[ProjectGroupInfo[i][j][k]].intention[5], student[ProjectGroupInfo[i][j][k]].banID, student[ProjectGroupInfo[i][j][k]].proficiency[0], student[ProjectGroupInfo[i][j][k]].proficiency[1],
                            student[ProjectGroupInfo[i][j][k]].proficiency[2], student[ProjectGroupInfo[i][j][k]].proficiency[3], student[ProjectGroupInfo[i][j][k]].proficiency[4], student[ProjectGroupInfo[i][j][k]].proficiency[5]);
                }
            }
        }
    }
    fclose(fp3);
}
int main()
{
    clean();
    generateInfo();
    ReadInfo();
    chooseAGroup();
    for (int i = 0; i < PROJECT; i++)
    {
        if (projectStudentNumber[i] > UPPERLIMIT)
        {
            KickPerson(i);
        }
        if (projectStudentNumber[i] < LOWERLIMIT)
        {
            BorrowPerson(i);
        }
    }
    for (int j = 0; j < PROJECT; j++)
    {
        Group(j);
    }
    Output();
    system("Output.xls");
    return 0;
}