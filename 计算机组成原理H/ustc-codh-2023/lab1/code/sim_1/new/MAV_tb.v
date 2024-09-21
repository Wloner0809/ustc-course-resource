`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 08:10:01
// Design Name: 
// Module Name: MAV_tb
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


module MAV_tb();

    reg clk, rstn, en;
    reg [15:0] d;
    wire [15:0] m;
    initial begin
        rstn = 1'b0;
        en = 1'b0;
        clk = 1'b0;
        d = 16'h0004;
        #100 rstn = 1'b1;
        #20 d = 16'h0002;
        #20 d = 16'h0003;
        #50 en = 1'b1;
        #20 d = 16'h0001;
        #20 d = 16'h0005;
        #20 d = 16'h0006;
        #20 d = 16'h0007;
        #20 d = 16'h0008;
    end
    always #5 clk = ~clk;
    always #10 en = ~en;
    MAV MAV_dut(
        .clk(clk),
        .rstn(rstn),
        .en(en),
        .d(d),
        .m(m)
    );
    
endmodule
