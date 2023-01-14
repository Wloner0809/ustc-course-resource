`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/17 08:03:50
// Design Name: 
// Module Name: Multiplt_8bits_tb
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


module Multiplt_8bits_tb();
    wire [15:0] y;
    reg [7:0] a;
    reg [7:0] b;
    initial begin
        /* change switch for 8 times */
        a = 8'b1111_1111;
        b = 8'b1111_1111;
        repeat(8) #1 a = a << 1; 
        /* add switch for 8 times */
        a = 8'b1111_1111;
        repeat(8) #3 b = b << 1;
    end
    Multiply_8bits  Multiply_8bits_test(
        .a(a),
        .b(b),
        .y(y)
    );
endmodule
