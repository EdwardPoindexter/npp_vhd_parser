#!/usr/bin/env python
#-*- coding: utf-8 -*-

from npp_vhd_parser import VhdParser

vhd_parser = VhdParser()

if __name__ == "__main__":
    
    start = editor.getSelectionStart() 
    stop = editor.getSelectionEnd()
    input_text = editor.getTextRange(start, stop)

    console.clear()
    console.show()
    vhd_parser.parse(input_text)
    console.write(repr(vhd_parser))
