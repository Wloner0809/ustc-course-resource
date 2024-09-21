`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 18:56:42
// Design Name: 
// Module Name: seven_disp_decoder
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


module seven_disp_decoder(
    input [3:0] d,      
    output reg [6:0] yn
    );
    always @(*) begin
    case(d)
        4'd0: yn = 7'b000_0001;
        4'd1: yn = 7'b100_1111;
        4'd2: yn = 7'b001_0010;
        4'd3: yn = 7'b000_0110;
        4'd4: yn = 7'b100_1100;
        4'd5: yn = 7'b010_0100;
        4'd6: yn = 7'b010_0000;
        4'd7: yn = 7'b000_1111;
        4'd8: yn = 7'b000_0000;
        4'd9: yn = 7'b000_0100;
        4'd10: yn = 7'b000_1000;
        4'd11: yn = 7'b110_0000;
        4'd12: yn = 7'b011_0001;
        4'd13: yn = 7'b100_0010;
        4'd14: yn = 7'b011_0000;
        4'd15: yn = 7'b011_1000;
        default: yn = 7'b111_1111;
    endcase
  end
endmodule
