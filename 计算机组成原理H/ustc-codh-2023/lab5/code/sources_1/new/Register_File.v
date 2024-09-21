`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/14 13:56:48
// Design Name: 
// Module Name: Register_File
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


module Register_File(
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
    //测试用
    initial begin
        rf[0] = 32'h00000000;
        rf[1] = 32'h00000000;
        rf[2] = 32'h00000000;
        rf[3] = 32'h00000000;
        rf[4] = 32'h00000000;
        rf[5] = 32'h00000000;
        rf[6] = 32'h00000000;
        rf[7] = 32'h00000000;
        rf[8] = 32'h00000000;
        rf[9] = 32'h00000000;
        rf[10] = 32'h00000000;
        rf[11] = 32'h00000000;
        rf[12] = 32'h00000000;
        rf[13] = 32'h00000000;
        rf[14] = 32'h00000000;
        rf[15] = 32'h00000000;
        rf[16] = 32'h00000000;
        rf[17] = 32'h00000000;
        rf[18] = 32'h00000000;
        rf[19] = 32'h00000000;
        rf[20] = 32'h00000000;
        rf[21] = 32'h00000000;
        rf[22] = 32'h00000000;
        rf[23] = 32'h00000000;
        rf[24] = 32'h00000000;
        rf[25] = 32'h00000000;
        rf[26] = 32'h00000000;
        rf[27] = 32'h00000000;
        rf[28] = 32'h00000000;
        rf[29] = 32'h00000000;
        rf[30] = 32'h00000000;
        rf[31] = 32'h00000000;
    end

endmodule
