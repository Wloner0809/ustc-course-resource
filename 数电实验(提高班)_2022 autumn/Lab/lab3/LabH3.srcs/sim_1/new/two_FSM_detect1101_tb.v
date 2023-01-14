`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/23 18:10:58
// Design Name: 
// Module Name: two_FSM_detect1101_tb
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


module two_FSM_detect1101_tb();
    reg x,rstn,clk;
    wire [1:0] sl;
    wire yl;
    two_FSM_detect1101 two_FSM_detect1101_test(
        .x(x),
        .rstn(rstn),
        .clk(clk),
        .sl(sl),
        .yl(yl)
    );
    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        x = 1'b0;
        # 100 rstn = 1'b1;
    end
    always #20 clk = ~clk;
    always #100 x = {$random} % 2;
endmodule
