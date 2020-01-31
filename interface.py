import argparse
import serial
import subprocess
import time
from mupq import mupq

PQRISCV_PLATFORMS = 'vexriscv'

def parse_arguments():
    parser = argparse.ArgumentParser(description='pqriscv specific settings')
    parser.add_argument('-d', '--debug', help='Enable debug flags', default=False, action='store_true')
    parser.add_argument('-p', '--platform', help='The pqriscv platform', choices=['vexriscv'], default='vexriscv')
    parser.add_argument('-s', '--sub-platform', help='The platform subtype', default='pqvexriscvup5k')
    parser.add_argument('--openocd-script', help='OpenOCD script to connect')
    parser.add_argument('-u', '--uart', help='Path to UART output')
    return parser.parse_known_args()

def get_platform(args):
    # NOTE: Add new platforms with an elif args.platform == 'XYZ':...
    if args.platform == 'vexriscv':
        settings = VexRiscvSettings(args.sub_platform, args.debug)
        platform = VexRiscv(args.sub_platform, args.openocd_script, args.uart)
    else:
        raise ValueError('Unknown pqriscv platform')
    return platform, settings

class VexRiscvSettings(mupq.PlatformSettings):
    PQVEXRISCV_PLATFORMS = ['murax', 'pqvexriscvup5k', 'pqvexriscvsim', 'pqvexriscvsimhuge', 'pqvexriscvicoboard']
    #: Specify folders to include
    scheme_folders = [  # mupq.PlatformSettings.scheme_folders + [
        ('pqriscv', 'crypto_kem', ''),
        ('pqriscv', 'crypto_sign', ''),
        ('mupq', 'mupq/crypto_kem', ''),
        ('mupq', 'mupq/crypto_sign', ''),
        ('pqclean', 'mupq/pqclean/crypto_kem', "PQCLEAN"),
        ('pqclean', 'mupq/pqclean/crypto_sign', "PQCLEAN")

    ]

    #: List of dicts, in each dict specify (Scheme class) attributes of the
    #: scheme with values, if all attributes match the scheme is skipped.
    skip_list = (
        {'scheme': 'frodokem640aes', 'implementation': 'clean'},
        {'scheme': 'frodokem640aes', 'implementation': 'opt'},
        {'scheme': 'frodokem976aes', 'implementation': 'clean'},
        {'scheme': 'frodokem976aes', 'implementation': 'opt'},
        {'scheme': 'frodokem1344aes', 'implementation': 'clean'},
        {'scheme': 'frodokem1344aes', 'implementation': 'opt'},
        {'scheme': 'frodokem640shake', 'implementation': 'clean'},
        {'scheme': 'frodokem976shake', 'implementation': 'clean'},
        {'scheme': 'frodokem976shake', 'implementation': 'opt'},
        {'scheme': 'frodokem1344shake', 'implementation': 'clean'},
        {'scheme': 'frodokem1344shake', 'implementation': 'opt'},
        {'scheme': 'mqdss-48', 'implementation': 'clean'},
        {'scheme': 'mqdss-64', 'implementation': 'clean'},
        {'scheme': 'luov-80-76-363-chacha', 'implementation': 'ref'},
        {'scheme': 'luov-80-76-363-keccak', 'implementation': 'ref'},
        {'scheme': 'luov-8-82-323-chacha', 'implementation': 'ref'},
        {'scheme': 'luov-8-82-323-keccak', 'implementation': 'ref'},
        {'scheme': 'luov-8-107-371-chacha', 'implementation': 'ref'},
        {'scheme': 'luov-8-107-371-keccak', 'implementation': 'ref'},
        {'scheme': 'lac128', 'implementation': 'ref'},
        {'scheme': 'lac192', 'implementation': 'ref'},
        {'scheme': 'lac256', 'implementation': 'ref'},
        {'scheme': 'sikep434', 'implementation': 'opt'},
        {'scheme': 'sikep503', 'implementation': 'opt'},
        {'scheme': 'sikep610', 'implementation': 'opt'},
        {'scheme': 'sikep751', 'implementation': 'opt'},
        {'scheme': 'ntrulpr653', 'implementation': 'ref'},
        {'scheme': 'ntrulpr761', 'implementation': 'ref'},
        {'scheme': 'ntrulpr857', 'implementation': 'ref'},
    )

    def __init__(self, vexriscv_platform, debug):
        """Initialize with a specific pqvexriscv platform"""
        super(VexRiscvSettings, self).__init__()
        self.makeflags = [
            "PLATFORM=vexriscv",
            f"VEXRISCV_PLATFORM={vexriscv_platform}",
        ]
        if debug:
            self.makeflags += ["DEBUG=1"]


class VexRiscv(mupq.Platform):

    class FileWrapper:

        def __init__(self, f):
            self.f = open(f, 'rb')
            self.f.seek(0,2)

        def close(self):
            self.f.close()

        def read(self):
            n = 0
            while n < 120:
                c = self.f.read(1)
                if c != b'':
                    return c
                time.sleep(1)
            return b''

    def __init__(self, targetname, openocd_script, uart):
        super(VexRiscv, self).__init__()
        self.targetname = targetname
        self.openocd_script = openocd_script
        self.uart = uart
        self._dev = None

    def __enter__(self):
        if 'tty' in self.uart:
            self._dev = serial.Serial(self.uart, 115200, timeout=20)
        else:
            self._dev = self.FileWrapper(self.uart)
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        self._dev.close()
        self._dev = None
        return super().__exit__(*args, **kwargs)

    def device(self):
        return self._dev

    def flash(self, binary_path):
        super().flash(binary_path)
        call = ["openocd-vexriscv", "-f", self.openocd_script]
        call += ["-c", "reset halt"]
        call += ["-c", "load_image {} 0x80000000 bin".format(binary_path)]
        call += ["-c", "resume 0x80000000"]
        call += ["-c", "shutdown"]
        subprocess.check_call(call, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
