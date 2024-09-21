`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/29 20:42:44
// Design Name: 
// Module Name: Control
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


module Control(
    input [31:0] Instruction,
    output reg ALUAsrc,
    output reg [1:0] ALUBsrc,
    output reg [3:0] ALUop,
    output reg MemRead, MemWrite,
    output reg MemtoReg,
    output reg [2:0] Branch,
    output reg RegWrite
    );

    always @(*) begin
        case (Instruction[6:0])
            7'b0110011: begin
                //add、sub、and、or、xor
                ALUAsrc = 1'b1;
                ALUBsrc = 2'b00;
                if({Instruction[31:25], Instruction[14:12]} == 10'b0000000000)
                    //add
                    ALUop = 4'b0000;
                else if({Instruction[31:25], Instruction[14:12]} == 10'b0100000000)
                    //sub
                    ALUop = 4'b1000;
                else if({Instruction[31:25], Instruction[14:12]} == 10'b0000000100)
                    //xor
                    ALUop = 4'bx100;
                else if({Instruction[31:25], Instruction[14:12]} == 10'b0000000110)
                    //or
                    ALUop = 4'bx110;
                else if({Instruction[31:25], Instruction[14:12]} == 10'b0000000111)
                    //and
                    ALUop = 4'bx111;
                else    
                    //avoid latch
                    ALUop = 4'bxxxx;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b1;
                Branch = 3'b000;
                RegWrite = 1'b1;
            end
            7'b0010011: begin
                //addi、slli、srli、srai
                ALUAsrc = 1'b1;
                ALUBsrc = 2'b10;
                if(Instruction[14:12] == 3'b000)
                    //addi
                    ALUop = 4'b0000;
                else if(Instruction[14:12] == 3'b001)
                    //slli
                    ALUop = 4'bx001;
                else if(Instruction[14:12] == 3'b101) begin
                    if(Instruction[31:25] == 7'b0000000)
                        //srli
                        ALUop = 4'b0101;
                    else
                        //srai
                        ALUop = 4'b1101; 
                end
                else
                    ALUop = 4'bxxxx;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b1;
                Branch = 3'b000;
                RegWrite = 1'b1;
            end
            7'b0110111: begin
                //lui
                ALUAsrc = 1'bx;
                ALUBsrc = 2'b10;
                ALUop = 4'bx011;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b1;
                Branch = 3'b000;
                RegWrite = 1'b1;
            end
            7'b0010111: begin
                //auipc
                ALUAsrc = 1'b0;
                ALUBsrc = 2'b10;
                ALUop = 4'b0000;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b1;
                Branch = 3'b000;
                RegWrite = 1'b1;
            end
            7'b0000011: begin
                //lw
                ALUAsrc = 1'b1;
                ALUBsrc = 2'b10;
                ALUop = 4'b0000;
                MemRead = 1'b1;
                MemWrite = 1'b0;
                MemtoReg = 1'b0;
                Branch = 3'b000;
                RegWrite = 1'b1;
            end
            7'b0100011: begin
                //sw
                ALUAsrc = 1'b1;
                ALUBsrc = 2'b10;
                ALUop = 4'b0000;
                MemRead = 1'b0;
                MemWrite = 1'b1;
                MemtoReg = 1'bx;
                Branch = 3'b000;
                RegWrite = 1'b0;
            end
            7'b1100011: begin
                //beq、blt、bltu
                ALUAsrc = 1'b1;
                ALUBsrc = 2'b00;
                if(Instruction[14:12] == 3'b000) begin
                    //beq
                    ALUop = 4'b1000;
                    Branch = 3'b001;
                end
                else if(Instruction[14:12] == 3'b100) begin
                    //blt
                    ALUop = 4'b0010;
                    Branch = 3'b010;
                end
                else if(Instruction[14:12] == 3'b110) begin
                    //bltu
                    ALUop = 4'b1010;
                    Branch = 3'b011;
                end
                else begin
                    //avoid latch
                    ALUop = 4'bxxxx;
                    Branch = 3'b000;
                end
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b0;
                RegWrite = 1'b0;
            end
            7'b1101111: begin
                //jal
                ALUAsrc = 1'b0;
                ALUBsrc = 2'b01;
                ALUop = 4'b0000;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b1;
                Branch = 3'b100;
                RegWrite = 1'b1;
            end
            7'b1100111: begin
                //jalr
                ALUAsrc = 1'b0;
                ALUBsrc = 2'b01;
                ALUop = 4'b0000;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b1;
                Branch = 3'b101;
                RegWrite = 1'b1;
            end
            default: begin
                //avoid latch
                ALUAsrc = 1'b1;
                ALUBsrc = 2'b00;
                ALUop = 4'b0000;
                MemRead = 1'b0;
                MemWrite = 1'b0;
                MemtoReg = 1'b0;
                Branch = 3'b000;
                RegWrite = 1'b0;
            end
        endcase
    end

endmodule