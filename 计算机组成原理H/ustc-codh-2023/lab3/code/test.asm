.data

data1: .word 0x00000023
data2: .word 0x00000210
data3: .word 0x00000233
data4: .word 0xffff00ff
data6: .word 0x00002100
data7: .word 0xfffff00f
data8: .word 0x00023000
data9: .word 0x00001184
data5: .word 0x00002100


.text

    beq x0, x0, next1           #测试beq
    addi t6, t6, -1

next1:
    addi t6, t6, 1
    lw  t1, 0x00002030          #测试lw，让0x00002030中的值为0
    beq t1, x0, next2
    addi t6, t6, -1

next2:
    addi t6, t6, 1
    lw  t1, data1               #测试add
    lw  t2, data2
    lw  t3, data3
    add t2, t2, t1
    beq t2, t3, next3
    addi t6, t6, -1

next3:
    lw  t1, data2               #测试addi
    addi t1, t1, 0x23
    beq t1, t3, next4
    add t6, t6, t6

next4:
    addi t6, t6, 1
    sub t1, t1, t3              #测试sub
    beq t1, x0, next5
    addi t6, t6, -1

next5:
    addi t6, t6, 1
    lw  t1, data4               #测试blt
    lw  t2, data1
    blt t1, t2, next6
    addi t6, t6, -1

next6:
    addi t6, t6, 1
    lw  t1, data1               #测试bltu
    lw  t2, data4
    bltu t1, t2, next7
    addi t6, t6, -1

next7:
    addi t6, t6, 1
    lw  t1, data1               #测试and
    lw  t2, data2
    and t1, t1, t2
    beq t1, x0, next8
    addi t6, t6, -1

next8:
    addi t6, t6, 1
    lw  t1, data2               #测试or
    lw  t2, data3
    or  t1, t1, t2
    beq t1, t2, next9
    addi t6, t6, -1

next9:
    addi t6, t6, 1
    lw  t1, data1               #测试xor
    lw  t2, data2
    lw  t3, data3
    xor t2, t2, t3
    beq t2, t1, next10
    addi t6, t6, -1

next10:
    addi t6, t6, 1
    lw  t1, data2               #测试slli
    lw  t2, data6
    slli t1, t1, 4
    beq t1, t2, next11
    addi t6, t6, -1

next11:
    addi t6, t6, 1
    lw  t1, data3               #测试srli
    lw  t2, data1
    srli t1, t1, 4
    beq t1, t2, next12
    addi t6, t6, -1

next12:
    addi t6, t6, 1
    lw  t1, data4               #测试srai
    lw  t2, data7
    srai t1, t1, 4
    beq t1, t2, next13
    addi t6, t6, -1

next13:
    addi t6, t6, 1
    lw  t1, data8               #测试lui
    lui t2, 0x00023
    beq t1, t2, next14
    addi t6, t6, -1

next14:
    addi t6, t6, 1
    auipc t1, 0x00001           #测试auipc
    lw  t2, data9
    beq t1, t2, next15
    addi t6, t6, -1

next15:
    addi t6, t6, 1
    lw  t1, 0x00002020           #测试sw
    lw  t2, data3
    sw  t2, 0(t1)
    lw  t3, 0(t1)
    beq t2, t3, next16
    addi t6, t6, -1

next16:
    addi t6, t6, 1
    addi ra, x0, 0              #测试jal
    jal ra, next17
    addi t6, t6, -1

next17:
    addi t6, t6, 1
    addi  t1, ra, 0x14          #测试jalr
    jalr ra, 0(t1)
    addi t6, t6, -1
    addi t6, t6, 2

