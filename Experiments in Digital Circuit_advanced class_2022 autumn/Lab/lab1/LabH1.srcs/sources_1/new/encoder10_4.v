`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/04 15:24:26
// Design Name: 
// Module Name: encoder10_4
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


module encoder10_4(
    input e,    //使能，高有效
    input [9:0] a,  //待编码信号                              
    output reg f,   //标志，高有效
    output reg [3:0] y  //4位BCD码
    );
  always @(*) begin
    if(e==0)begin
      y=4'd0;
      f=0;
    end
    else    //当e=1时，实现优先编码的功能
        begin
          f=1;
          casex(a)      //x表示任意值
            10'b1x_xxxx_xxxx: y=4'd9;
            10'b01_xxxx_xxxx: y=4'd8;
            10'b00_1xxx_xxxx: y=4'd7;
            10'b00_01xx_xxxx: y=4'd6;
            10'b00_001x_xxxx: y=4'd5;
            10'b00_0001_xxxx: y=4'd4;
            10'b00_0000_1xxx: y=4'd3;
            10'b00_0000_01xx: y=4'd2;
            10'b00_0000_001x: y=4'd1;
            10'b00_0000_0001: y=4'd0;
          default:begin
            y=4'd0;
            f=0;
          end
          endcase
        end
  end
endmodule
