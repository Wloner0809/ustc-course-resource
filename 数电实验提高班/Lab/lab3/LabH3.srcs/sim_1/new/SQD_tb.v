`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/23 18:54:57
// Design Name: 
// Module Name: SQD_tb
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


module SQD_tb();
    reg x,rstn,clk;
    wire [4:0] sr;
    wire yr;
    wire [1:0] sl;
    wire yl;
    wire [7:0] rx;
    SQD SQD_test(
        .x(x),
        .rstn(rstn),
        .clk(clk),
        .sr(sr),
        .yr(yr),
        .sl(sl),
        .yl(yl),
        .rx(rx)
    );
    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        x = 1'b0;
        # 100 rstn = 1'b1;
    end
    always #20 clk = ~clk;
    always #40 x = {$random} % 2;
endmodule
