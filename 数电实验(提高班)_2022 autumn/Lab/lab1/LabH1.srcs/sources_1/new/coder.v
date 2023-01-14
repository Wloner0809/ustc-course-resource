`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/05 12:47:22
// Design Name: 
// Module Name: coder
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


module coder(
    input e,
    input [9:0] a,
    input [3:0] b,
    output f,
    output [3:0] d,
    output [9:0] y,
    output [6:0] yn,
    output dp,
    output [7:0] an
    );
    wire f1;
    wire [3:0] y1;
    wire [3:0] y2;
    encoder10_4 encoder10_4_dut(
        .e(e),
        .a(a),
        .f(f1),
        .y(y1)
    );
    assign f=f1;
    assign d=y1;
    mux2_1 mux2_1_dut(
        .b(y1),
        .a(b),
        .s(f1),
        .y(y2)
    );
    decoder4_10 decoder4_10_dut(
        .d(y2),
        .y(y)
    );
    seven_disp_decoder seven_disp_decoder_dut(
        .d(y2),
        .yn(yn)
    );
    assign dp=1'b1;
    assign an=8'b1111_1110;
endmodule
