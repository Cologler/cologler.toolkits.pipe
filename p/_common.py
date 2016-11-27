#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os

class ArgParser:
    def __init__(self):
        self._available_args = {}
        for attr in [z for z in dir(self) if not z.startswith('_')]:
            if attr != 'parse':
                self._available_args[attr] = getattr(self, attr)

    def parse(self, arg_name, line):
        func = self._available_args.get(arg_name)
        return func(line) if func else None

    def line(self, line):
        return line
