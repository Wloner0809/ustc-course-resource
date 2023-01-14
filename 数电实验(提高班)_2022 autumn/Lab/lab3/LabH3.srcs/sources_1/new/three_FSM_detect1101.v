`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/23 16:09:43
// Design Name: 
// Module Name: three_FSM_detect1101
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

//三段式
module three_FSM_detect1101(
    input x,
    input rstn,
    input clk,
    output reg yr,
    output reg [4:0] sr
    );
    //独热码
    parameter s0 = 5'b00001,
              s1 = 5'b00010,
              s2 = 5'b00100,
              s3 = 5'b01000,
              s4 = 5'b10000;
    //存放状态的两个变量
    reg [4:0] NS,CS;
  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        CS <= s0;
    else 
        CS <= NS;
  end
  always @(*) begin
    NS = s0;
    case(CS)
    s0: NS = x ? s1 : s0;
    s1: NS = x ? s2 : s0;
    s2: NS = x ? s2 : s3;
    s3: NS = x ? s4 : s0;
    s4: NS = x ? s2 : s0;
    default: NS = s0;
    endcase
  end
  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        {yr,sr} <= 6'b000001;
    else begin
        {yr,sr} <= 6'b000001;
        case(NS)
        s0: {yr,sr} <= 6'b000001;
        s1: {yr,sr} <= 6'b000010;
        s2: {yr,sr} <= 6'b000100;
        s3: {yr,sr} <= 6'b001000;
        s4: {yr,sr} <= 6'b110000;
        default: {yr,sr} <= 6'b000001;
        endcase
    end
  end
endmodule
