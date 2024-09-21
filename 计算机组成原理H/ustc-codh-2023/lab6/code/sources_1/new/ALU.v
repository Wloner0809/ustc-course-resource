`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/29 20:40:45
// Design Name: 
// Module Name: ALU
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


module ALU #(
    parameter WIDTH = 32
)(
    input [WIDTH-1:0] a,b,
    input [3:0] f,
    output reg [WIDTH-1:0] y,
    output reg Zero, Less   
);

    always @(*) begin
        casex (f)
            4'b0000: begin
                //add operation
                y = a + b;
                Zero = 0;
                Less = 0;
            end
            4'b1000: begin
                //sub operation
                //this case doesn't set Less
                y = a - b;
                Zero = y ? 0 : 1;
                Less = 0;
            end
            4'bx001: begin
                //shift left operation
                y = a << b;
                Zero = 0;
                Less = 0;
            end
            4'b0010: begin
                //sub operation
                //this case compare two signed operands
                y = a - b;
                Zero = y ? 0 : 1;
                Less = ($signed(a) < $signed(b)) ? 1 : 0;
            end
            4'b1010: begin
                //sub operation
                //this case compare two unsigned operands
                y = a - b;
                Zero = y ? 0 : 1;
                Less = (a < b) ? 1 : 0;
            end
            4'bx011: begin
                //choose operand b to output directly
                y = b;
                Zero = 0;
                Less = 0;
            end
            4'bx100: begin
                //xor operation
                y = a ^ b;
                Zero = 0;
                Less = 0;
            end
            4'b0101: begin
                //logical shift right operation
                y = a >> b;
                Zero = 0;
                Less = 0;
            end
            4'b1101: begin
                //arithmetical shift right operation
                y = $signed(a) >>> b;
                Zero = 0;
                Less = 0;
            end
            4'bx110: begin
                //or operation
                y = a | b;
                Zero = 0;
                Less = 0;
            end
            4'bx111: begin
                //and operation
                y = a & b;
                Zero = 0;
                Less = 0;
            end
            default: begin
                y = 0;
                Zero = 0;
                Less = 0;
            end      
        endcase
    end
endmodule
