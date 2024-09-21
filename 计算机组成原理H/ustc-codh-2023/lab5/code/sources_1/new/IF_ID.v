`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/14 20:29:28
// Design Name: 
// Module Name: IF_ID
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


module IF_ID(
    input [31:0] PC,
    input [31:0] Inst,
    input stall,
    input IF_ID_Flush,
    input clk,
    input rstn,
    output reg [31:0] IF_ID_PC,
    output reg [31:0] IF_ID_Inst
    );

    always @(posedge clk or negedge rstn) begin
        if(!rstn | IF_ID_Flush) begin
            IF_ID_PC <= 32'b0;
            IF_ID_Inst <= 32'b0;
        end
        else if(stall) begin
            IF_ID_PC <= IF_ID_PC;
            IF_ID_Inst <= IF_ID_Inst;
        end
        else begin
            IF_ID_PC <= PC;
            IF_ID_Inst <= Inst;
        end
    end
endmodule
