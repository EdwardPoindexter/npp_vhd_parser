#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
from npp_vhd_parser import VhdParser
entity_example='''
entity my_module is
    generic(
        my_freq_1     : positive ; -- rrr
        my_freq_2     : positive; -- rrr
        my_freq_3     : positive := 10; -- rrr
        my_val        : positive := 10 -- eeee
    );
    port(
        -- systeme
        clk                : in  std_logic; --module clock
        rstn               : in  std_logic; --low active asynchronous reset with deassertion synchronous to clk
        -- Triggers and events
        triggin_req_tgl    : in  std_logic; -- titi
        triggin_ack_tgl    : out std_logic; 
        my_vect            : out std_logic_vector(3 downto 1);
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
    print("paste as initializations")
    print(vhd_parser.paste_as_initializations(indent))
    print("paste as testbench")
    print(vhd_parser.paste_as_testbench(indent))
    print("paste as fake par")
    print(vhd_parser.paste_as_fake_par(indent))

