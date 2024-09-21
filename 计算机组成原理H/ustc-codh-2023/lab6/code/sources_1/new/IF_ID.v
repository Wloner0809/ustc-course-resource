module IF_ID(
    input [31:0] PC,
    input [31:0] Inst,
    input stall,
    input IF_ID_Flush,
    input clk,
    input rstn,
    input cache_stall,
    output reg [31:0] IF_ID_PC,
    output reg [31:0] IF_ID_Inst
    );

    always @(posedge clk or negedge rstn) begin
        if(!rstn) begin
            IF_ID_PC <= 32'b0;
            IF_ID_Inst <= 32'b0;
        end
        else if(stall | cache_stall) begin
            IF_ID_PC <= IF_ID_PC;
            IF_ID_Inst <= IF_ID_Inst;
        end
        else if(IF_ID_Flush) begin
            IF_ID_PC <= 32'b0;
            IF_ID_Inst <= 32'b0;
        end
        else begin
            IF_ID_PC <= PC;
            IF_ID_Inst <= Inst;
        end
    end
endmodule
