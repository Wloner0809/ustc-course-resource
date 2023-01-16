`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/05 13:33:17
// Design Name: 
// Module Name: decoder4_10_tb
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

module decoder4_10_tb();
    //输入
    reg [3:0] d;
    //输出
    wire [9:0] y;

    initial begin
       d <= 4'd0; 
    end

    always #10 d <= {$random} % 10;
    
    initial begin
        $monitor("time:%t d:%b y: %b",$time,d,y);
    end
    
    decoder4_10 decoder4_10_dut(
        .d(d),
        .y(y)
    );
endmodule
