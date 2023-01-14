`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/31 23:55:15
// Design Name: 
// Module Name: display_tb
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


module display_tb();

    reg [31:0] d;
    reg clk,rstn;
    wire [7:0] an;
    wire [6:0] cn;

    initial begin
        clk = 1'b0;
        d = 32'h33000106;
        rstn = 1'b1;
    end
    always #5 clk = ~clk;
    always #1000000 d = d >> 1;

    Display Display_test(
        .d(d),
        .clk(clk),
        .rstn(rstn),
        .an(an),
        .cn(cn)
    );
endmodule
