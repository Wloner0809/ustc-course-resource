module Imm_Gen(
    input [31:0] Instruction,
    output reg [31:0] imm
    );
    always @(*) begin
        case (Instruction[6:0])
            7'b0110011: begin
                //add、sub、and、or、xor
                imm = 0;
            end
            7'b0010011: begin
                //addi、slli、srli、srai
                if(Instruction[14:12] == 3'b101)
                    imm = {27'b0, Instruction[24:20]};
                else
                    imm = {{20{Instruction[31]}}, Instruction[31:20]};
            end
            7'b0110111: begin
                //lui
                imm = {Instruction[31:12], 12'b0};
            end
            7'b0010111: begin
                //auipc
                imm = {Instruction[31:12], 12'b0};
            end
            7'b0000011: begin
                //lw
                imm = {{20{Instruction[31]}}, Instruction[31:20]};
            end
            7'b0100011: begin
                //sw
                imm = {{20{Instruction[31]}}, Instruction[31:25],Instruction[11:7]};
            end
            7'b1100011: begin
                //beq、blt、bltu
                imm = {{20{Instruction[31]}}, Instruction[7], Instruction[30:25], Instruction[11:8], 1'b0};
            end
            7'b1101111: begin
                //jal
                imm = {{12{Instruction[31]}}, Instruction[19:12], Instruction[20], Instruction[30:21], 1'b0};
            end
            7'b1100111: begin
                //jalr
                imm = {{20{Instruction[31]}}, Instruction[31:20]};
            end
            default: begin
                imm = 0;
            end
        endcase
    end

endmodule
