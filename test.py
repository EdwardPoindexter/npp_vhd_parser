#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
from npp_vhd_parser import VhdParser
entity_example='''
entity my_module is
    generic(
        my_freq       : positive := 10; -- rrr
        my_val        : positive := 10 -- eeee
    );
    port(
        -- systeme
        clk                : in  std_logic; --module clock
        rstn               : in  std_logic; --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl    : in  std_logic; -- titi
        triggin_ack_tgl    : out std_logic; 
        triggout_req_tgl   : out std_logic  -- tata
    );
end my_module;
'''


vhd_parser = VhdParser()

if __name__ == "__main__":

    # get the selected text
    # input_text = editor.getSelText()
    input_text = entity_example

    vhd_parser.parse(input_text)
    indent = 4
    print("paste as entity")
    print(vhd_parser.paste_as_entity(indent))
    print("paste as instance")
    print(vhd_parser.paste_as_instance(indent))
    print("paste as component")
    print(vhd_parser.paste_as_component(indent))
    print("paste as signal")
    print(vhd_parser.paste_as_signal(indent))