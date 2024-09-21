`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/08 13:34:30
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


module sort_top_tb();

    reg clk, rstn, run;
    wire [15:0] cycles;
    wire done;

    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        run = 1'b1;
        #5 rstn = 1'b1;
        #1000 rstn = 1'b0;
        #100 rstn = 1'b1;
    end
    always #5 clk = ~clk;

    sort_top sort_top_dut(
        .clk(clk),
        .rstn(rstn),
        .run(run),
        .cycles(cycles),
        .done(done)
    );
    
endmodule
