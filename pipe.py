#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback

from _core import execute_pipe
from _core import Executor

class SystemExecutor(Executor):
    def execute(self, cmd_args: list):
        cmd = cmd_args[0]
        args = ['"' + x + '"' for x in cmd_args[1:]]
        os.system(cmd + ' ' + ' '.join(args))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        execute_pipe(argv, SystemExecutor())
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()