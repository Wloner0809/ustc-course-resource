`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/30 10:30:17
// Design Name: 
// Module Name: frequency_divider_tb
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


module frequency_divider_tb();
    reg clk,rstn;
    wire y;

    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        #10 rstn = 1'b1;
    end
    always #10 clk = ~clk;
    frequency_divider #(.k(100000)) frequency_divider_test(
        .clk(clk),
        .rstn(rstn),
        .y(y)
    );
endmodule
