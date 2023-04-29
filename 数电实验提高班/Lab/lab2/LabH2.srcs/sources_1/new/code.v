`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/16 19:32:40
// Design Name: 
// Module Name: code
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


module code(
    input [7:0] a,b,
    input en,rstn,clk,
    output [15:0] y,
    output [4:0] q
    );
    wire [7:0] c,d;
    wire [15:0] e;
    wire [4:0] f;
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
    Multiply_8bits#(.WIDTH(8)) Multiply_8bits_dut(
        .a(c),
        .b(d),
        .y(e)
    );
    assign f[4] = ((c*d)==e);
    Comparer_8bits Comparer_8bits_dut(
        .a(c),
        .b(d),
        .ug(f[3]),
        .ul(f[2]),
        .sg(f[1]),
        .sl(f[0])
    );
    register#(.WIDTH(16)) register_dut3(
        .d(e),
        .q(y),
        .en(en),
        .rstn(rstn),
        .clk(clk)
    );
    register#(.WIDTH(5)) register_dut4(
        .d(f),
        .q(q),
        .en(en),
        .rstn(rstn),
        .clk(clk)
    );
endmodule
