#!/usr/bin/env python3
"""
Builds all of the binaries without flashing them.
"""

from interface import *
from mupq import mupq

import sys

if __name__ == "__main__":
    args, rest = parse_arguments()
    platform, settings = get_platform(args)
    mupq.BuildAll(settings).test_all(rest)
