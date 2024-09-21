`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/14 20:30:35
// Design Name: 
// Module Name: MEM_WB
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


module MEM_WB(
    input EX_MEM_MemtoReg,
    input EX_MEM_RegWrite,
    input [31:0] EX_MEM_ALUout,
    input [31:0] MEMout,
    input [4:0] EX_MEM_RD,
    input [31:0] EX_MEM_Inst,
    input clk,
    input rstn,
    output reg MEM_WB_MemtoReg,
    output reg MEM_WB_RegWrite,
    output reg [31:0] MEM_WB_ALUout,
    output reg [31:0] MEM_WB_MEMout,
    output reg [4:0] MEM_WB_RD,
    output reg [31:0] MEM_WB_Inst
    );

    always @(posedge clk or negedge rstn) begin
        if(!rstn) begin
            MEM_WB_MemtoReg <= 1'b0;
            MEM_WB_RegWrite <= 1'b0;
            MEM_WB_ALUout <= 32'b0;
            MEM_WB_MEMout <= 32'b0;
            MEM_WB_RD <= 5'b0;
            MEM_WB_Inst <= 32'b0;
        end 
        else begin
            MEM_WB_MemtoReg <= EX_MEM_MemtoReg;
            MEM_WB_RegWrite <= EX_MEM_RegWrite;
            MEM_WB_ALUout <= EX_MEM_ALUout;
            MEM_WB_MEMout <= MEMout;
            MEM_WB_RD <= EX_MEM_RD;
            MEM_WB_Inst <= EX_MEM_Inst;
        end
    end
endmodule
