`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/23 16:41:10
// Design Name: 
// Module Name: SQD
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


module SQD(
    input x,
    input rstn,
    input clk,
    output  yl,
    output  [1:0] sl,
    output  yr,
    output  [4:0] sr,
    output  reg [7:0] rx
    );
    two_FSM_detect1101 two_FSM_detect1101_dut(
        .x(x),
        .rstn(rstn),
        .clk(clk),
        .yl(yl),
        .sl(sl)
    );
    three_FSM_detect1101 three_FSM_detect1101_dut(
        .x(x),
        .rstn(rstn),
        .clk(clk),
        .yr(yr),
        .sr(sr)
    );
  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        rx <= 8'b0000_0000;
    else begin
        rx <= rx << 1;
        rx[0] <= x;
    end
  end
endmodule
