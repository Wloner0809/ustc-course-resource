`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/18 22:04:58
// Design Name: 
// Module Name: adder_8bits_mix
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


module adder_8bits_mix(
    input [7:0] a,b,
    input ci,
    output [7:0] s,
    output co
    );
    wire c;
    ahead_nbits_adder#(.WIDTH(4)) ahead_nbits_adder_dut1(
        .a(a[3:0]),
        .b(b[3:0]),
        .ci(ci),
        .s(s[3:0]),
        .co(c)
    );
    ahead_nbits_adder#(.WIDTH(4)) ahead_nbits_adder_dut2(
        .a(a[7:4]),
        .b(b[7:4]),
        .ci(c),
        .s(s[7:4]),
        .co(co)
    );
endmodule
