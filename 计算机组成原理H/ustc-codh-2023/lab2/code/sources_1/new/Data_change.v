`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/08 08:55:44
// Design Name: 
// Module Name: Data_change
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


module Data_change(
    input [31:0] data1, data2,
    input clk,
    input [3:0] NS,
    output reg cmp,
    output reg [31:0] d
    );

    always @(posedge clk) begin
        if(data1 > data2)begin
            cmp <= 1;
            if(NS == 4'b0100)
                d <= data2;
            else if(NS == 4'b0101)
                d <= data1;
            else 
                d <= d;
        end
        else begin
            cmp <= 0;
        end
    end
endmodule
