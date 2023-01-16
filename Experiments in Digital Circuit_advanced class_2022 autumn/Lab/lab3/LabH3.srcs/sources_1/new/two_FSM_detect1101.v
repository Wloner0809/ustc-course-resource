`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/23 15:40:28
// Design Name: 
// Module Name: two_FSM_detect1101
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


//两段式
module two_FSM_detect1101(
    input x,
    input rstn,
    input clk,
    output reg yl,
    output reg [1:0] sl
    );
    //顺序码
    parameter s0 = 2'b00,
              s1 = 2'b01,
              s2 = 2'b10,
              s3 = 2'b11;
    //存放状态的两个变量
    reg [1:0] NS,CS;
  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        CS <= s0;
    else
        CS <= NS;
  end
  always @(*) begin
    yl = 0;
    sl = 2'b00;
    NS = s0;
    case(CS)
    s0:begin
        sl = 2'b00;
        yl = 0;
        NS = x ? s1 : s0; 
    end
    s1:begin
        sl = 2'b01;
        yl = 0;
        NS = x ? s2 : s0;
    end
    s2:begin
        sl = 2'b10;
        yl = 0;
        NS = x ? s2 : s3;
    end
    s3:begin
        sl = 2'b11;
        yl = x ? 1 : 0;
        NS = x ? s1 : s0; 
    end
    default:begin
        yl = 0;
        sl = 2'b00;
        NS = s0;
    end
    endcase
  end
endmodule
