`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/05/30 09:13:22
// Design Name: 
// Module Name: DCache
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


module DCache #(
    parameter OFFSET = 5,
    parameter CACHE_INDEX = 5,
    parameter ADDR_TAG = 2,
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 12,
    parameter BLOCK = 8
)(
    input clk,
    input rstn,
    input [ADDR_WIDTH-1 : 0] addr,  //读or写的地址
    input [31 : 0] din,             //要写入的数据，一次写入一个字
    input we_write,                 //写使能          
    input we_read,                  //读使能
    output [31 : 0] dout,           //读出的数据，一次读一个字
    output cache_miss,              //cache未命中信号
    //用于SDU交互的变量
    input [11 : 0] sdu_addr,
    output [31 : 0] sdu_data,
    //输出cache命中率
    output reg [31 : 0] cache_miss_cnt,
    output reg [31 : 0] cache_hit_cnt
);

    //cache状态机
    reg [1:0] CS;
    reg [1:0] NS;
    parameter IDLE = 2'b00,
              WRITE_MEM = 2'b01,
              WRITE_CACHE = 2'b10,
              WRITE_FINISH = 2'b11;

    //cache有关定义
    reg [DATA_WIDTH-1 : 0] cache_data [0 : (1 << (OFFSET + CACHE_INDEX)) - 1];  //cache存储数据
    reg [ADDR_TAG-1 : 0] cache_addr_tag [0 : (1 << CACHE_INDEX) - 1];
    reg valid [0 : (1 << CACHE_INDEX) - 1]; //valid有效位
    reg dirty [0 : (1 << CACHE_INDEX) - 1]; //dirty脏位
    wire [OFFSET-1 : 0] offset;
    wire [CACHE_INDEX-1 : 0] index;
    wire [ADDR_TAG-1 : 0] addr_tag;
    assign {addr_tag, index, offset} = addr;    //将输入的地址分为三部分
    reg cache_hit;  //cache命中

    //主存有关定义
    wire mem_ready; //主存输出的读写握手信号
    wire [(DATA_WIDTH << OFFSET) - 1 : 0] read_mem_data;    //读取主存中的一行数据
    reg [(DATA_WIDTH << OFFSET) - 1 : 0] write_mem_data;    //向主存中写入一行数据(dirty)
    reg [ADDR_WIDTH-1-OFFSET : 0] write_mem_addr;  //写入主存的地址，这里不需要offset，因为是一行一行写的
    reg [ADDR_WIDTH-1-OFFSET : 0] read_mem_addr;  //读取主存的地址，这里不需要offset，因为是一行一行读的


    always @(*) begin
        if(valid[index] && (cache_addr_tag[index] == addr_tag) && (we_read | we_write))
            cache_hit = 1'b1;
        else
            cache_hit = 1'b0;
    end

    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            CS <= IDLE;
        else    
            CS <= NS;
    end

    always @(*) begin
        if(CS == IDLE) begin
            if(cache_hit)
                NS = IDLE;
            else if((we_read | we_write) && (valid[index] && dirty[index]))
                NS = WRITE_MEM;
            else if((!valid[index] || !dirty[index]) && (we_read | we_write))
                NS = WRITE_CACHE; 
            else
                NS = IDLE;
        end
        else if(CS == WRITE_MEM) begin
            NS = mem_ready ? WRITE_CACHE : WRITE_MEM;
        end
        else if(CS == WRITE_CACHE) begin
            NS = mem_ready ? WRITE_FINISH : WRITE_CACHE;
        end
        else begin
            NS = IDLE;
        end
    end

    //输出数据
    //异步读数据，模拟分布式存储器
    assign dout = (CS === IDLE && cache_hit && we_read) ? {cache_data[(index << OFFSET) + offset], cache_data[(index << OFFSET) + offset + 1],cache_data[(index << OFFSET) + offset + 2], cache_data[(index << OFFSET) + offset + 3]} : 0;

    integer i, j ,k, m;
    always @(posedge clk or negedge rstn) begin
        if(!rstn) begin
            //初始化valid和dirty
            for (i = 0; i < (1 << CACHE_INDEX); i = i + 1) begin
                valid[i] <= 0;
                dirty[i] <= 0;
            end
            //初始化向主存中写入的数据
            write_mem_data <= 0;
            //初始化向主存写入的地址
            write_mem_addr <= 0;
            //初始化从主存读数据的地址
            read_mem_addr <= 0;
            //初始化读出的数据
            //dout <= 0;
        end
        else begin
            case(CS)
                IDLE: begin
                    if(cache_hit) begin
                        //cache命中
                        if(we_read) begin
                            //读请求
                            //dout <= {cache_data[(index << OFFSET) + offset], cache_data[(index << OFFSET) + offset + 1],cache_data[(index << OFFSET) + offset + 2], cache_data[(index << OFFSET) + offset + 3]};
                        end
                        else if(we_write)begin
                            //写请求
                            {cache_data[(index << OFFSET) + offset], cache_data[(index << OFFSET) + offset + 1],cache_data[(index << OFFSET) + offset + 2], cache_data[(index << OFFSET) + offset + 3]} <= din;
                            dirty[index] <= 1;
                        end
                    end
                    else begin
                        //cache未命中
                        if(we_read || we_write) begin
                            //如果有读写请求        
                            if(valid[index] && dirty[index]) begin
                                //换入的那一行有效且脏
                                //此时需要写入主存
                                write_mem_addr <= {cache_addr_tag[index], index};
                                for(k = 0; k < (1 << OFFSET); k = k + 1) begin
                                    write_mem_data[((k + 1) * DATA_WIDTH - 1)-:DATA_WIDTH] <= cache_data[(index << OFFSET) + k];
                                end
                            end
                            //记录要写入cache的主存那一行的地址有关信息
                            //同时为了更新cache
                            read_mem_addr <= {addr_tag, index};
                        end
                    end
                end
                WRITE_FINISH: begin
                    //该状态用于写入cache数据
                    for(m = 0; m < (1 << OFFSET); m = m + 1) begin
                        cache_data[(read_mem_addr[CACHE_INDEX-1 : 0] << OFFSET) + m] <= read_mem_data[((m + 1) * DATA_WIDTH - 1)-:DATA_WIDTH];
                    end
                    
                    //更新tag
                    cache_addr_tag[index] <= read_mem_addr[ADDR_WIDTH-1-OFFSET : CACHE_INDEX];
                    //更新valid、dirty
                    valid[read_mem_addr[CACHE_INDEX-1 : 0]] <= 1;
                    dirty[read_mem_addr[CACHE_INDEX-1 : 0]] <= 0;
                end
            endcase
        end
    end


    wire we_read_data_memory;
    assign we_read_data_memory = (CS === WRITE_CACHE) ? 1 : 0;
    wire we_write_data_memory;
    assign we_write_data_memory = (CS === WRITE_MEM) ? 1 : 0;
    wire [CACHE_INDEX+ADDR_TAG-1 : 0] mem_addr;
    assign mem_addr = we_read_data_memory ? read_mem_addr : (we_write_data_memory ? write_mem_addr : 0);

    main_data_memory main_data_memory_dut(
        .clk(clk),
        .rstn(rstn),
        .we_read(we_read_data_memory),
        .we_write(we_write_data_memory),
        .addr(mem_addr),
        .write_mem(write_mem_data),
        .read_mem_line(read_mem_data),
        .ready(mem_ready),
        .sdu_addr(sdu_addr),
        .sdu_data(sdu_data)
    );

    assign cache_miss = (we_read | we_write) & (~cache_hit | CS != IDLE);

    //统计cache的命中率
    //需要对cache_miss取边沿
    reg pre_cache_miss;
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            pre_cache_miss <= 0;
        else
            pre_cache_miss <= cache_miss;
    end
    //对未命中的统计
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            cache_miss_cnt <= 0;
        else if(~pre_cache_miss & cache_miss)
            cache_miss_cnt <= cache_miss_cnt + 1;
        else    
            cache_miss_cnt <= cache_miss_cnt;
    end
    always @(posedge clk or negedge rstn) begin
        if(!rstn)
            cache_hit_cnt <= 0;
        else if(cache_hit)
            cache_hit_cnt <= cache_hit_cnt + 1;
        else 
            cache_hit_cnt <= cache_hit_cnt;
    end

endmodule
