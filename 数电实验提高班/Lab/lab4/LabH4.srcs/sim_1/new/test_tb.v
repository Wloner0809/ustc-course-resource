`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/11/01 00:11:32
// Design Name: 
// Module Name: test_tb
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


module test_tb();

    reg clk,rstn,x;
    wire p;
    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        x = 1'b1;
        #5 rstn = 1'b1; 
        #15000000 x = ~x;
        #20 x = ~x;
        #15000000 x = ~x;
        #20 x = ~x;
        #10000000 x = ~x;
        #20 x = ~x;
        #15000000 x = ~x;
        #20 x = ~x;
        #15000000 x = ~x;
        #20 x = ~x;
    end
    always #5 clk = ~clk;

    test test_test(
        .clk(clk),
        .rstn(rstn),
        .x(x),
        .p(p)
    );

endmodule
