`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/05 20:03:06
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
    input we                //写使能
    );

    reg [31:0] rf [0:31];   //寄存器堆

    assign rd1 = rf[ra1];
    assign rd2 = rf[ra2];

    //初始化寄存器堆
    initial begin
        rf[0] = 32'h00000000;
        rf[1] = 32'h000001F1;
        rf[2] = 32'h00000005;
        rf[3] = 32'h00000FFF;
        rf[4] = 32'h00000005;
        rf[5] = 32'h00000006;
        rf[6] = 32'h00000007;
        rf[7] = 32'h00000004;
        rf[8] = 32'h00000009;
        rf[9] = 32'h0000000A;
        rf[10] = 32'h0000000B;
        rf[11] = 32'h00000004;
        rf[12] = 32'h0000000D;
        rf[13] = 32'h0000000E;
        rf[14] = 32'h0000000F;
        rf[15] = 32'h00000010;
        rf[16] = 32'h0000001A;
        rf[17] = 32'h00000012;
        rf[18] = 32'h00000017;
        rf[19] = 32'h00000014;
        rf[20] = 32'h00000015;
        rf[21] = 32'h00000032;
        rf[22] = 32'h00000010;
        rf[23] = 32'h00000018;
        rf[24] = 32'h00000109;
        rf[25] = 32'h0000001A;
        rf[26] = 32'h0000001B;
        rf[27] = 32'h00000014;
        rf[28] = 32'h0000001D;
        rf[29] = 32'h0000001E;
        rf[30] = 32'h0000001F;
        rf[31] = 32'h000100F0;
    end

    always @(posedge clk) begin
        rf[0] <= 0;  //满足0号寄存器的内容恒为零
    end

    always @(posedge clk) begin
        //忽略对0号寄存器的写
        if(we && wa != 5'b0)begin
            rf[wa] <= wd;   //写操作
        end   
    end

endmodule
