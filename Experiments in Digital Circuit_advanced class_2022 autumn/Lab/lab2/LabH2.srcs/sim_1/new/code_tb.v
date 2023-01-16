`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/18 15:51:02
// Design Name: 
// Module Name: code_tb
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


module code_tb();
        wire [15:0] y;
        wire [4:0] q;
        reg en,rstn,clk;
        reg [7:0] a,b;
        code code_test(
            .a(a),
            .b(b),
            .en(en),
            .rstn(rstn),
            .clk(clk),
            .q(q),
            .y(y)
        );
        initial begin
            clk = 1;
            forever #50 clk = ~clk;
        end
        initial begin
            rstn = 1; en = 1 ; a = 8'b0000_1100; b = 8'b0000_0110;
            #100  a = 8'b1111_1100; b = 8'b1001_1011;
            #100  rstn = 0;
            #100  rstn = 1; a = 8'b1010_1101; b = 8'b1101_1000;
            #200  a = 8'b0111_1001; b = 8'b1101_1010;
        end
endmodule
