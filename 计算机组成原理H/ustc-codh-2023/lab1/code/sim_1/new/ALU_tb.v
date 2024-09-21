`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 08:09:13
// Design Name: 
// Module Name: ALU_tb
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


module ALU_tb();

    reg [3:0] a,b;
    reg [2:0] f;
    wire [3:0] y;
    wire [2:0] t;
    initial begin
        a = 4'b1011;
        b = 4'b1100;
        f = 3'b000;
        #50 f = 3'b001;
        #50 f = 3'b010;
        #50 f = 3'b011;
        #50 f = 3'b100;
        #50 f = 3'b101;
        #50 f = 3'b110;
        #50 f = 3'b111;
    end
    ALU #(4) ALU_dut(
        .a(a),
        .b(b),
        .f(f),
        .y(y),
        .t(t)
    );

endmodule
