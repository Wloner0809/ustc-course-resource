`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/08 12:50:34
// Design Name: 
// Module Name: sort_top
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


module sort_top(
    input clk, rstn, run,
    output [15:0] cycles,
    output done
    );

    wire [31:0] spo, dpo, d;
    wire [7:0] a, dpra;
    wire [2:0] sel;
    wire [3:0] NS;
    wire we, cmp;


    //下面用于获取数组大小
    reg [31:0] num;
    wire [31:0] temp;
    always @(posedge clk) begin
        if(a == 0)
            num <= spo;
        else if(dpra == 0)
            num <= dpo;
        else 
            num <= num;
    end
    assign temp = num;

    dist_mem_gen_0 dist_mem_gen_0_dut (
        .a(a),        // input wire [7 : 0] a
        .d(d),        // input wire [31 : 0] d
        .dpra(dpra),  // input wire [7 : 0] dpra
        .clk(clk),    // input wire clk
        .we(we),      // input wire we
        .spo(spo),    // output wire [31 : 0] spo
        .dpo(dpo)     // output wire [31 : 0] dpo
    );

    Addr_change Addr_change_dut(
        .clk(clk),
        .sel(sel),
        .addr1(a),
        .addr2(dpra)
    );

    Data_change Data_change_dut(
        .clk(clk),
        .data1(spo),
        .data2(dpo),
        .NS(NS),
        .cmp(cmp),
        .d(d)
    );

    sort_control sort_control_dut(
        .clk(clk),
        .rstn(rstn),
        .run(run),
        .cmp(cmp),
        .cycles(cycles),
        .done(done),
        .we(we),
        .sel(sel),
        .next_state(NS),
        .num(temp)
    );

endmodule
