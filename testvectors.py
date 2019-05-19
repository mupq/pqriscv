#!/usr/bin/env python3
from mupq import mupq
from interface import VexRiscvSettings, VexRiscv

import sys

if __name__ == "__main__":
    with VexRiscv() as riscv:
        test = mupq.TestVectors(VexRiscvSettings(), riscv)
        test.test_all(sys.argv[1:])
