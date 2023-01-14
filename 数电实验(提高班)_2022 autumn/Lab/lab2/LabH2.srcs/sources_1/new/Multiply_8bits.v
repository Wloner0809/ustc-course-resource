`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/15 18:48:36
// Design Name: 
// Module Name: Multiply_8bits
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


module Multiply_8bits (y,a,b);
    //shift and add multiply
    parameter WIDTH = 8;
    output reg[2*WIDTH-1:0] y;
    input [WIDTH-1:0] a;
    input [WIDTH-1:0] b;

    wire [7:0] temp[7:0],bit[7:0];
    wire co[7:0];
    genvar i;
    generate
        for(i=0;i<WIDTH;i=i+1)begin:block_1
            assign temp[i] = b[i]?a:8'b0000_0000;
        end
    endgenerate
    assign bit[0] = temp[0];
    assign co[0] = 1'b0;
    generate
        for(i=0;i<WIDTH-1;i=i+1)begin:block_2
            ahead_nbits_adder#(.WIDTH(WIDTH)) ahead_nbits_adder_dut(
                .a({co[i],bit[i][7:1]}),
                .b(temp[i+1]),
                .ci(1'b0),
                .s(bit[i+1]),
                .co(co[i+1])
            );
        end
    endgenerate
  always @(*) begin
    y[0] = bit[0][0];
    y[1] = bit[1][0];
    y[2] = bit[2][0];
    y[3] = bit[3][0];
    y[4] = bit[4][0];
    y[5] = bit[5][0];
    y[6] = bit[6][0];
    y[14:7] = bit[7];
    y[15] = co[7];
  end
endmodule
