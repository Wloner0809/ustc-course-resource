`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 18:55:17
// Design Name: 
// Module Name: decoder3_8
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


module decoder3_8(
    input [2:0] d,
    output reg [7:0] y 
    );
    always @(*) begin
    case(d)
        //这里是低电平有效(an)
        3'b000: y = 8'b1111_1110; 
        3'b001: y = 8'b1111_1101; 
        3'b010: y = 8'b1111_1011; 
        3'b011: y = 8'b1111_0111; 
        3'b100: y = 8'b1110_1111; 
        3'b101: y = 8'b1101_1111; 
        3'b110: y = 8'b1011_1111; 
        3'b111: y = 8'b0111_1111; 
    endcase
  end
endmodule
