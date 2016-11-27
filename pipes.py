#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import traceback
import subprocess

from _core import execute_pipe
from _core import Executor


class SubProcessExecutor(Executor):
    def __init__(self):
        self._sps = []

    def execute(self, cmd_args: list):
        subprocess.call(cmd_args)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        execute_pipe(argv, SubProcessExecutor())
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
