.text

j	main

sort:
    #a0存储数组的起始地址，a1存放数组的大小
    mv  t0, a0      #t0存放数组的起始地址
    addi t0, t0, 4  #因为第一个存放的是数组大小，之后的才是数据
    add a1, a1, a1
    add a1, a1, a1  #a1 = a1 * 4
    add t1, a0, a1  #t1存放最后元素的地址
    addi t1, t1, 4
    mv  t2, t0      #t2相当于外层循环中的i

    outloop:
        beq t2, t1, outloop_end
        addi t3, t2, 4  #t3相当于内层循环的j

    inloop:
        beq t3, t1, inloop_end
        lw  t4, 0(t2)   #t4存放的是待排序的数据 
        lw  t5, 0(t3)   #t5存放的是待排序的数据
        bleu t4, t5, next_inloop    #数组按照升序排列
        mv  t6, t4      #交换数据
        mv  t4, t5
        mv  t5, t6
        sw  t4, 0(t2)   #将数据写入内存
        sw  t5, 0(t3)

    next_inloop:
        addi t3, t3, 4  #更新内层循环变量
        j   inloop

    inloop_end:
        addi t2, t2, 4  #更新外层循环变量
        j   outloop
    outloop_end:
        ret

main:
    lw  a0, 0x00002000
    lw  a1, 0(a0)
    jal ra, sort
    
