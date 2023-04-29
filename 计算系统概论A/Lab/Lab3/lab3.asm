    .ORIG	x3000
    LDI	R0,	NUM     ;R0存放的是N
    ADD R0, R0, #1
    LD	R1,	DATA    ;R1相当于字符串的指针
    LDI	R2,	DATA    ;R2存放的是读取的字符
    LDI	R3,	DATA    ;R3存放的是待检测的字符

LOOP1   ADD	R0,	R0,	#-1 ;循环变量的更新
        BRn	OUTPUT
        NOT	R6,	R3
        ADD	R6,	R6,	#1  ;R6存放R3的取反加1，便于后续减法
        ADD	R6,	R2,	R6  ;R6存放R2-R3的结果
        BRz	LOOP2
        NOT	R7,	R5      
        ADD	R7,	R7,	#1  ;R7存放R5的取反加1，便于后续减法
        ADD	R7,	R4,	R7  ;R7存放R4-R5
        BRn	LOOP3
LOOP4   AND R5, R5, #0
        ADD R5, R5, #1  ;此时R5应该存1，因为最小重复的子串长度为1
        LDR R2, R1, #0
        ADD	R1,	R1,	#1
        LDR	R3,	R1,	#0
        BRnzp LOOP1

LOOP2   ADD	R5,	R5,	#1  ;R5存放中间结果，字符相等就加1
        ADD	R1,	R1,	#1  ;R1指针加1
        LDR	R3,	R1,	#0
        BRnzp	LOOP1

LOOP3   AND	R4,	R5,	R5
        BRnzp LOOP4
        
OUTPUT  STI	R4,	RESULT
        TRAP	x25

NUM     .FILL	x3100
RESULT  .FILL	x3050
DATA    .FILL	x3101

    .END