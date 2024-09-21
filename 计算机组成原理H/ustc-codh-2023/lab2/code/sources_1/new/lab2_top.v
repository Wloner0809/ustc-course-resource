`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/09 14:23:51
// Design Name: 
// Module Name: lab2_top
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


module lab2_top(
    input clk,
    input rstn,
    input run,              //启动排序
    output done,            //排序结束
    output [15:0] cycles,   //排序耗费时钟周期数
    input rxd, 
    output txd
    );

    //SDU_DM接口
    wire [31:0] addr;       //读or写地址
    wire [31:0] dout;       //读数据
    wire [31:0] din;        //写数据
    wire we;                //写使能    
    wire clk_ld;            //写时钟


    wire [31:0] dpo;
    wire [7:0] dpra;
    wire [2:0] sel;
    wire [3:0] NS;
    wire cmp, run_final;


    //下面用于解决多驱动问题
    //排序结束作为选择信号
    wire [7:0] a;
    wire [31:0] addr_temp;
    assign a = done ? addr_temp[7:0] : (run_final ? addr[7:0] : addr_temp[7:0]); 

    wire we_temp, we_dm;
    assign we_dm = done ? we_temp : (run_final ? we : we_temp);

    wire [31:0] din_temp, din_dm;
    assign din_dm = done ? din_temp : (run_final ? din : din_temp);

    wire clk_ld_temp;
    assign clk_ld_temp = done ? clk_ld : (run_final ? clk : clk_ld);



    //下面用于获取数组大小
    reg [31:0] num;
    wire [31:0] temp;
    always @(posedge clk) begin
        if(a == 0)
            num <= dout;
        else if(dpra == 0)
            num <= dpo;
        else 
            num <= num;
    end
    assign temp = num;


    Debounce Debounce_dut(
        .clk(clk),
        .rstn(rstn),
        .x(run),
        .y(run_final)
    );

    dist_mem_gen_0 dist_mem_gen_0_dut (
        .a(a),              // input wire [7 : 0] a
        .d(din_dm),            // input wire [31 : 0] d
        .dpra(dpra),        // input wire [7 : 0] dpra
        .clk(clk_ld_temp),  // input wire clk
        .we(we_dm),         // input wire we
        .spo(dout),         // output wire [31 : 0] spo
        .dpo(dpo)           // output wire [31 : 0] dpo
    );

    Addr_change Addr_change_dut(
        .clk(clk),
        .sel(sel),
        .addr1(addr[7:0]),
        .addr2(dpra)
    );

    Data_change Data_change_dut(
        .clk(clk),
        .data1(dout),
        .data2(dpo),
        .NS(NS),
        .cmp(cmp),
        .d(din)
    );

    sort_control sort_control_dut(
        .clk(clk),
        .rstn(rstn),
        .run(run_final),
        .cmp(cmp),
        .cycles(cycles),
        .done(done),
        .we(we),
        .sel(sel),
        .next_state(NS),
        .num(temp)
    );


    sdu_dm sdu_dm_dut(
        .clk(clk),
        .rstn(rstn),
        .rxd(rxd),
        .txd(txd),
        .addr(addr_temp),
        .dout(dout),
        .din(din_temp),
        .we(we_temp),
        .clk_ld(clk_ld)
    );

endmodule
