`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/31 15:16:03
// Design Name: 
// Module Name: main_data_memory
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


module main_data_memory #(
    parameter ADDR = 7,
    parameter DATA = 8,
    parameter LINE_BYTE = 32,
    parameter DELAY = 16
)(
    input clk,
    input rstn,
    input we_read,
    input we_write,
    input [ADDR-1 : 0] addr,
    input [(DATA << 5) - 1 : 0] write_mem,
    output reg [(DATA << 5) - 1 : 0] read_mem_line,
    output ready,   //握手信号
    //用于与SDU交互
    input [11 : 0] sdu_addr,
    output [31 : 0] sdu_data
);

    localparam READ_CYCLE = DELAY + (LINE_BYTE >> 2);
    localparam WRITE_CYCLE = DELAY + (LINE_BYTE >> 2);

    reg [4 : 0] read_cnt;   
    reg [4 : 0] write_cnt;
    wire read_finish;
    wire write_finish;
    reg [9 : 0] data_mem_addr; //访问的主存地址
    reg [31 : 0] data_mem_din;
    wire [31 : 0] data_mem_dout;
    reg [31 : 0] read_buffer [0 : (LINE_BYTE >> 2) - 1];
    reg we;

    assign read_finish = (read_cnt >= READ_CYCLE);
    assign write_finish = (write_cnt >= WRITE_CYCLE);

    Data_memory Data_memory_dut(
        .clka(clk),
        .addra(data_mem_addr),
        .dina(data_mem_din),
        .wea(we),
        .douta(data_mem_dout)
    );

    //解决SDU的问题
    reg [31 : 0] sdu_data_mem [0 : 1023];
    always @(posedge clk) begin
        if(we) begin
            sdu_data_mem[data_mem_addr] <= data_mem_din;
        end
    end
    assign sdu_data = sdu_data_mem[sdu_addr[9 : 0]];


    always @(posedge clk or negedge rstn) begin
        if(!rstn) begin
            data_mem_addr <= 0;
            data_mem_din <= 0;
            we <= 0;
            read_cnt <= 0;
            write_cnt <= 0;
        end
        else begin
            data_mem_addr <= {addr, 3'b0};
            data_mem_din <= 0;
            we <= 0;
            if(we_read) begin
                write_cnt <= 0;
                if(read_finish) begin
                    read_cnt <= 0;
                end
                else begin
                    if(read_cnt < DELAY) begin
                        if((read_cnt <= (LINE_BYTE >> 2)) && read_cnt > 0) begin
                            data_mem_addr <= (addr << 3) + (read_cnt - 1);
                        end
                        if(read_cnt > 3 && read_cnt < 12) begin
                            read_buffer[read_cnt-4] <= data_mem_dout;
                        end
                    end
                    else begin
                        //每次读出一个字
                        //首字延迟16个clks
                        // read_mem_line[(32*(read_cnt-DELAY) + 31)-:32] <=read_buffer[read_cnt-DELAY];
                        read_mem_line[(32*(read_cnt-DELAY) + DATA - 1)-:8] <= read_buffer[read_cnt-DELAY][31:24];
                        read_mem_line[(32*(read_cnt-DELAY) + 2*DATA - 1)-:8] <= read_buffer[read_cnt-DELAY][23:16];
                        read_mem_line[(32*(read_cnt-DELAY) + 3*DATA - 1)-:8] <= read_buffer[read_cnt-DELAY][15:8];
                        read_mem_line[(32*(read_cnt-DELAY) + 4*DATA - 1)-:8] <= read_buffer[read_cnt-DELAY][7:0];
                    end
                    read_cnt <= read_cnt + 1;
                end
            end
            else if(we_write) begin
                read_cnt <= 0;
                if(write_finish) begin
                    write_cnt <= 0;
                end
                else begin
                    if(write_cnt >= DELAY) begin
                        data_mem_addr <= (addr << 3) + (write_cnt - DELAY);
                        we <= 1;
                        data_mem_din[7:0] <= write_mem[(32*(write_cnt-DELAY) + 4*DATA - 1)-:8];
                        data_mem_din[15:8] <= write_mem[(32*(write_cnt-DELAY) + 3*DATA - 1)-:8];
                        data_mem_din[23:16] <= write_mem[(32*(write_cnt-DELAY) + 2*DATA - 1)-:8];
                        data_mem_din[31:24] <= write_mem[(32*(write_cnt-DELAY) + DATA - 1)-:8];
                    end
                end 
                write_cnt <= write_cnt + 1;
            end
        end
    end

    assign ready = ((we_write && write_finish) || (we_read && read_finish) === 1) ? 1 : 0; 


endmodule
