#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from ._common import ArgParser

class PathArgParser(ArgParser):
    def parent(self, line):
        return os.path.dirname(line)

export_parser = PathArgParser
