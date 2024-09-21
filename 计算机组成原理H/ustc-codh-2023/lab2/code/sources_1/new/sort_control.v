`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/04/05 20:42:40
// Design Name: 
// Module Name: sort_control
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


module sort_control(
    input clk, rstn, run, cmp,  //cmp用于判断是否需要交换
    input [31:0] num,           //数组大小
    output reg [15:0] cycles,
    output reg done, we,
    output reg [2:0] sel,       //用于地址的更替(Addr_change.v)
    output [3:0] next_state     //用于s4、s5状态写数据(Data_change.v)
    );

    parameter s0 = 4'b0000,
              s1 = 4'b0001,
              s2 = 4'b0010,
              s3 = 4'b0011,
              s4 = 4'b0100,
              s5 = 4'b0101,
              s6 = 4'b0110,
              s7 = 4'b0111,
              s8 = 4'b1000,
              s9 = 4'b1001,
              s10 = 4'b1010;
    reg [3:0] CS, NS;
    reg [31:0] cycle_external, cycle_internal;   //外层循环、内层循环

    assign next_state = NS;

    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            CS <= s8;
        else
            CS <= NS;
    end

    always @(*) begin
        if(run)begin
            if(CS == s0)
                NS = s1;
            else if(CS == s1)begin
                if(cycle_external > 0)
                    NS = s2;
                else    
                    NS = s7;    //退出循环
            end
            else if(CS == s2)begin
                if(cycle_internal > 0)
                    NS = s3;
                else    
                    NS = s1; 
            end
            else if(CS == s3)begin
                if(cmp)
                    NS = s4;
                else
                    NS = s6;     
            end
            else if(CS == s4)
                NS = s5;
            else if(CS == s5)
                NS = s6;
            else if(CS == s6)
                NS = s2;
            else if(CS == s8)
                NS = s9;
            else if(CS == s9)
                NS = s10;
            else if(CS == s10)
                NS = s0;
            else    
                NS = s7;

            //这一版本总是有latch生成
            //上板的结果不对

            // case(CS)
            //     s0: NS = s1;
            //     s1: begin
            //         if(cycle_external > 0)
            //             NS = s2;
            //         else    
            //             NS = s7;    //退出循环
            //     end
            //     s2: begin
            //         if(cycle_internal > 0)
            //             NS = s3;
            //         else    
            //             NS = s1; 
            //     end
            //     s3: begin
            //         if(cmp)
            //             NS = s4;
            //         else
            //             NS = s6; 
            //     end
            //     s4: NS = s5;
            //     s5: NS = s6;
            //     s6: NS = s2;
            //     s7: ;
            //     s8: NS = s9;
            //     s9: NS = s10;
            //     s10: NS = s0;
            //     default: NS = s7;                    
            // endcase
        end
        else
            NS = s8;
    end

    always @(posedge clk or negedge rstn) begin
        if(!rstn)begin
            cycles <= 16'h0000;
            done <= 1'b0;
            cycle_external <= num;
            cycle_internal <= 0;    
            we <= 0;
            sel <= 3'b100;
        end
        else if(run)begin
            case(NS)
                s10: ;
                s9: ;
                s8: ;
                s0: begin
                    cycle_external <= num;
                    cycle_internal <= 0;
                    we <= 0;
                    sel <= 3'b100;
                    cycles <= 16'h0000;
                    done <= 1'b0;
                end
                s1: begin
                    cycle_external <= cycle_external - 1;
                    cycle_internal <= cycle_external - 1;
                    sel <= 3'b000;
                    cycles <= cycles + 1;
                end
                s2: begin
                    sel <= 3'b001;
                    cycles <= cycles + 1;
                end
                s3: begin
                    cycles <= cycles + 1;
                end
                s4: begin
                    cycles <= cycles + 1;
                    we <= 1;
                    sel <= 3'b011;
                end
                s5: begin
                    cycles <= cycles + 1;
                end
                s6: begin
                    cycle_internal <= cycle_internal - 1;
                    cycles <= cycles + 1;
                    we <= 0;
                    sel <= 3'b010;
                end
                s7: begin
                    sel <= 3'b001;
                    done <= 1'b1;
                end
            endcase
        end
        else begin
            cycles <= cycles;
            done <= done;
            cycle_external <= cycle_external;
            cycle_internal <= cycle_internal;
        end
    end

endmodule
