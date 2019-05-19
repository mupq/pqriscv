#!/usr/bin/env python3
"""
Builds all of the binaries without flashing them.
"""

from interface import VexRiscvSettings
from mupq import mupq

import sys

if __name__ == "__main__":
    mupq.BuildAll(VexRiscvSettings()).test_all(sys.argv[1:])
