`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/16 21:27:47
// Design Name: 
// Module Name: Multiply_test
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


module Multiply_test(
    input [7:0] a,b,
    input rstn,clk,en,
    output [15:0] result
    );
    wire [7:0] c,d;
    wire [15:0] e;
    register#(.WIDTH(8)) register_dut1(
        .d(a),
        .q(c),
        .en(en),
        .rstn(rstn),
        .clk(clk)
    );
    register#(.WIDTH(8)) register_dut2(
        .d(b),
        .q(d),
        .en(en),
        .rstn(rstn),
        .clk(clk)
    );
    Multiply_8bits Multiply_8bits_dut(
        .a(c),
        .b(d),
        .y(e)
    );
    register#(.WIDTH(16)) register_dut3(
        .d(e),
        .q(result),
        .en(en),
        .rstn(rstn),
        .clk(clk)
    );
endmodule
