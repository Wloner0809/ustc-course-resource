`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/30 19:13:49
// Design Name: 
// Module Name: syn_ps_tb
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


module syn_ps_tb();
    wire p;
    reg clk,rstn,a;
    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        a = 1'b0;
        #10 rstn = 1'b1;
        #5 a = 1'b1;
    end
    always #10 clk = ~clk;
    always #60 a = ~a;
               
    syn_ps syn_ps_test(
        .clk(clk),
        .rstn(rstn),
        .a(a),
        .p(p)
    );
endmodule
