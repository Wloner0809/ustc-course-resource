`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/06/08 14:02:47
// Design Name: 
// Module Name: IOU_tb
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


module IOU_tb();
    reg clk, rstn, data, del;
    reg [15:0] x;
    wire [15:0] led;
    wire [31:0] disp_data;
    reg [7:0] io_addr;
    reg [31:0] io_dout;
    reg io_we;
    reg io_rd; 
    wire [31:0] io_din;


    initial begin
        clk = 0;
        rstn = 0;
        data = 0;
        del = 0;
        x = 0;
        io_addr = 0;
        io_dout = 0;
        io_we = 0;
        io_rd = 0;
        #5 rstn = 1;
        #10 x = 2;
        #10 x = 0;
        #10 x = 8;
        #5 data = 1;
        io_addr = 20;
        io_rd = 1;
        #5 data = 0;
        x = 0;
    end


    always #5 clk = ~clk;

    io_unit io_unit_dut(
        .cpu_clk(clk),
        .rstn(rstn),
        .data(data),
        .del(del),
        .x(x),
        .led(led),
        .disp_data(disp_data),
        .io_addr(io_addr),
        .io_dout(io_dout),
        .io_we(io_we),
        .io_rd(io_rd),
        .io_din(io_din)
    );


endmodule
