#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import sys
import traceback

from _core import execute_pipe

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        execute_pipe(argv, True)
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()