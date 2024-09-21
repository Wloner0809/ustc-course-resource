`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/14 20:26:49
// Design Name: 
// Module Name: Branch
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


module Branch(
    input Zero, Less,
    input [2:0] Branch,
    output reg PCAsrc, PCBsrc
    );

    always @(*) begin
        case (Branch)
            3'b000: begin
                PCAsrc = 1'b0;
                PCBsrc = 1'b0;
            end
            3'b001: begin
                PCBsrc = 1'b0;
                if(Zero) 
                    PCAsrc = 1'b1;
                else 
                    PCAsrc = 1'b0;
            end
            3'b010: begin
                PCBsrc = 1'b0;
                if(Less)
                    PCAsrc = 1'b1;
                else
                    PCAsrc = 1'b0; 
            end
            3'b011: begin
                PCBsrc = 1'b0;
                if(Less)
                    PCAsrc = 1'b1;
                else    
                    PCAsrc = 1'b0;
            end
            3'b100: begin
                PCAsrc = 1'b1;
                PCBsrc = 1'b0;
            end
            3'b101: begin
                PCAsrc = 1'b1;
                PCBsrc = 1'b1;
            end
            default: begin
                //avoid latch
                PCAsrc = 1'bx;
                PCBsrc = 1'bx;
            end
        endcase
    end
endmodule
