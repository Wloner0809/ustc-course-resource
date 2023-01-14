`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/23 18:40:31
// Design Name: 
// Module Name: three_FSM_detect1101_tb
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


module three_FSM_detect1101_tb();
    reg x,rstn,clk;
    wire [4:0] sr;
    wire yr;
    three_FSM_detect1101 three_FSM_detect1101_test(
        .x(x),
        .rstn(rstn),
        .clk(clk),
        .sr(sr),
        .yr(yr)
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
