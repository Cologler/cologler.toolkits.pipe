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

export_parser = DirArgParser
