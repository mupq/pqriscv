import argparse
import logging
import telnetlib
import os.path

from mupq import mupq
from mupq import platforms


def parse_arguments():
    parser = argparse.ArgumentParser(description="PQRISCV Specific Settings")
    parser.add_argument(
        "-p",
        "--platform",
        help="The PQM4 platform",
        choices=["pqvexriscvsim", "pqvexriscvsimhuge", "pqvexriscvarty"],
        default="pqvexriscvsim",
    )
    parser.add_argument(
        "-o",
        "--opt",
        help="Optimization flags",
        choices=["speed", "size", "debug"],
        default="size",
    )
    parser.add_argument(
        "-l", "--lto", help="Enable LTO flags", default=False, action="store_true"
    )
    parser.add_argument(
        "--no-aio", help="Disable all-in-one compilation", default=False, action="store_true"
    )
    parser.add_argument("-f", "--openocd", help="OpenOCD Script")
    parser.add_argument("-u", "--uart", help="Path to UART output")
    parser.add_argument("-i", "--iterations", default=1, help="Number of iterations for benchmarks")
    return parser.parse_known_args()


def get_platform(args):
    platform = None
    bin_type = 'bin'
    if args.platform in ["pqvexriscvsim", "pqvexriscvsimhuge", "pqvexriscvarty"]:
        platform = OpenOCDTelnet(tty=args.uart, baud=115200, timeout=None)
    else:
        raise NotImplementedError("Unsupported Platform")
    settings = RiscvSettings(args.platform, args.opt, args.lto, not args.no_aio, args.iterations, bin_type)
    return platform, settings


class RiscvSettings(mupq.PlatformSettings):
    #: Specify folders to include
    scheme_folders = [  # mupq.PlatformSettings.scheme_folders + [
        ('pqriscv', 'crypto_kem', ''),
        ('pqriscv', 'crypto_sign', ''),
        ('mupq', 'mupq/crypto_kem', ''),
        ('mupq', 'mupq/crypto_sign', ''),
        ('pqclean', 'mupq/pqclean/crypto_kem', "PQCLEAN"),
        ('pqclean', 'mupq/pqclean/crypto_sign', "PQCLEAN")
    ]

    size_executable = 'riscv64-unknown-elf-size'

    def __init__(self, platform, opt="speed", lto=False, aio=False, iterations=1, binary_type='bin'):
        """Initialize with a specific pqvexriscv platform"""
        super(RiscvSettings, self).__init__()
        self.skip_list = []
        # import skiplist
        # for impl in skiplist.skip_list:
        #     if impl['estmemory'] > self.platform_memory[platform]:
        #         impl = impl.copy()
        #         del impl['estmemory']
        #         self.skip_list.append(impl)
        # self.skip_list.append({'implementation': 'vec'})
        self.binary_type = binary_type
        optflags = {"speed": [], "size": ["OPT_SIZE=1"], "debug": ["DEBUG=1"]}
        if opt not in optflags:
            raise ValueError(f"Optimization flag should be in {list(optflags.keys())}")
        self.makeflags = [f"PLATFORM={platform}"]
        self.makeflags += [f"MUPQ_ITERATIONS={iterations}"]
        self.makeflags += optflags[opt]
        if lto:
            self.makeflags += ["LTO=1"]
        else:
            self.makeflags += ["LTO="]
        if aio:
            self.makeflags += ["AIO=1"]
        else:
            self.makeflags += ["AIO="]


class OpenOCDTelnet(platforms.SerialCommsPlatform):
    def __init__(self, load_addr=0x80000000, server="localhost", port=4444, tty="/dev/ttyACM0", baud=38400, timeout=60):
        super().__init__(tty, baud, timeout)
        self.load_addr = load_addr
        self.telnet = telnetlib.Telnet(server, port)

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        self.telnet.close()
        return super().__exit__(*args, **kwargs)

    def flash(self, binary_path):
        binary_path = os.path.abspath(binary_path)
        logging.info("Loading image...")
        self.telnet.write(b"reset halt\n")
        self.telnet.read_until(b"> ")
        self.telnet.write(f"load_image {binary_path} 0x{self.load_addr:08X}\n".encode("ascii"))
        self.telnet.read_until(b"> ")
        self.telnet.write(b"resume\n")
        self.telnet.read_until(b"> ")
        logging.info("Loaded image")
