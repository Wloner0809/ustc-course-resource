`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/15 21:34:54
// Design Name: 
// Module Name: CPU_tb
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


module CPU_tb();

    reg clk, rstn;
    wire [31:0] npc;  //npc就是IF阶段pc_reg中的npc
    wire [31:0] pc;   //pc就是IF阶段pc_reg中的pc
    wire [31:0] ir;   //ir就是ID阶段的ins_D
    wire [31:0] pcd;  //pcd就是ID阶段的pc
    wire [31:0] imm;  //imm就是ID阶段的imm
    wire [31:0] a;    //a就是EX阶段ALU的a
    wire [31:0] b;    //b就是EX阶段ALU的b
    wire [31:0] pce;  //pce就是EX阶段的pc
    wire [31:0] ctre; //ctr就是EX阶段的ctre(控制信号总线)
    wire [31:0] mdw;  //mdw就是EX向MEM阶段传入的Rs2_data(mem_data_write)
    wire [31:0] y;    //y就是EX阶段的ALU_out
    wire [31:0] ctrm; //ctrm就是MEM阶段的ctrm(控制信号总线)
    wire [31:0] yw;   //yw就是WB阶段的y
    wire [31:0] mdr;  //mdr就是WB阶段的mem_data_read
    wire [31:0] ctrw;  //ctrw就是WB阶段的ctrm(控制信号总线)
    wire [31:0] ire;
    wire [31:0] irm;
    wire [31:0] irw;

    initial begin
        rstn = 1'b0;
        clk = 1'b0;
        #10 rstn = 1'b1;
    end
    always #5 clk = ~clk;
    CPU CPU_tb(
        .clk(clk),
        .rstn(rstn),
        .npc(npc),
        .pc(pc),
        .ir(ir),
        .pcd(pcd),
        .imm(imm),
        .a(a),
        .b(b),
        .pce(pce),
        .ctre(ctre),
        .mdw(mdw),
        .y(y),
        .ctrm(ctrm),
        .yw(yw),
        .mdr(mdr),
        .ctrw(ctrw),
        .ire(ire),
        .irm(irm),
        .irw(irw)
    );

endmodule
