`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/06/03 14:06:47
// Design Name: 
// Module Name: Dcache_two_way_tb
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


module Dcache_two_way_tb();

    reg clk, rstn;
    reg [11:0] addr;
    reg [31:0] din;
    reg we_write, we_read;
    wire [31:0] dout;
    wire cache_miss;
    reg [11:0] sdu_addr;
    wire [31:0] sdu_data;

    initial begin
        clk = 0;
        rstn = 0;
        addr = 0;
        din = 23;
        we_read = 0;
        we_write = 1;
        sdu_addr = 0;
        #10 rstn = 1;
        #500 addr = 32;
    end

    always #5 clk = ~clk;

    Dcache_two_way Dcache_two_way_dut(
        .clk(clk),
        .rstn(rstn),
        .addr(addr),
        .din(din),
        .we_write(we_write),
        .we_read(we_read),
        .dout(dout),
        .cache_miss(cache_miss),
        .sdu_addr(sdu_addr),
        .sdu_data(sdu_data)
    );


endmodule
