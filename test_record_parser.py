#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
from npp_vhd_parser import RecordParser
txt_example ='''
    
    type t_toto is record
        frame_command_valid            : std_logic;
        frame_command_flush            : std_logic;
        frame_done_counter_ack         : std_logic_vector( 7 downto 0);
        enable_it                      : std_logic;
        clear_it                       : std_logic;
        low_latency_mode               : std_logic;
        max_burst_length               : std_logic_vector( 7 downto 0);
        color_space                    : std_logic_vector( 1 downto 0);
        mapping                        : std_logic_vector( 1 downto 0);
        bitdepth                       : std_logic_vector( 1 downto 0);
        frame_width                    : std_logic_vector(12 downto 0);
        frame_height                   : std_logic_vector(12 downto 0);
        axi4_word_in_line_yuv_y        : std_logic_vector( 9 downto 0);
        axi4_word_in_line_uv_u_v       : std_logic_vector( 9 downto 0);
        buffer_start_address_r_y       : std_logic_vector(31 downto 0);
        buffer_start_address_g_u       : std_logic_vector(31 downto 0);
        buffer_start_address_b_v       : std_logic_vector(31 downto 0);
        buffer_line_stride_luma        : std_logic_vector(31 downto 0);
        buffer_line_stride_chroma      : std_logic_vector(31 downto 0);
        fifo_pix_y_clr_ovfl            : std_logic;
        fifo_pix_y_clr_udfl            : std_logic;
        fifo_pix_uv_clr_ovfl           : std_logic;
        fifo_pix_uv_clr_udfl           : std_logic;
        fifo_pix_u_clr_ovfl            : std_logic;
        fifo_pix_u_clr_udfl            : std_logic;
        fifo_pix_v_clr_ovfl            : std_logic;
        fifo_pix_v_clr_udfl            : std_logic;
    end record;  
'''


record_parser = RecordParser()

if __name__ == "__main__":

    # get the selected text
    # input_text = editor.getSelText()
    input_text = txt_example

    record_parser.parse(input_text)
    
    print(record_parser.paste_as_init())
    print(record_parser.paste_as_constant_width())
    print(record_parser.paste_as_slv_to_record())
    print(record_parser.paste_as_record_to_slv())
    print(repr(record_parser))
