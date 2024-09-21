`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/06/05 13:20:23
// Design Name: 
// Module Name: Dcache_wrapper
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module Dcache_wrapper(
    input clk,
    input rstn,
    input [31:0] addr,  //这里注意地址是32位的，其实也就是alu的输出结果
    input [31:0] din,
    input we_write, we_read,
    input [11:0] sdu_addr,
    output [31:0] dout,
    output cache_miss,
    output [31:0] sdu_data,
    //下面是IO相关
    output [7:0] io_addr,
    output [31:0] io_dout,
    output io_we,
    output io_rd,
    input [31:0] io_din,
    //下面是cache命中率的统计
    output [31:0] cache_hit_cnt,
    output [31:0] cache_miss_cnt
    );

    //判断是否为外设
    wire mmio;
    assign mmio = (addr[31:8] == 24'h00007f) ? 1 : 0;
    wire true_we_write;
    assign true_we_write = mmio ? 0 : we_write;
    wire true_we_read;
    assign true_we_read = mmio ? 0 : we_read;

    wire [31:0] memout;
    //更改这里来换不同的cache实现
    Dcache_two_way DCache_dut(
        .clk(clk),
        .rstn(rstn),
        .addr(addr[11:0]),
        .din(din),
        .we_write(true_we_write),
        .we_read(true_we_read),
        .dout(memout),
        .cache_miss(cache_miss),
        .sdu_addr(sdu_addr),
        .sdu_data(sdu_data),
        .cache_hit_cnt(cache_hit_cnt),
        .cache_miss_cnt(cache_miss_cnt)
    );
    assign dout = mmio ? io_din : memout;
    assign io_addr = addr[7:0];
    assign io_dout = din;
    assign io_we = we_write & mmio;
    assign io_rd = we_read & mmio;

    




endmodule
