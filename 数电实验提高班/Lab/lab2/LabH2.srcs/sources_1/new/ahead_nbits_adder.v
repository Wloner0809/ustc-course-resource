`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/16 18:30:46
// Design Name: 
// Module Name: ahead_nbits_adder
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


module ahead_nbits_adder #(parameter WIDTH=8)(
    input [WIDTH-1:0] a,b,
    input ci,
    output [WIDTH-1:0] s,
    output co
    );
    wire [WIDTH-1:0] G,P,C;
    assign P = a ^ b;   //Pi是ai和bi的异或
    assign G = a & b;   //Gi是ai和bi的与
    genvar i;
    assign C[0] = G[0] | (P[0] & ci);
    assign s[0] = P[0] ^ ci;
    generate
        for(i=1;i<WIDTH;i=i+1)begin:block
            assign C[i] = G[i] | (P[i] & C[i-1]);
            assign s[i] = P[i] ^ C[i-1];
        end
    endgenerate
    assign co=C[WIDTH-1];
endmodule
