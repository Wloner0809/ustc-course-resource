        .ORIG	x3000
        LDI	R0, RA1
        LDI R1, RA2
        LDI R2, RA3     ;分别将p、q、N存放在R0、R1、R2寄存器中
        ADD	R2,	R2,	#-1 ;便于后面循环
        ADD	R0,	R0,	#-1 ;将p-1存放到R0中用于后续取模运算
        NOT	R1,	R1      
        ADD R1, R1, #1  ;R1中存放的是q的非+1，用于后续取模时做减法
        ADD R3, R3, #1  ;R3存放的是F(N-2),初始值为1
        ADD	R4,	R4,	#1  ;R4存放的是F(N-1),初始值为1

CYCLE   
        AND	R5,	R3,	R3
        AND	R6,	R4,	R4  ;R5、R6用于存放取模后的值
        AND	R5,	R5,	R0  ;F(N-2)取模运算
        AND	R7,	R6,	R6  ;用R7存放取模中间结果
MODE    AND	R6,	R7,	R7
        ADD	R7,	R7,	R1  ;F(N-1)取模运算
        BRzp	MODE
        AND	R3,	R4,	R4  ;更新F(N-2)
        ADD	R4,	R5,	R6  ;求得F(N),更新F(N-1)
        ADD	R2,	R2,	#-1 ;
        BRp	    CYCLE

        STI	R4,	WA      ;写入地址x3103中
        TRAP	x25

RA1     .FILL	x3100    
RA2     .FILL	x3101 
RA3     .FILL	x3102 
WA      .FILL	x3103
        .END