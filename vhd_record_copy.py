#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
from npp_vhd_parser import RecordParser

record_parser = RecordParser()

if __name__ == "__main__":
    
    start = editor.getSelectionStart() 
    stop = editor.getSelectionEnd()
    if stop == start:
        # when nothing is selected, select all the text.
        input_text = editor.getText()
    else:
        input_text = editor.getTextRange(start, stop)

    console.clear()
    console.show()
    record_parser.parse(input_text)
    console.write(repr(record_parser))
    
    time.sleep(1)
    console.hide()
