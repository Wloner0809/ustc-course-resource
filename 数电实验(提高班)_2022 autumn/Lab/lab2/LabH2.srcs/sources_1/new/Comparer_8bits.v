`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/15 18:23:34
// Design Name: 
// Module Name: Comparer_8bits
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


module Comparer_8bits(
    input [7:0] a,b,
    output reg ug,ul,sg,sl
    );
    wire [7:0] sum;
    wire c;
    integer i;
    //利用8位超前进位加法器实现a-b
    ahead_nbits_adder #(.WIDTH(8)) ahead_8bits_adder_dut(
        .a(a),
        .b(~b),
        .ci(1),
        .s(sum),
        .co(c)
    );
  always @(*) begin
    ug=0;
    ul=0;
    sg=0;
    sl=0;
    //c的非是无符号数相减结果的符号位
    if(!c) begin
        ug=0;
        ul=1;
    end
    else begin
        for(i=0;i<8;i=i+1)begin
            if(sum[i]) begin
                ug=1;
                ul=0;
            end
        end
    end
    //这之后用来判断有符号数的大小
    //首先看符号位是否相同，若不相同直接出结果
    //若相同则相减之后的结果不会产生溢出，直接判断sum中的结果即可
    if(a[7]&&!b[7]) begin
        sg=0;
        sl=1;
    end
    else if(!a[7]&&b[7]) begin
        sg=1;
        sl=0;
    end
    else begin
        if(sum[7]) begin
            sg=0;
            sl=1;
        end
        else begin  
            for(i=6;i>=0;i=i-1)begin
            if(sum[i]) begin
                sg=1;
                sl=0;
            end
        end
        end
    end
  end
endmodule
