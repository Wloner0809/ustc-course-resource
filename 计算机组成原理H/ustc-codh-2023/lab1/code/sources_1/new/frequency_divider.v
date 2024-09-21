`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 18:54:37
// Design Name: 
// Module Name: frequency_divider
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


module frequency_divider #(
    parameter k = 100000
)(
    input clk,rstn,
    output reg y
    );

    reg [31:0] count;
    reg [31:0] pre_odd_cnt;
    reg [31:0] now_odd_cnt;    
  always @(posedge clk or negedge rstn) begin
    if(!rstn)begin
        count <= k>>1 - 1;
        pre_odd_cnt <= (k>>1) - 1;
        now_odd_cnt <= k[0] ? k>>1 : (k>>1)-1;
    end
    else if(count == 0)begin
        count <= (k[0] ? pre_odd_cnt : (k>>1)-1);
        pre_odd_cnt <= now_odd_cnt;
        now_odd_cnt <= pre_odd_cnt;
    end
    else
        count <= count - 1;
  end
  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        y <= 0;
    else if(count == 0)
        y <= ~y;
    else    
        y <= y;
  end

endmodule
