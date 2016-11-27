#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import re
from ._common import ArgParser

class DirArgParser(ArgParser):
    RE_DATE = '(?:19|20)\\d{2}/(?:0\\d|1[0-2])/(?:[0-2]\\d|3[01])'
    RE_TIME = '(?:[01]\\d|2[0-3])\\:[0-5]\\d'
    RE_TYPE = '(?:   <DIR>         |[ ,\\d]{17})'
    RE_EXP  = '^%s  %s %s (.*)$' % (
        RE_DATE,
        RE_TIME,
        RE_TYPE,
    )
    REGEX = re.compile(RE_EXP)

    def __init__(self):
        super().__init__()

    def path(self, line):
        # 2016/03/19  22:13    <DIR>          XXX
        # 2015/07/20  03:41         2,217,217 XXX
        m = self.REGEX.match(line)
        ret = m.groups()[0] if m else None
        if ret in ['.', '..']:
            return None
        else:
            return ret

    def name(self, line):
        path = self.path(line)
        if path:
            return os.path.split(path)[1]

export_parser = DirArgParser
