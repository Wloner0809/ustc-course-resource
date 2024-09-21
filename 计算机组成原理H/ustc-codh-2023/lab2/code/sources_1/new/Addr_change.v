`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/08 08:56:09
// Design Name: 
// Module Name: Addr_change
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


module Addr_change(
    input clk,
    input [2:0] sel,
    output reg [7:0]addr1, addr2
    );
    always @(posedge clk) begin
        case(sel)
            3'b000: begin
                addr1 <= 8'h01;
                addr2 <= 8'h02;
            end 
            3'b001: begin
                addr1 <= addr1;
                addr2 <= addr2;
            end
            3'b010: begin
                addr1 <= addr1 + 1;
                addr2 <= addr2 + 1;
            end
            3'b011: begin
                addr1 <= addr2;
                addr2 <= addr1;
            end
            3'b100: begin
                addr1 <= 8'h00;
                addr2 <= 8'h00;
            end
        endcase
    end
endmodule
