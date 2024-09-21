`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/03/31 18:57:02
// Design Name: 
// Module Name: Debounce
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


module Debounce(
    input clk,rstn,x,
    output reg y
    );
    reg [19:0] count;   //用于计数
    reg [1:0] x_pre_now;    //用于检验什么时候开始计数

  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        x_pre_now <= 2'b00;
    else
        x_pre_now <= {x_pre_now[0],x};
  end
  
  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        count <= 20'h0;
    else if(x_pre_now[1]^x_pre_now[0])  //还在抖动的情况
        count <= 20'h0;
    else if(count == 20'hf4240)         //达到稳定后count保持不变
        count <= count;
    else 
        count <= count + 1'h1;
  end

  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        y <= 1'b0;
    else if(count == 20'hf4240 && x_pre_now[1] == 1'b1) //按键被按下
        y <= x;
    else
        y <= 1'b0;
  end
endmodule
