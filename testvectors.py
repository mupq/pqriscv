#!/usr/bin/env python3
from mupq import mupq
from interface import RISCVSettings, RISCV

if __name__ == "__main__":
    test = mupq.TestVectors(RISCVSettings(), RISCV())
    test.test_all()

