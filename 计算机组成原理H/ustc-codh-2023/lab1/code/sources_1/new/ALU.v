`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/03/29 20:41:27
// Design Name: 
// Module Name: ALU
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


module ALU #(
    parameter WIDTH = 32
)(
    input [WIDTH-1:0] a,b,
    input [2:0] f,
    output reg [WIDTH-1:0] y,
    output reg [2:0] t   
);
    always @(*) begin
        if(f == 3'b000)begin
            y = a - b;
            //t需要根据运算结果来设置
            if(y == 0)begin
                t = 3'b001;
            end
            //下面时a!=b的情况
            else begin
                t[0] = 0;
                if(!a[WIDTH-1] && !b[WIDTH-1])begin
                    t[2] = y[WIDTH-1];
                    t[1] = y[WIDTH-1];
                end
                else if(!a[WIDTH-1] && b[WIDTH-1])begin
                    t[2] = 1;
                    t[1] = 0;
                end
                else if(a[WIDTH-1] && !b[WIDTH-1])begin
                    t[2] = 0;
                    t[1] = 1;
                end
                else begin
                    t[2] = y[WIDTH-1];
                    t[1] = y[WIDTH-1];
                end
            end
        end
        else if(f == 3'b001)begin
            y = a + b;
            t = 3'b000;
        end
        else if(f == 3'b010)begin
            y = a & b;
            t = 3'b000;
        end
        else if(f == 3'b011)begin
            y = a | b;
            t = 3'b000;
        end
        else if(f == 3'b100)begin
            y = a ^ b;
            t = 3'b000;
        end
        else if(f == 3'b101)begin
            y = a >> b;
            t = 3'b000;
        end
        else if(f == 3'b110)begin
            y = a << b;
            t = 3'b000;
        end
        else begin
            //verilog默认是无符号数
            //通过$signed()将其变为有符号数再算术右移
            y = $signed(a) >>> b;
            t = 3'b000;
        end
    end

endmodule
