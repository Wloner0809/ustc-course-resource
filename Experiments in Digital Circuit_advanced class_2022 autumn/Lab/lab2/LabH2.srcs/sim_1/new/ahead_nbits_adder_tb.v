`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/17 12:18:11
// Design Name: 
// Module Name: ahead_nbits_adder_tb
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


module ahead_nbits_adder_tb();
    wire co;
    wire [7:0] s;
    reg [7:0] a;
    reg [7:0] b;
    reg ci;
    initial begin
        /* change switch for 8 times */
        a = 8'b1111_0001;
        b = 8'b1101_1111;
        ci=1;
        repeat(8) #1 a = a << 1;
        a =  8'b1111_1101;
        ci = 0;
        repeat(8) #4 b = b >> 1;
        /* add switch for 8 times */
    end
    ahead_nbits_adder ahead_nbits_adder_test(
        .a(a),
        .b(b),
        .ci(ci),
        .s(s),
        .co(co)
    );
endmodule
