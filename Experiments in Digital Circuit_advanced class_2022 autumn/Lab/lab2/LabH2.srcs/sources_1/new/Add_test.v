`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/18 13:16:27
// Design Name: 
// Module Name: Add_test
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


module Add_test(
    input [7:0] a,b,
    input ci,clk,en,rstn,
    output [7:0] s,
    output co
    );
    wire [7:0] c,d,sum;
    wire e,f;
    register register_dut1(
        .d(a),
        .q(c),
        .clk(clk),
        .en(en),
        .rstn(rstn)
    );
    register register_dut2(
        .d(b),
        .q(d),
        .clk(clk),
        .en(en),
        .rstn(rstn)
    );
    register register_dut3(
        .d(ci),
        .q(e),
        .clk(clk),
        .en(en),
        .rstn(rstn)
    );
    ahead_nbits_adder ahead_nbits_adder_dut(
        .a(c),
        .b(d),
        .ci(e),
        .s(sum),
        .co(f)
    );
    register register_dut4(
        .d(sum),
        .q(s),
        .clk(clk),
        .en(en),
        .rstn(rstn)
    );
    register register_dut5(
        .d(f),
        .q(co),
        .clk(clk),
        .en(en),
        .rstn(rstn)
    );
endmodule
