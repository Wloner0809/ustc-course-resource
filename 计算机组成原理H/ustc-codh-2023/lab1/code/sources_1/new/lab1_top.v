`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 09:37:53
// Design Name: 
// Module Name: lab1_top
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


module lab1_top(
    input clk,
    input rstn,
    input en,
    input [15:0] d,
    output [15:0] m
    );
    wire en_mid, en_final;
    wire [15:0] d_temp;

    Debounce Debounce_dut(
        .clk(clk),
        .rstn(rstn),
        .x(en),
        .y(en_mid)
    );
    syn_ps syn_ps_dut(
        .clk(clk),
        .rstn(rstn),
        .a(en_mid),
        .p(en_final)
    );

    genvar i;
    generate
        for(i = 0; i < 16; i = i + 1)
        begin:block
            Debounce Debounce_dut(
                .x(d[i]),
                .y(d_temp[i]),
                .clk(clk),
                .rstn(rstn)
            );
        end
    endgenerate

    MAV MAV_dut(
        .clk(clk),
        .rstn(rstn),
        .en(en_final),
        .d(d_temp),
        .m(m)
    );
endmodule
