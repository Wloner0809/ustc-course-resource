`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/31 23:41:20
// Design Name: 
// Module Name: coder_lab4_tb
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


module coder_lab4_tb();

    reg clk,rstn,x,sel;
    wire [7:0] an;
    wire [6:0] cn;
    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        x = 1'b1;
        sel = 1'b1;
        #5 rstn = 1'b1;
        #10000000 x = 1'b0;
        #5 x = 1'b1;
        #20000000 x = 1'b0;
        #1 x = 1'b1;
        #2 x = 1'b0;
        #2 x = 1'b1;
    end

    always #5 clk = ~clk;


    coder_lab4_1 coder_lab4_1_test(
        .clk(clk),
        .rstn(rstn),
        .x(x),
        .sel(sel),
        .an(an),
        .cn(cn)
    );
endmodule
