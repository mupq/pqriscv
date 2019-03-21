#!/usr/bin/env python3
from mupq import mupq
from interface import RISCVSettings, RISCV


if __name__ == "__main__":
    riscv = RISCV()
    test = mupq.StackBenchmark(RISCVSettings(), riscv)
    test.test_all()

    test = mupq.SpeedBenchmark(RISCVSettings(), riscv)
    test.test_all()

