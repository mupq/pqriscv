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

    large_schemes = (
        {'scheme': 'sikep434'},
        {'scheme': 'sikep503'},
        {'scheme': 'sikep610'},
        {'scheme': 'sikep751'},
        {'scheme': 'lac192'},
        {'scheme': 'lac256'},
        {'scheme': 'lac128'},
        {'scheme': 'lac192'},
        {'scheme': 'lac256'},
        {'scheme': 'ntrulpr653'},
        {'scheme': 'ntrulpr761'},
        {'scheme': 'ntrulpr857'},
        {'scheme': 'ledakemlt12'},
        {'scheme': 'ledakemlt32'},
        {'scheme': 'ledakemlt52'},
        {'scheme': 'r5n1-3kemcca-0d'},
        {'scheme': 'r5n1-3kemcca-0d-sneik'},
        {'scheme': 'r5n1-5kemcca-0d'},
        {'scheme': 'r5n1-5kemcca-0d-sneik'},
        {'scheme': 'r5n1-3kemcca-0d'},
        {'scheme': 'r5n1-3kemcca-0d-sneik'},
        {'scheme': 'r5n1-5kemcca-0d'},
        {'scheme': 'r5n1-5kemcca-0d-sneik'},
        {'scheme': 'rollo-I-128'},
        {'scheme': 'rollo-I-192'},
        {'scheme': 'rollo-I-256'},
        {'scheme': 'rollo-II-128'},
        {'scheme': 'rollo-II-192'},
        {'scheme': 'rollo-II-256'},
        {'scheme': 'rollo-III-128'},
        {'scheme': 'rollo-III-192'},
        {'scheme': 'rollo-III-256'},
        {'scheme': 'rqc128'},
        {'scheme': 'rqc192'},
        {'scheme': 'rqc256'},
        {'scheme': 'sntrup653'},
        {'scheme': 'sntrup761'},
        {'scheme': 'sntrup857'},
        {'scheme': 'falcon-512'},
        {'scheme': 'falcon-1024'},
        {'scheme': 'falcon-512-tree'},
        {'scheme': 'falcon-1024-tree'},
        {'scheme': 'dilithium2'},
        {'scheme': 'dilithium3'},
        {'scheme': 'dilithium4'},
        {'scheme': 'luov-7-110-374-chacha'},
        {'scheme': 'luov-7-110-374-keccak'},
        {'scheme': 'luov-61-60-261-chacha'},
        {'scheme': 'luov-61-60-261-keccak'},
        {'scheme': 'luov-7-83-283-chacha'},
        {'scheme': 'luov-7-83-283-keccak'},
        {'scheme': 'luov-79-76-341-chacha'},
        {'scheme': 'luov-79-76-341-keccak'},
        {'scheme': 'frodokem640aes'},
        {'scheme': 'frodokem976aes'},
        {'scheme': 'frodokem1344aes'},
        {'scheme': 'frodokem640shake'},
        {'scheme': 'frodokem976shake'},
        {'scheme': 'frodokem1344shake'},
        {'scheme': 'kyber512-90s'}, # AES Implementation is too big ATM
        {'scheme': 'kyber768-90s'},
        {'scheme': 'kyber1024-90s'},
        {'scheme': 'mqdss-48'},
        {'scheme': 'mqdss-64'},
        {'scheme': 'qtesla-p-I'},
        {'scheme': 'qtesla-p-III'},
        {'scheme': 'rainbowIa-classic'},
        {'scheme': 'rainbowIa-cyclic'},
        {'scheme': 'rainbowIa-cyclic-compressed'},
        {'scheme': 'rainbowIIIc-classic'},
        {'scheme': 'rainbowIIIc-cyclic'},
        {'scheme': 'rainbowIIIc-cyclic-compressed'},
        {'scheme': 'rainbowVc-classic'},
        {'scheme': 'rainbowVc-cyclic'},
        {'scheme': 'rainbowVc-cyclic-compressed'},
        {'scheme': 'sphincs-haraka-128s-robust'},
        {'scheme': 'sphincs-haraka-128s-simple'},
        {'scheme': 'sphincs-haraka-192s-robust'},
        {'scheme': 'sphincs-haraka-192s-simple'},
        {'scheme': 'sphincs-haraka-256s-robust'},
        {'scheme': 'sphincs-haraka-256s-simple'},
        {'scheme': 'sphincs-haraka-192f-robust'},
        {'scheme': 'sphincs-haraka-192f-simple'},
        {'scheme': 'sphincs-haraka-256f-robust'},
        {'scheme': 'sphincs-haraka-256f-simple'},
        {'scheme': 'sphincs-sha256-128f-robust'},
        {'scheme': 'sphincs-sha256-128f-simple'},
        {'scheme': 'sphincs-sha256-128s-robust'},
        {'scheme': 'sphincs-sha256-128s-simple'},
        {'scheme': 'sphincs-sha256-192f-robust'},
        {'scheme': 'sphincs-sha256-192f-simple'},
        {'scheme': 'sphincs-sha256-192s-robust'},
        {'scheme': 'sphincs-sha256-192s-simple'},
        {'scheme': 'sphincs-sha256-256f-robust'},
        {'scheme': 'sphincs-sha256-256f-simple'},
        {'scheme': 'sphincs-sha256-256s-robust'},
        {'scheme': 'sphincs-sha256-256s-simple'},
        {'scheme': 'sphincs-shake256-192f-robust'},
        {'scheme': 'sphincs-shake256-192f-simple'},
        {'scheme': 'sphincs-shake256-256f-robust'},
        {'scheme': 'sphincs-shake256-256f-simple'},
    )

    #: List of dicts, in each dict specify (Scheme class) attributes of the
    #: scheme with values, if all attributes match the scheme is skipped.
    skip_list = (
        # TODO: Remove once mamabear folder in mupq is fixed
        {'scheme': 'babybear-ephem'},
        {'scheme': 'mamabear-ephem'},
        {'scheme': 'papabear-ephem'},
    )

    size_executable = 'riscv64-unknown-elf-size'

    def __init__(self, vexriscv_platform, debug):
        """Initialize with a specific pqvexriscv platform"""
        super(VexRiscvSettings, self).__init__()
        if vexriscv_platform != 'pqvexriscvsimhuge':
            self.skip_list = self.skip_list + self.large_schemes
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
            while n < 600:
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
