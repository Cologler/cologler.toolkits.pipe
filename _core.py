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
import re
import importlib

class Executor:
    def execute(self, cmd_args: list):
        raise NotImplementedError

    def end(self):
        pass

def parser_factory(name):
    script_file = os.path.join(os.path.dirname(__file__), 'p', name + '.py')
    if os.path.isfile(script_file):
        sys.path.append(os.path.join(os.path.dirname(__file__), 'p'))
        module = importlib.import_module('p.' + name)
        return getattr(module, 'export_parser', None)
    return None

def resolve_line(factory, line, sbs, mbs):
    parser = factory()
    mbsc = mbs.copy()
    ces = []
    for i, mb in enumerate(mbsc):
        mbc = mb.copy()
        for j in range(0, len(mbc)):
            arg_name = mbc[j][1:-1].lower()
            pr = parser.parse(arg_name, line)
            if pr == None:
                return
            mbc[j] = pr
        for j in range(0, len(mbc)):
            mbc.insert(j * 2, sbs[i][j])
        mbc.append(sbs[i][-1])
        ces.append(''.join(mbc))
    return ces

def parse_cmd(factory, rawcmd):
    cmd = rawcmd.copy()
    regex = re.compile('\\{\\w+\\}')
    sbs = []
    mbs = []
    for block in cmd:
        sbs.append(regex.split(block))
        mbs.append(regex.findall(block))
    if len(mbs) == 0:
        print('[ERROR]', 'cannot find any argument in command.')
        return
    sps = []
    resolved_cmds = []
    for line in sys.stdin.read().splitlines():
        rcmd = resolve_line(factory, line, sbs, mbs)
        if rcmd:
            resolved_cmds.append(rcmd)
    return resolved_cmds

def execute_pipe(argv, executor: Executor):
    if sys.stdin.isatty():
        print('[ERROR]', 'no pipe input.')
        return
    if len(argv) < 3:
        print('[ERROR]', 'too less args.')
        return
    parser_name = argv[1]
    factory = parser_factory(parser_name)
    if factory is None:
        print('[ERROR]', 'unknown parser.')
        return
    rawcmd = argv[2:]
    resolved_cmds = parse_cmd(factory, rawcmd)
    if resolved_cmds:
        for cmd_args in resolved_cmds:
            executor.execute(cmd_args)
    executor.end()
