`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/04 15:19:53
// Design Name: 
// Module Name: decoder4_10
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


module decoder4_10(
    input [3:0] d,      //4位BCD码
    output reg [9:0] y      //10位译码，高电平有效
    );
  always @(*) begin
    case(d)
        4'd0: y=10'b00_0000_0001;
        4'd1: y=10'b00_0000_0010;
        4'd2: y=10'b00_0000_0100;
        4'd3: y=10'b00_0000_1000;
        4'd4: y=10'b00_0001_0000;
        4'd5: y=10'b00_0010_0000;
        4'd6: y=10'b00_0100_0000;
        4'd7: y=10'b00_1000_0000;
        4'd8: y=10'b01_0000_0000;
        4'd9: y=10'b10_0000_0000; 
        default: y=10'b00_0000_0000;
    endcase
  end
endmodule


