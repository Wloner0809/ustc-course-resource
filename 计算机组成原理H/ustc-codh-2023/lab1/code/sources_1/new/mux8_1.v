`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 18:57:58
// Design Name: 
// Module Name: mux8_1
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


module mux8_1(
    input [2:0] s,
    input [31:0] d,
    output reg [3:0] y
    );
    always @(*) begin
    case(s)
        3'b000: y = d[3:0];
        3'b001: y = d[7:4];
        3'b010: y = d[11:8];
        3'b011: y = d[15:12];
        3'b100: y = d[19:16];
        3'b101: y = d[23:20];
        3'b110: y = d[27:24];
        3'b111: y = d[31:28];
        default: y = 4'b0000;
    endcase
  end
endmodule
