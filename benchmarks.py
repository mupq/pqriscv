#!/usr/bin/env python3
from mupq import mupq
from interface import VexRiscvSettings, VexRiscv

import sys

if __name__ == "__main__":
    with VexRiscv() as riscv:
        if "--nostack" not in sys.argv:
            test = mupq.StackBenchmark(VexRiscvSettings(), riscv)
            test.test_all(sys.argv[1:])

        if "--nospeed" not in sys.argv:
            test = mupq.SpeedBenchmark(VexRiscvSettings(), riscv)
            test.test_all(sys.argv[1:])

        if "--nohashing" not in sys.argv:
            test = mupq.HashingBenchmark(VexRiscvSettings(), riscv)
            test.test_all(sys.argv[1:])

        if "--nosize" not in sys.argv:
            test = mupq.SizeBenchmark(VexRiscvSettings(), riscv)
            test.test_all(sys.argv[1:])

