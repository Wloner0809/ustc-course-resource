`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/14 20:30:17
// Design Name: 
// Module Name: EX_MEM
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


module EX_MEM(
    input ID_EX_MemtoReg,
    input ID_EX_RegWrite,
    input ID_EX_MemRead,
    input ID_EX_MemWrite,
    input [31:0] ALUout,
    input [31:0] ID_EX_RD2,
    input [4:0] ID_EX_RD,
    input [31:0] ID_EX_Inst, 
    input clk,
    input rstn,
    output reg EX_MEM_MemtoReg,
    output reg EX_MEM_RegWrite,
    output reg EX_MEM_MemRead,
    output reg EX_MEM_MemWrite,
    output reg [31:0] EX_MEM_ALUout,
    output reg [31:0] EX_MEM_RD2,
    output reg [4:0] EX_MEM_RD,
    output reg [31:0] EX_MEM_Inst
    );

    always @(posedge clk or negedge rstn) begin
        if(!rstn) begin
            EX_MEM_MemtoReg <= 1'b0;
            EX_MEM_RegWrite <= 1'b0;
            EX_MEM_MemRead <= 1'b0;
            EX_MEM_MemWrite <= 1'b0;
            EX_MEM_ALUout <= 32'b0;
            EX_MEM_RD2 <= 32'b0;
            EX_MEM_RD <= 5'b0;
            EX_MEM_Inst <= 32'b0;
        end
        else begin
            EX_MEM_MemtoReg <= ID_EX_MemtoReg;
            EX_MEM_RegWrite <= ID_EX_RegWrite;
            EX_MEM_MemRead <= ID_EX_MemRead;
            EX_MEM_MemWrite <= ID_EX_MemWrite;
            EX_MEM_ALUout <= ALUout;
            EX_MEM_RD2 <= ID_EX_RD2;
            EX_MEM_RD <= ID_EX_RD;
            EX_MEM_Inst <= ID_EX_Inst;
        end
    end
endmodule
