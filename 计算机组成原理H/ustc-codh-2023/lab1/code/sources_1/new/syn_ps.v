`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/03/31 19:12:18
// Design Name: 
// Module Name: syn_ps
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


module syn_ps(
    input a,clk,rstn,
    output  p
    );
    reg q,s,m;
    //信号同步和取边沿
    always @(posedge clk or negedge rstn) begin
    if(!rstn)
        q <= 1'b0;
    else    
        q <= a;
  end

  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        s <= 1'b0;
    else
        s <= q;
  end

  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        m <= 1'b0;
    else
        m <= s;
  end
  
  assign p = s & (~m);
endmodule
