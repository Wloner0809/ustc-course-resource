`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/03/30 22:40:04
// Design Name: 
// Module Name: MAV
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


module MAV(
    input clk,
    input rstn,
    input en,
    input [15:0] d,
    output [15:0] m
    );
    reg [15:0] temp;    
    reg [63:0] num;     //存放最近四个number
    wire [15:0] alu_mid1, alu_mid2, alu_mid3, alu_mid4, m_temp0, m_temp;
    wire [2:0] t1, t2, t3, t4; 
    reg sel = 1'b0;     //用于选择赋给m的是temp还是m_temp
    //采用顺序码
    parameter s0 = 3'b000, 
              s1 = 3'b001,
              s2 = 3'b010,
              s3 = 3'b011,
              s4 = 3'b100;
    reg [2:0] NS,CS;
    
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            CS <= s0;
        else 
            CS <= NS;
    end

    ALU #(16) ALU_dut1(
        .a(num[15:0]),
        .b(num[31:16]),
        .f(3'b001),
        .y(alu_mid1),
        .t(t1)
    );
    ALU #(16) ALU_dut2(
        .a(num[47:32]),
        .b(num[63:48]),
        .f(3'b001),
        .y(alu_mid2),
        .t(t2)
    );
    assign alu_mid3 = alu_mid1;
    assign alu_mid4 = alu_mid2;
    ALU #(16) ALU_dut3(
        .a(alu_mid3),
        .b(alu_mid4),
        .f(3'b001),
        .y(m_temp0),
        .t(t3)
    );
    ALU #(16) ALU_dut4(
        .a(m_temp0),
        .b(16'h0002),
        .f(3'b101),
        .y(m_temp),
        .t(t4)
    );


    always @(posedge clk or negedge rstn) begin

        if(!rstn)begin
            temp <= 16'h0;
            num <= 64'h0;
            NS <= s0;
            sel <= 1'b0;
        end
        else begin
            if(en)begin
                case(CS)
                s0:begin
                    temp <= d;
                    num[15:0] <= d;
                    NS <= s1;
                    sel <= 1'b0;
                end 
                s1:begin
                    temp <= d;
                    num[31:16] <= d;
                    NS <= s2;
                    sel <= 1'b0;
                end
                s2:begin
                    temp <= d;
                    num[47:32] <= d;
                    NS <= s3;
                    sel <= 1'b0;
                end
                s3:begin
                    temp <= m_temp;
                    num[63:48] <= d;
                    NS <= s4;
                    sel <= 1'b1;
                end
                s4:begin
                    temp <= m_temp;
                    num <= {d, num[63:16]};
                    NS <= s4;
                    sel <= 1'b1;
                end
                endcase
            end
            else begin
                temp <= temp;
                num <= num;
                NS <= NS;
                sel <= sel;
            end
        end
    end

    assign m = sel ? m_temp : temp;

endmodule
