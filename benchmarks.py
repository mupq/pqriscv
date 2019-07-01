#!/usr/bin/env python3
from mupq import mupq
from interface import *

import sys

if __name__ == "__main__":
    args, rest = parse_arguments()
    riscv, settings = get_platform(args)
    with riscv:
        if "--nostack" not in sys.argv:
            test = mupq.StackBenchmark(settings, riscv)
            test.test_all(rest)

        if "--nospeed" not in sys.argv:
            test = mupq.SpeedBenchmark(settings, riscv)
            test.test_all(rest)

        if "--nohashing" not in sys.argv:
            test = mupq.HashingBenchmark(settings, riscv)
            test.test_all(rest)

        # if "--nosize" not in sys.argv:
        #     test = mupq.SizeBenchmark(settings, riscv)
        #     test.test_all(rest)
