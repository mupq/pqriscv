#!/usr/bin/env python3
"""
Builds all of the binaries without flashing them.
"""

from interface import MuraxSettings
from mupq import mupq

if __name__ == "__main__":
    mupq.BuildAll(MuraxSettings()).test_all()
