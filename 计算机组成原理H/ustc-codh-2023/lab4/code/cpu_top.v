`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/24 20:08:23
// Design Name: 
// Module Name: cpu_top
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


module cpu_top(
    input clk, rstn, clk_ld,
    input debug,
    input [31:0] addr,
    input [31:0] din,
    input we_dm, we_im,
    output [31:0] pc_chk, npc, pc,
    output [31:0] IR,
    output [31:0] CTL,  //control signal
    output [31:0] A, B,
    output [31:0] IMM,
    output [31:0] Y,
    output [31:0] MDR,
    output [31:0] dout_rf, dout_im, dout_dm,
    output reg [15:0] led
    );


    wire [31:0] Instruction;
    wire [31:0] WD;
    reg [31:0] PC, NPC;
    wire [31:0] RD1, RD2;
    //control signal
    wire ALUAsrc, MemRead, MemWrite, MemtoReg, RegWrite;
    wire [1:0] ALUBsrc;
    wire [3:0] ALUop;
    wire [2:0] Branch;

    //used in Branch
    wire Zero, Less;

    //used in PC calculation
    wire PCAsrc, PCBsrc;
    //集成在一起的control signal
    assign CTL = {16'b0, PCAsrc, PCBsrc, ALUAsrc, MemRead, MemWrite, MemtoReg, RegWrite, ALUBsrc, ALUop, Branch};
    
    wire CLK; 
    assign CLK = debug ? clk_ld : clk;
    wire WE_DM; 
    assign WE_DM = debug ? we_dm : MemWrite;


    //有关PC
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            PC <= 32'h00000000;
        else
            PC <= NPC;
    end

    always @(*) begin
        case ({PCAsrc, PCBsrc})
            2'b00: begin
                NPC = PC + 32'h00000004;
            end
            2'b10: begin
                NPC = IMM + PC;
            end
            2'b11: begin
                NPC = (IMM + RD1) & ~1;
            end
            default: begin
                NPC = 32'h00000000;
            end
        endcase
    end

    assign pc = PC;
    assign npc = NPC;
    assign pc_chk = PC;
    assign IR = Instruction;



    //IO
    //CPU输入
    reg [31:0] clk_cpu_cnt;
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            clk_cpu_cnt <= 32'h00000000;
        else
            clk_cpu_cnt <= clk_cpu_cnt + 1;
    end


    Instruction_memory IM(
        .a(addr[9:0]),
        .d(din),
        .dpra(PC[9:0] >> 2),
        .clk(CLK), 
        .we(we_im),
        .spo(dout_im),
        .dpo(Instruction)
    );

    //这里主要是为了处理从外设输入的情况
    //输入内容为CPU工作时钟的计数
    assign WD = (Y == 32'h00003f20) ? clk_cpu_cnt : (MemtoReg ? Y : MDR);

    register_file RF(
        .clk(clk),
        .ra1(Instruction[19:15]),
        .ra2(Instruction[24:20]),
        .rd1(RD1),
        .rd2(RD2),
        .wa(Instruction[11:7]),
        .wd(WD),
        .we(RegWrite),
        .ra3(addr[4:0]),
        .rd3(dout_rf)
    );

    Imm_Gen IG(
        .Instruction(Instruction),
        .imm(IMM)
    );

    Control Control_dut(
        .Instruction(Instruction),
        .ALUAsrc(ALUAsrc),
        .ALUBsrc(ALUBsrc),
        .ALUop(ALUop),
        .MemRead(MemRead),
        .MemWrite(MemWrite),
        .MemtoReg(MemtoReg),
        .Branch(Branch),
        .RegWrite(RegWrite)
    );

    assign A = ALUAsrc ? RD1 : PC;
    assign B = (ALUBsrc == 2'b00) ? RD2 : ((ALUBsrc == 2'b01) ? 32'h00000004 : IMM);

    alu alu_dut(
        .a(A),
        .b(B),
        .f(ALUop),
        .y(Y),
        .Zero(Zero),
        .Less(Less)
    );

    Branch_control BC(
        .Zero(Zero),
        .Less(Less),
        .Branch(Branch),
        .PCAsrc(PCAsrc),
        .PCBsrc(PCBsrc)
    );


    wire [9:0] ADDR_DM_WRITE;
    assign ADDR_DM_WRITE = debug ? addr[9:0] : (Y[9:0] >> 2);

    wire [31:0] DATA_DM_WRITE;
    assign DATA_DM_WRITE = debug ? din : RD2;

    // pay attention to which port "we" makes difference to.
    Data_memory DM(
        //address here is similar to the address in IM
        .a(ADDR_DM_WRITE),
        .d(DATA_DM_WRITE),
        .dpra(addr[9:0]),
        .clk(CLK),
        .we(WE_DM),
        .spo(MDR),
        .dpo(dout_dm)
    );

    //IO
    //CPU输出
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            led <= 16'hffff;
        else if(Y == 32'h00003f00)
            led <= RD2[15:0];
        else    
            led <= led;
    end
endmodule
