`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/09 16:59:48
// Design Name: 
// Module Name: register_file_tb
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


module register_file_tb();

    reg clk, we;
    reg [4:0] ra1, ra2, wa;
    reg [31:0] wd;
    wire [31:0] rd1, rd2;
    
    initial begin
        clk = 1'b0;
        we = 1'b0;
        ra1 = 5'b0;
        ra2 = 5'b1;
        wa = 5'b1;
        wd = 32'h89;

        #50 we = 1'b1;
        #5000 we = 1'b0; 
    end

    always #5 clk = ~clk;
    always #20 wa = wa + 1;
    always #20 ra1 = ra1 + 1;
    always #20 ra2 = ra2 + 1;
    always #100 wd = wd + 10;
    
    register_file register_file_dut(
        .clk(clk),
        .we(we),
        .ra1(ra1),
        .ra2(ra2),
        .wa(wa),
        .wd(wd),
        .rd1(rd1),
        .rd2(rd2)
    );
endmodule
