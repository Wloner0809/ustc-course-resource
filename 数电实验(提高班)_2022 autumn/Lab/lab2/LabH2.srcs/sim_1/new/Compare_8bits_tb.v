`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/18 07:27:44
// Design Name: 
// Module Name: Compare_8bits_tb
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


module Compare_8bits_tb();
        wire ug,ul,sg,sl;
        reg [7:0] a,b;
        initial begin
            /* change switch for 8 times */
            a = 8'b1111_1111;
            b = 8'b1111_1111;
            repeat(8) #1 a = a << 1; 
            /* add switch for 8 times */
            a = 8'b1111_1111;
            repeat(8) #3 b = b << 1;
        end
        Comparer_8bits Comparer_8bits_test(
            .a(a),
            .b(b),
            .ug(ug),
            .ul(ul),
            .sg(sg),
            .sl(sl)
        );
endmodule
