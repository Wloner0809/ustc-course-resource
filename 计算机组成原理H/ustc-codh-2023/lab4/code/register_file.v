`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/22 20:51:31
// Design Name: 
// Module Name: register_file
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


module register_file(
    input clk,
    input [4:0] ra1, ra2,   //读地址
    output [31:0] rd1, rd2, //读数据
    input [4:0] wa,         //写地址
    input [31:0] wd,        //写数据
    input we,               //写使能
    input [4:0] ra3,        //读地址(用于调试)
    output [31:0] rd3       //读数据(用于调试)
    );

    reg [31:0] rf [0:31];   //寄存器堆

    assign rd1 = rf[ra1];
    assign rd2 = rf[ra2];
    assign rd3 = rf[ra3];


    always @(posedge clk) begin
        rf[0] <= 0;  //满足0号寄存器的内容恒为零
        //忽略对0号寄存器的写
        if(we && wa != 5'b0)begin
            rf[wa] <= wd;   //写操作
        end   
    end
endmodule
