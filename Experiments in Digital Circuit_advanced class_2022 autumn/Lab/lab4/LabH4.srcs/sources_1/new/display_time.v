`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/31 22:23:25
// Design Name: 
// Module Name: display_time
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


module display_time(
    input [15:0] d,
    input clk,rstn,
    output reg [3:0] an,
    output [6:0] cn
    );

    wire clk_div;
    reg [1:0] cnt;
    reg [3:0] data;
    
    frequency_divider frequency_divider_dut(
        .clk(clk),
        .rstn(rstn),
        .y(clk_div)
    );

  always @(posedge clk_div or negedge rstn) begin
    if(!rstn)
        cnt <= 2'b00;
    else if(cnt < 2'b11)
        cnt <= cnt + 1'b1;
    else 
        cnt <= 2'b00;
  end

  
  always @(*) begin
    case(cnt)
        2'b00: an = 4'b1110; 
        2'b01: an = 4'b1101; 
        2'b10: an = 4'b1011; 
        2'b11: an = 4'b0111;
    endcase
  end

  always @(*) begin
    case(cnt)
        2'b00: data = d[3:0];
        2'b01: data = d[7:4];
        2'b10: data = d[11:8];
        2'b11: data = d[15:12];
        default: data = 4'b0000;
    endcase
  end

    seven_disp_decoder seven_disp_decoder_dut(
        .d(data),
        .yn(cn)
    );

endmodule
