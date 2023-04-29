`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/15 14:37:24
// Design Name: 
// Module Name: register
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


module register #(parameter WIDTH = 8)
(
    input clk,rstn,en,
    input [WIDTH-1:0] d,
    output reg [WIDTH-1:0] q
);
  always @(posedge clk, negedge rstn) begin
    if(!rstn)   q <= 0;
    else if(en) q <= d;
  end
endmodule
