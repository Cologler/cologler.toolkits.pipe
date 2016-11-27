#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import re

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

export_parser = AcdcliArgParser
