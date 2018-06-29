#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import time
from npp_vhd_parser import VhdParser


if __name__ == "__main__":

    console.clear()
    console.show()
    console.write(repr(vhd_parser))
    console.write("paste as entity")
    
    res = os.linesep
    res += vhd_parser.paste_as_entity()
    editor.addText(res)

    time.sleep(1)
    console.hide()
