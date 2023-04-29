; Unfortunately we have not YET installed Windows or Linux on the LC-3,
; so we are going to have to write some operating system code to enable
; keyboard interrupts. The OS code does three things:
;
;    (1) Initializes the interrupt vector table with the starting
;        address of the interrupt service routine. The keyboard
;        interrupt vector is x80 and the interrupt vector table begins
;        at memory location x0100. The keyboard interrupt service routine
;        begins at x1000. Therefore, we must initialize memory location
;        x0180 with the value x1000.
;    (2) Sets bit 14 of the KBSR to enable interrupts.
;    (3) Pushes a PSR and PC to the system stack so that it can jump
;        to the user program at x3000 using an RTI instruction.

        .ORIG x800
        ; (1) Initialize interrupt vector table.
        LD R0, VEC
        LD R1, ISR
        STR R1, R0, #0

        ; (2) Set bit 14 of KBSR.
        LDI R0, KBSR
        LD R1, MASK
        NOT R1, R1
        AND R0, R0, R1
        NOT R1, R1
        ADD R0, R0, R1
        STI R0, KBSR

        ; (3) Set up system stack to enter user space.
        LD R0, PSR
        ADD R6, R6, #-1
        STR R0, R6, #0
        LD R0, PC
        ADD R6, R6, #-1
        STR R0, R6, #0
        ; Enter user space.
        RTI
        
VEC     .FILL x0180
ISR     .FILL x1000
KBSR    .FILL xFE00
MASK    .FILL x4000
PSR     .FILL x8002
PC      .FILL x3000
        .END

        .ORIG x3000
        ; *** Begin user program code here ***
        LD	R6, INIT
        ST	R0,	SaveR0
        ST	R2,	SaveR2
        AND	R2,	R2,	#0

AGAIN   LEA	R0,	ID
        TRAP	x22
        JSR	DELAY
        LDI R2, NADDRESS
        BRz	AGAIN
        ADD	R2,	R2,	#-12
        ADD	R2,	R2,	#-12
        ADD	R2,	R2,	#-12
        ADD	R2,	R2,	#-12    ;ASCII码向数字转换
        JSR	HANOI           ;调用Hanoi子程序
        LEA	R0,	RESULT
        
        AND	R4,	R3,	#8
        BRz	SD              ;结果是个位数的情况
        LD	R4,	VALUE1
        AND	R4,	R3,	R4      ;判断有两位还是有三位
        BRz	DD              ;结果是两位数的情况
        AND	R4,	R4,	#0
        AND	R5,	R5,	#0
        ADD R5,	R5,	#-1
        LD	R4,	VALUE2
LOOP2   ADD	R5,	R5,	#1
        ADD	R3,	R3,	R4
        BRp	LOOP2
        ADD	R5,	R5,	#12
        ADD	R5,	R5,	#12
        ADD	R5,	R5,	#12
        ADD	R5,	R5,	#12
        STR	R5,	R0,	#22     ;百位写入
        LD	R4,	VALUE3
        ADD	R3,	R3,	R4
        BRnzp	DD
        
SD      ADD	R3,	R3,	#12
        ADD	R3,	R3,	#12
        ADD	R3,	R3,	#12
        ADD	R3,	R3,	#12
        STR	R3,	R0,	#23
        BRnzp	OUTPUTRESULT


DD      AND	R4,	R4,	#0
        ADD	R4,	R4,	#-1

LOOP1   ADD	R4,	R4,	#1
        ADD	R3,	R3,	#-10
        BRp	LOOP1
        ADD	R4,	R4,	#12
        ADD	R4,	R4,	#12
        ADD	R4,	R4,	#12
        ADD	R4,	R4,	#12
        STR	R4,	R0,	#23
        ADD	R3,	R3,	#10
        ADD	R3,	R3,	#12
        ADD	R3,	R3,	#12
        ADD	R3,	R3,	#12
        ADD	R3,	R3,	#12
        STR	R3,	R0,	#24
        BRnzp	OUTPUTRESULT
        



OUTPUTRESULT    LEA	R0,	RESULT
                TRAP	x22
                LD	R0, SaveR0
                LD	R2,	SaveR2
                TRAP	x25


HANOI   ADD	R6,	R6,	#-1
        STR	R7,	R6,	#0      ;Push R7
        ADD	R6,	R6,	#-1
        STR	R2,	R6,	#0      ;Push R2, the value of n

;Check for base case
        ADD	R2,	R2,	#0
        BRp	SKIP
        BRnzp	DONE

;Not a base, do the recursion
SKIP    ADD	R2,	R2,	#-1
        ADD	R3,	R3,	R3
        ADD	R3,	R3,	#1
        JSR HANOI

;Restore registers and return
DONE    LDR	R2,	R6,	#0
        ADD	R6,	R6,	#1
        LDR	R7,	R6,	#0
        ADD	R6,	R6,	#1
        RET

DELAY   ST	R1,	SaveR1
        LD	R1,	COUNT
REP     ADD	R1,	R1,	#-1
        BRp	REP
        LD	R1, SaveR1
        RET

SaveR0  .BLKW	1
SaveR1  .BLKW	1
SaveR2  .BLKW	1
NADDRESS    .FILL	x3FFF
COUNT   .FILL	#2500       ;防止输出太快，这里选择2500(D)作为计数标准
INIT    .FILL	xFDFF
VALUE1  .FILL	#64
VALUE2  .FILL	#-100
VALUE3  .FILL	#100
ID      .STRINGZ	"PB21030814 "
RESULT  .STRINGZ	"Tower of hanoi needs       moves.\n"
        ; *** End user program code here ***
        .END


        .ORIG x1000
        ; *** Begin interrupt service routine code here ***
        ST	R0,	SR0
        ST	R1,	SR1
        TRAP	x20
        ADD	R1,	R0,	#0      ;将R0中的值放到R1当中
        LD	R0,	ZERO
        ADD	R0,	R0,	R1
        BRn	NDN             ;小于0的ASCII码，说明不是数字
        LD	R0, NINE
        ADD	R0,	R0,	R1  
        BRp	NDN             ;大于9的ASCII码，说明不是数字
        STI	R1,	NA          ;输入的是数字，保存到X3FFF当中       
        LEA	R0,	NUMBER
        STR	R1,	R0,	#1      ;写入读进来的那个字符
        LEA	R0,	NUMBER
        BRnzp	OUTPUT

NDN     LEA	R0,	NOTNUMBER
        STR	R1,	R0,	#1      ;写入读进来的那个字符
        LEA	R0,	NOTNUMBER

OUTPUT  TRAP	x22

        LD	R0,	SR0
        LD	R1, SR1
        RTI

        ; *** End interrupt service routine code here ***
SR0     .BLKW	1
SR1     .BLKW	1
NA      .FILL	x3FFF
ZERO    .FILL	xFFD0       ;-48，48代表0的ASCII码
NINE    .FILL	xFFC7       ;-57，57代表9的ASCII码
NUMBER  .STRINGZ	"\n  is a decimal digit.\n"
NOTNUMBER   .STRINGZ	"\n  is not a decimal digit.\n"
        .END