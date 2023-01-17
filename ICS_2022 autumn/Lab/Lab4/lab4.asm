    .ORIG	x3000
    LD	R0,	NUM
    AND R1, R1, #0
    LD  R1, NUM      ;R0控制外层循环,R1控制内层循环
    NOT	R1,	R1
    ADD	R1,	R1,	#1  ;R1取反加1

OUTLOOP
    ADD R0, R0, #-1
    BRn	STOP        ;外层循环完毕，终止程序
    LD	R2,	AD      ;R2存储分数所在的地址
    LD	R7,	AD      ;默认最大值的地址在x4000
    LDR	R3,	R2,	#0  ;R3存储第一个分数(初始化)，R3存放的是每次内循环的最大值
    ADD	R2,	R2,	#1
    LDR	R4,	R2,	#0  ;R4存储第二个分数(初始化)
    AND	R5,	R5,	#0  ;R5在开始内存循环之前要更新为0

INLOOP
    ADD	R5,	R5,	#1  
    ADD	R6,	R5,	R1
    BRz STORE       ;内层循环结束，返回外层循环
    NOT	R6,	R4
    ADD	R6,	R6,	#1  ;R4取反加1
    ADD	R6,	R3,	R6  
    BRn	LESS        ;R3小于R4的情况
    ADD	R2,	R2,	#1  ;更新地址
    LDR	R4,	R2,	#0  ;读取下一个分数
    BRnzp	INLOOP

STORE
    AND	R6,	R6,	#0  ;把最大值变为0
    STR	R6,	R7,	#0
    LD	R6,	WD
    ADD	R6,	R6,	R0  ;更新写地址
    STR	R3,	R6,	#0  ;把当前的最大值写入相应的地址当中
    BRnzp	OUTLOOP

LESS
    AND	R3,	R3,	#0
    ADD	R3,	R3,	R4  ;把R4赋值给R3，R3存放的是每次循环的最大值
    AND	R7,	R7,	#0  ;R7存放每次循环最大值的地址
    ADD	R7,	R7,	R2
    ADD	R2,	R2,	#1  ;更新地址
    LDR	R4,	R2,	#0  ;读取下一个分数
    BRnzp	INLOOP

STOP                ;这部分用于统计A和B的人数
    AND	R0,	R0,	#0
    AND	R1,	R1,	#0
    AND R2, R2, #0
    AND	R3,	R3,	#0
    AND	R4,	R4,	#0
    AND	R5,	R5,	#0
    AND R6, R6, #0
    AND	R7,	R7,	#0
    LD	R0,	SCOREA  ;R0存放的是85分
    NOT	R0,	R0
    ADD	R0,	R0,	#1
    LD	R1,	SCOREB  ;R1存放的是75分
    NOT R1, R1
    ADD	R1,	R1,	#1
    ADD	R2,	R2,	#4  ;R2存放的是4人
    NOT	R2,	R2
    ADD R2, R2, #1
    ADD	R3,	R3,	#8  ;R3存放的是8人
    NOT R3, R3
    ADD R3, R3, #1
    LD  R4, WD
    ADD	R4,	R4,	x000F

ALOOP
    LDR	R5,	R4, #0  ;R5存放的是现在读进来的分数
    ADD	R5,	R5,	R0
    BRn BLOOP
    ADD	R5,	R6,	R2
    BRz	BLOOP
    ADD	R6,	R6,	#1  ;R6记录A的人数
    ADD	R4,	R4,	#-1
    BRnzp ALOOP

BLOOP
    LDR	R5,	R4,	#0
    ADD	R5,	R5,	R1  ;分数小于75
    BRn OUTPUT
    ADD	R5,	R7,	R6
    ADD R5, R5, R3  ;正好8人
    BRz OUTPUT
    ADD	R7,	R7,	#1  ;R7记录B的人数
    ADD	R4,	R4,	#-1
    BRnzp	BLOOP
    
OUTPUT  
    STI	R6,	AAD
    STI R7, BAD
    TRAP	x25

NUM     .FILL	x0010
AD      .FILL	x4000
WD      .FILL	x5000
SCOREA  .FILL	#85
SCOREB  .FILL   #75
AAD     .FILL	x5100
BAD     .FILL	x5101

        .END