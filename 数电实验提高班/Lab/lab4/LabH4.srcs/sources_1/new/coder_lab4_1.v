`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/30 18:15:21
// Design Name: 
// Module Name: coder_lab4_1
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


module coder_lab4_1(
    input sel,x,rstn,clk,
    output [7:0] an,
    output [6:0] cn
    );
    wire y,p,q;
    wire [31:0] data;

    Debounce Debounce_dut(
        .x(x),
        .clk(clk),
        .rstn(rstn),
        .y(y)
    );
    
    assign p = sel ? y : x;

    syn_ps syn_ps_dut(
        .clk(clk),
        .rstn(rstn),
        .a(p),
        .p(q)
    );

    counter counter_dut(
        .clk(clk),
        .rstn(rstn),
        .d(32'b0),
        .pe(1'b0),
        .ce(q),
        .q(data)
    );

    Display Display_dut(
        .d(data),
        .clk(clk),
        .rstn(rstn),
        .an(an),
        .cn(cn)
    );
    
endmodule
