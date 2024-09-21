`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 20:15:26
// Design Name: 
// Module Name: Display
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


module Display(
    input [31:0] d,
    input clk,rstn,
    output  [7:0] an,
    output  [6:0] cn
    );
    wire clk_div;
    reg [2:0] cnt;
    wire [3:0] data;
    
    frequency_divider frequency_divider_dut(
        .clk(clk),
        .rstn(rstn),
        .y(clk_div)
    );
    //clk_div是分频后的时钟信号
  always @(posedge clk_div or negedge rstn) begin
    //对cnt循环计数达到动态显示的效果
    if(!rstn)
        cnt <= 3'b000;
    else if(cnt < 3'b111)
        cnt <= cnt + 1'b1;
    else 
        cnt <= 3'b000;
  end

  
    decoder3_8 decoder3_8_dut(
        .d(cnt),
        .y(an)
    );

    mux8_1 mux8_1_dut(
        .s(cnt),
        .d(d),
        .y(data)
    );

    seven_disp_decoder seven_disp_decoder_dut(
        .d(data),
        .yn(cn)
    );
endmodule
