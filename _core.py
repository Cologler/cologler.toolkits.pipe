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
import subprocess

from jasily import switch

class ArgParser:
    def __init__(self):
        self._available_args = {}
        for attr in [z for z in dir(self) if not z.startswith('_')]:
            if attr != 'parse':
                self._available_args[attr] = getattr(self, attr)
    
    def parse(self, arg_name, line):
        func = self._available_args.get(arg_name)
        return func(line) if func else None

class DefaultArgParser(ArgParser):
    def line(self, line):
        return line

class DirArgParser(ArgParser):
    def __init__(self):
        super().__init__()
        re_date = '(?:19|20)\\d{2}/(?:0\\d|1[0-2])/(?:[0-2]\\d|3[01])'
        re_time = '(?:[01]\\d|2[0-3])\\:[0-5]\\d'
        re_type = '(?:   <DIR>         |[ ,\\d]{17})'
        re_exp  = '^%s  %s %s (.*)$' % (
            re_date,
            re_time,
            re_type,
        )
        self._regex = re.compile(re_exp)

    def path(self, line):
        # 2016/03/19  22:13    <DIR>          XXX
        # 2015/07/20  03:41         2,217,217 XXX
        m = self._regex.match(line)
        ret = m.groups()[0] if m else None
        if ret in ['.', '..']:
            return None
        else:
            return ret

    def name(self, line):
        path = self.path(line)
        if path:
            return os.path.split(path)[1]

class AcdcliArgParser(ArgParser):
    def __init__(self):
        super().__init__()
        self._regex = re.compile('^\\[([^ ]+)\\] \\[[^\\]]*\\] (.+)$')

    def id(self, line):
        # [id] [A] path
        m = self._regex.match(line)
        if m == None:
            print('None')
            return None
        else:
            return m.groups()[0]

    def path(self, line):
        # [id] [A] path
        m = self._regex.match(line)
        if m == None:
            return None
        else:
            return m.groups()[1]

def create_parser(name):
    for case in switch(name):
        if case('def'):
            return DefaultArgParser()
        elif case('dir'):
            return DirArgParser()
        elif case('acdcli'):
            return AcdcliArgParser()
    return None

def exec_line(parser_name, line, sbs, mbs, use_thread_pool: bool):
    parser = create_parser(parser_name)
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
    if use_thread_pool:
        return subprocess.Popen(ces)
    else:
        subprocess.call(ces)

def parse_cmd(parser_name, rawcmd, use_thread_pool: bool):
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
    for line in sys.stdin.read().splitlines():
        sp = exec_line(parser_name, line, sbs, mbs, use_thread_pool)
        if sp != None:
            sps.append(sp)
    for sp in sps:
        sp.wait()

def execute_pipe(argv, use_thread_pool: bool):
    if sys.stdin.isatty():
        print('[ERROR]', 'no pipe input.')
        return
    if len(argv) < 3:
        print('[ERROR]', 'too less args.')
        return
    parser_name = argv[1]
    if create_parser(parser_name) == None:
        print('[ERROR]', 'unknown parser.')
        return
    rawcmd = argv[2:]
    parse_cmd(parser_name, rawcmd, use_thread_pool)