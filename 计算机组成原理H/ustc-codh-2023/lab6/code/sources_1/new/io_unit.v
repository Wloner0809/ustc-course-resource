`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/06/08 14:36:50
// Design Name: 
// Module Name: io_unit
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


module io_unit(
    input clk,
    input cpu_clk,        //用sdu生成的cpu时钟
    input rstn,           //cpu_resetn
    input data,           //btnc
    input del,            //btnl
    input [15:0] x,       //sw15-0
    output reg [15:0] led,//led15-0
    output reg [7:0] an,
    output reg [6:0] seg,
    //IO_BUS
    input [7:0] io_addr,
    input [31:0] io_dout,
    input io_we,
    input io_rd,
    output reg [31:0] io_din
    );

    //数码管数据
    reg [31:0] seg_data;
    //数码管准备好
    reg seg_rdy;
    //数码管选择
    reg seg_sel;
    //开关输入有效
    reg swx_vld;
    //开关输入数据
    reg [31:0] swx_data;
    //计数器数据
    reg [31:0] cnt_data;
    //开关编码后的数据
    reg [3:0] x_hd_t;
    //临时编辑的数据
    reg [31:0] tmp;
    //显示的数据
    reg [31:0] disp_data;


    //PDU模块的一些代码
    reg [15:0] rstn_r;
    wire rst;               //复位信号，高电平有效
    assign rst = rstn_r[15];//经处理后的复位信号，高电平有效

    reg [19:0] cnt_clk_r;           //时钟分频、数码管刷新计数器
    wire clk_db;                    //去抖动计数器时钟
    assign clk_db = cnt_clk_r[16];  //去抖动计数器时钟763Hz（周期约1.3ms）

    wire pdu_clk;
    assign pdu_clk = cnt_clk_r[1];  //PDU工作时钟25MHz

    //开关
    reg [4:0] cnt_sw_db_r;
    reg [15:0] x_db_r, x_db_1r;
    reg xx_r, xx_1r;
    wire x_p;
    assign x_p = xx_r ^ xx_1r;

    //按钮
    wire [1:0] btn;
    assign btn ={data, del};
    reg [1:0] cnt_btn_db_r;
    reg [1:0] btn_db_r, btn_db_1r;
    wire data_p, del_p;
    assign data_p = btn_db_r[1] & ~ btn_db_1r[1];
    assign del_p = btn_db_r[0] & ~ btn_db_1r[0];


    ///////////////////////////////////////////////
    //复位处理：异步复位、同步和延迟释放
    ///////////////////////////////////////////////
    always @(posedge clk, negedge rstn) begin
        if (~rstn)
            rstn_r <= 16'hFFFF;
        else
            rstn_r <= {rstn_r[14:0], 1'b0};
    end
    ///////////////////////////////////////////////
    //时钟分频
    ///////////////////////////////////////////////
    always @(posedge clk, posedge rst) begin
        if (rst)
            cnt_clk_r <= 20'h0;
        else
            cnt_clk_r <= cnt_clk_r + 20'h1;
    end
    ///////////////////////////////////////////////
    //开关sw去抖动
    ///////////////////////////////////////////////
    always @(posedge clk_db, posedge rst) begin
        if (rst)
            cnt_sw_db_r <= 5'h0;
        else if ((|(x ^ x_db_r)) & (~ cnt_sw_db_r[4])) 
            cnt_sw_db_r <= cnt_sw_db_r + 5'h1;
        else
            cnt_sw_db_r <= 5'h0;
    end

    always@(posedge clk_db, posedge rst) begin
        if (rst) begin
            x_db_r <= x;
            x_db_1r <= x;
            xx_r <= 1'b0;
        end
        else if (cnt_sw_db_r[4]) begin    //信号稳定约21ms后输出
            x_db_r <= x;
            x_db_1r <= x_db_r;
            xx_r <= ~xx_r;
        end
    end

    always @(posedge pdu_clk, posedge rst) begin
        if (rst)
            xx_1r <= 1'b0;
        else
            xx_1r <= xx_r;
    end

    ///////////////////////////////////////////////
    //按钮btn去抖动
    ///////////////////////////////////////////////
    always @(posedge clk_db, posedge rst) begin
        if (rst)
            cnt_btn_db_r <= 2'h0;
        else if ((|(btn ^ btn_db_r)) & (~ cnt_btn_db_r[1]))
            cnt_btn_db_r <= cnt_btn_db_r + 2'h1;
        else
            cnt_btn_db_r <= 2'h0;
    end

    always@(posedge clk_db, posedge rst) begin  
        if (rst)
            btn_db_r <= btn;
        else if (cnt_btn_db_r[1])
            btn_db_r <= btn;
    end

    always @(posedge pdu_clk, posedge rst) begin   
        if (rst)
            btn_db_1r <= btn;
        else
            btn_db_1r <= btn_db_r;
    end




    ///////////////////////////////////////////////
    //CPU输入/输出
    ///////////////////////////////////////////////

    //CPU输出
    always @(posedge cpu_clk or negedge rstn) begin
        if(!rstn) begin
            led <= 16'hffff;
            seg_data <= 32'h12345678;
        end
        else if(io_we) begin
            if(io_addr == 8'h00)
                led <= io_dout[15:0];
            else if(io_addr == 8'h0c)
                seg_data <= io_dout;
        end
    end

    always @(posedge pdu_clk or negedge rstn) begin
        if(!rstn)
            seg_rdy <= 1;
        else if(io_we & (io_addr == 8'h0c))
            seg_rdy <= 0;
        else if(x_p | del_p)
            seg_rdy <= 1;   //这里不确定
    end

    //CPU输入
    always @(*) begin
        case (io_addr)
            8'h04:
                io_din = {14'h0, data, del, x};
            8'h08:
                io_din = {31'h0, seg_rdy};
            8'h10:
                io_din = {31'h0, swx_vld};
            8'h14:
                io_din = swx_data;
            8'h18:
                io_din = cnt_data;
            default: 
                io_din = 0;
        endcase
    end

    always @(posedge pdu_clk or negedge rstn) begin
        if(!rstn)
            swx_vld <= 0;
        else if(~swx_vld & data_p)
            swx_vld <= 1;
        else if(io_rd & (io_addr == 8'h14))
            swx_vld <= 0;
    end

    ///////////////////////////////////////////////
    //性能计数器
    ///////////////////////////////////////////////
    always@(posedge cpu_clk or negedge rstn) begin
        if(!rstn)
            cnt_data <= 32'h0;
        else 
            cnt_data <= cnt_data + 1;
    end
    
    ///////////////////////////////////////////////
    //开关编辑数据
    ///////////////////////////////////////////////
    always @* begin    //开关输入编码
        case (x_db_r ^ x_db_1r)
            16'h0001:
                x_hd_t = 4'h0;
            16'h0002:
                x_hd_t = 4'h1;
            16'h0004:
                x_hd_t = 4'h2;
            16'h0008:
                x_hd_t = 4'h3;
            16'h0010:
                x_hd_t = 4'h4;
            16'h0020:
                x_hd_t = 4'h5;
            16'h0040:
                x_hd_t = 4'h6;
            16'h0080:
                x_hd_t = 4'h7;
            16'h0100:
                x_hd_t = 4'h8;
            16'h0200:
                x_hd_t = 4'h9;
            16'h0400:
                x_hd_t = 4'hA;
            16'h0800:
                x_hd_t = 4'hB;
            16'h1000:
                x_hd_t = 4'hC;
            16'h2000:
                x_hd_t = 4'hD;
            16'h4000:
                x_hd_t = 4'hE;
            16'h8000:
                x_hd_t = 4'hF;
            default:
                x_hd_t = 4'h0;
        endcase
    end

    always @(posedge pdu_clk or negedge rstn) begin
        if(!rstn)
            tmp <= 0;
        else if(x_p)
            tmp <= {tmp[27:0], x_hd_t};
        else if(del_p)
            tmp <= {4'h0, tmp[31:4]};
        else if(~swx_vld & data_p)
            tmp <= 0;
    end



    always @(posedge pdu_clk or negedge rstn) begin
        if(!rstn)
            swx_data <= 0;
        else if(~swx_vld & data_p)
            swx_data <= tmp;
        else 
            swx_data <= swx_data;

    end

    ///////////////////////////////////////////////
    //数码管多用途显示
    ///////////////////////////////////////////////

    always @(posedge pdu_clk or negedge rstn) begin
        if(!rstn)
            seg_sel <= 0;
        else if(io_we & (io_addr == 8'h0c))
            seg_sel <= 1;
        else if(x_p | del_p)
            seg_sel <= 0;
    end

    always @(*) begin
        if(seg_sel)
            disp_data = seg_data;
        else    
            disp_data = tmp;
    end

    reg [3:0] hd_t;

    always @(*) begin          //数码管扫描
        an <= 8'b1111_1111;
        hd_t <= disp_data[3:0];
        if (&cnt_clk_r[16:15])    //降低亮度
        case (cnt_clk_r[19:17])   //刷新频率约为95Hz
            3'b000: begin
                an <= 8'b1111_1110;
                hd_t <= disp_data[3:0];
            end
            3'b001: begin
                an <= 8'b1111_1101;
                hd_t <= disp_data[7:4];
            end
            3'b010: begin
                an <= 8'b1111_1011;
                hd_t <= disp_data[11:8];
            end
            3'b011: begin
                an <= 8'b1111_0111;
                hd_t <= disp_data[15:12];
            end
            3'b100: begin
                an <= 8'b1110_1111;
                hd_t <= disp_data[19:16];
            end
            3'b101: begin
                an <= 8'b1101_1111;
                hd_t <= disp_data[23:20];
            end
            3'b110: begin
                an <= 8'b1011_1111;
                hd_t <= disp_data[27:24];
            end
            3'b111: begin
                an <= 8'b0111_1111;
                hd_t <= disp_data[31:28];
            end
            default:
                ;
        endcase
    end

    always @ (*) begin    //7段译码
        case(hd_t)
            4'b1111:
                seg = 7'b0111000;
            4'b1110:
                seg = 7'b0110000;
            4'b1101:
                seg = 7'b1000010;
            4'b1100:
                seg = 7'b0110001;
            4'b1011:
                seg = 7'b1100000;
            4'b1010:
                seg = 7'b0001000;
            4'b1001:
                seg = 7'b0001100;
            4'b1000:
                seg = 7'b0000000;
            4'b0111:
                seg = 7'b0001111;
            4'b0110:
                seg = 7'b0100000;
            4'b0101:
                seg = 7'b0100100;
            4'b0100:
                seg = 7'b1001100;
            4'b0011:
                seg = 7'b0000110;
            4'b0010:
                seg = 7'b0010010;
            4'b0001:
                seg = 7'b1001111;
            4'b0000:
                seg = 7'b0000001;
            default:
                seg = 7'b1111111;
        endcase
    end


endmodule
