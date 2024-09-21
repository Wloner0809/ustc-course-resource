module Hazard_Unit(
    input [4:0] rs1, rs2,
    input ID_EX_MemRead,
    input [4:0] ID_EX_RD,
    input [2:0] ID_EX_Branch,
    input PCAsrc, PCBsrc, 
    output reg stall, IF_ID_Flush, ID_EX_Flush
    );
    
    // 处理Load-Use Hazard
    always @(*) begin
        if(ID_EX_MemRead & (ID_EX_RD != 5'b0) & ((ID_EX_RD == rs1) | (ID_EX_RD == rs2)))
            stall = 1'b1;
        else
            stall = 1'b0;
    end

    always @(*) begin
        if(ID_EX_Branch == 3'b100 | ID_EX_Branch == 3'b101) begin
            // 说明是跳转指令
            IF_ID_Flush = 1'b1;
            ID_EX_Flush = 1'b1;            
        end
        else if({PCAsrc, PCBsrc} == 2'b10) begin
            // 跳转成功的情况
            // 为了处理数据相关与控制相关的情况
            IF_ID_Flush = 1'b1;
            ID_EX_Flush = 1'b1; 
        end
        else begin
            IF_ID_Flush = 1'b0;
            ID_EX_Flush = stall ? 1'b1 : 1'b0;
        end
    end
endmodule