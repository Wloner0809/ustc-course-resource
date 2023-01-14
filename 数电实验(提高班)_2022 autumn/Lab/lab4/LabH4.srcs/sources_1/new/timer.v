`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2022/10/31 07:38:21
// Design Name: 
// Module Name: timer
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

module timer#(parameter k =100000000)(
    input [15:0] tc,
    input st,clk,rstn,
    output reg td,
    output  [6:0] cn,
    output  [7:0] an
    );

    wire st_now_1,st_now;
    reg [15:0] q;
    assign an[7:4] = 4'b1111;
    //ce当做计数使能信号
    reg ce;
    //count在这里用于计数
    reg [31:0] count;
    //st_pre用于记录前一个st的值
    reg  st_pre;


    Debounce Debounce_dut(
        .x(st),
        .clk(clk),
        .rstn(rstn),
        .y(st_now_1)
    );

    syn_ps syn_ps_dut(
        .a(st_now_1),
        .clk(clk),
        .rstn(rstn),
        .p(st_now)
    );

  always @(posedge clk or negedge rstn) begin
    if(!rstn)begin
        q <= 16'h0000;
        st_pre <= 1'b0;
    end
    else if(st_now)begin 
        q <= tc;
    end
    else if(ce && q > 16'h0000)begin
        q <= q - 16'h0001;
        st_pre <= 1'b0;
    end
    else begin
        q <= q; 
        st_pre <= 1'b0;
    end
  end
  
  always @(posedge clk or negedge rstn) begin
    if(!rstn)begin
        count <= k>>1 - 1;
    end
    //st_pre与st不相同时(也就是计数未到零st再次变高)需要对计数器重新计数
    else if(st_pre ^ st_now)
        count <= k>>1 - 1;
    else if(count == 32'h00000000)begin
        count <= k>>1 - 1;
    end
    else
        count <= count - 1;
  end

  always @(posedge clk or negedge rstn) begin
    if(!rstn)
        ce <= 1'b0;
    else if(count == 32'h00000000)
        ce <= ~ce;
    else 
        ce <= 1'b0;
  end


    //组合逻辑实现不会出现延迟
  always @(*) begin
    if(st) 
        td = 1'b0;
    else if(q == 16'h0000)
        td = 1'b1;
    else 
        td = 1'b0;
  end


    display_time display_time_dut(
        .d(q),
        .clk(clk),
        .rstn(rstn),
        .cn(cn),
        .an(an[3:0])
    );

endmodule
