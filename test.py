#!/usr/bin/env python3
from mupq import mupq
from interface import *

import sys

if __name__ == "__main__":
    args, rest = parse_arguments()
    riscv, settings = get_platform(args)
    with riscv:
        test = mupq.SimpleTest(settings, riscv)
        test.test_all(rest)
