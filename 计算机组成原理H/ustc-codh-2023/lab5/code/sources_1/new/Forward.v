`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/14 20:29:02
// Design Name: 
// Module Name: Forward
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


module Forward(
    input EX_MEM_RegWrite,
    input MEM_WB_RegWrite,
    input [4:0] ID_EX_RS1,
    input [4:0] ID_EX_RS2,
    input [4:0] EX_MEM_RD,
    input [4:0] MEM_WB_RD,
    output reg [1:0] ForwardA,
    output reg [1:0] ForwardB
    );

    always @(*) begin
        if(EX_MEM_RegWrite & (EX_MEM_RD !=0) & (EX_MEM_RD == ID_EX_RS1))
            ForwardA = 2'b10;
        else if(MEM_WB_RegWrite & (MEM_WB_RD !=0) & (MEM_WB_RD == ID_EX_RS1))
            ForwardA = 2'b01;
        else 
            ForwardA = 2'b00;
    end
    always @(*) begin
        if(EX_MEM_RegWrite & (EX_MEM_RD !=0) & (EX_MEM_RD == ID_EX_RS2))
            ForwardB = 2'b10;
        else if(MEM_WB_RegWrite & (MEM_WB_RD !=0) & (MEM_WB_RD == ID_EX_RS2))
            ForwardB = 2'b01;
        else 
            ForwardB = 2'b00;
    end

endmodule
