#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import os
from npp_vhd_parser import RecordParser

if __name__ == "__main__":
    console.clear()
    console.show()
    console.write(repr(record_parser))
    console.write("paste as component")

    res = os.linesep
    res += record_parser.paste_as_init() + os.linesep
    res += record_parser.paste_as_constant_width() + os.linesep
    res += record_parser.paste_as_slv_to_record() + os.linesep
    res += record_parser.paste_as_record_to_slv() + os.linesep

    editor.addText(res)

    time.sleep(1)
    console.hide()
