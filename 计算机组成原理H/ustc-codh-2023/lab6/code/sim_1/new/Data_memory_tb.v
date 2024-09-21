`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/30 08:19:22
// Design Name: 
// Module Name: Data_memory_tb
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


module Data_memory_tb();

    reg clk;
    reg [11 : 0] addr;
    reg [7 : 0] din;
    reg we;
    wire [7 : 0] dout;

    initial begin
        clk = 0;
        addr = 0;
        din = 3;
        we = 0;
        #100 we = 1;
    end
    always #5 clk = ~clk;
    always #20 din = din + 1;
    always #10 addr = addr + 1;
    // always #20 we = ~we;

    Data_memory DM(
        .clk(clk),
        .addr(addr),
        .din(din),
        .we(we),
        .dout(dout)
    );


endmodule
