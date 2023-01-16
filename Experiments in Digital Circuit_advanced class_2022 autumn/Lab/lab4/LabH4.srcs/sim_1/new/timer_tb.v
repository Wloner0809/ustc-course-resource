`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/31 21:54:08
// Design Name: 
// Module Name: timer_tb
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


module timer_tb();
    reg clk,rstn,st;
    reg [15:0] tc;
    wire td;
    wire [6:0] cn;
    wire [3:0] an;

    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        tc = 16'h0012;
        st = 1'b0;
        #10 rstn = 1'b1;

        #10 st = 1'b1;
        #100000000 st = 1'b0;
    end

    always #5 clk = ~clk;

    timer timer_test(
        .clk(clk),
        .rstn(rstn),
        .st(st),
        .td(td),
        .tc(tc),
        .cn(cn),
        .an(an)
    );
endmodule
