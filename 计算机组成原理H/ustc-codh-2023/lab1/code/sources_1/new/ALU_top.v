`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/01 18:49:28
// Design Name: 
// Module Name: ALU_top
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


module ALU_top(
    input [15:0] sw,
    input en, clk, rstn,
    output [7:0] an,
    output [6:0] cn,
    output reg [2:0] t
    );

    reg [31:0] a, b;
    wire [31:0] y;
    reg [31:0] y_temp;
    reg [2:0] f;
    wire [2:0] t_temp;
    wire [15:0] sw_temp;
    wire en_temp0, en_temp;

    parameter s0 = 3'b000, 
              s1 = 3'b001,
              s2 = 3'b010,
              s3 = 3'b011,
              s4 = 3'b100,
              s5 = 3'b101;
    reg [2:0] CS, NS;


    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            CS <= s0;
        else    
            CS <= NS;
    end

    always @(posedge clk or negedge rstn) begin
        if(!rstn)begin
            a <= 32'h0;
            b <= 32'h0;
            f <= 3'b0;
            NS <= s0;
            y_temp <= 32'h0;
            t <= 3'h0;
        end
        else if(en_temp)begin
            case(CS)
            s0:begin
                NS <= s1;
                a[15:0] <= sw_temp;
            end 
            s1:begin
                NS <= s2;
                a[31:16] <= sw_temp;
            end
            s2:begin
                NS <= s3;
                b[15:0] <= sw_temp;
            end
            s3:begin
                NS <= s4;
                b[31:16] <= sw_temp;
            end
            s4:begin
                NS <= s5;
                f <= sw_temp[2:0];
            end
            s5:begin
                NS <= s0;
                y_temp <= y;
                t <= t_temp;
            end
            endcase
        end
        else begin
            a <= a;
            b <= b;
            f <= f;
            NS <= NS;
            y_temp <= y_temp;
            t <= t;
        end
    end


    ALU ALU_dut(
        .a(a),
        .b(b),
        .f(f),
        .y(y),
        .t(t_temp)
    );

    genvar i;
    generate
        for(i = 0; i < 16; i = i + 1)
        begin:block
            Debounce Debounce_dut(
                .x(sw[i]),
                .y(sw_temp[i]),
                .clk(clk),
                .rstn(rstn)
            );
        end
    endgenerate

    Debounce Debounce_dut1(
        .x(en),
        .y(en_temp0),
        .clk(clk),
        .rstn(rstn)
    );

    syn_ps syn_ps_dut(
        .a(en_temp0),
        .p(en_temp),
        .clk(clk),
        .rstn(rstn)
    );

    Display Display_dut(
        .d(y_temp),
        .clk(clk),
        .rstn(rstn),
        .an(an),
        .cn(cn)
    );

endmodule
