import argparse
from mupq import mupq

PQRISCV_PLATFORMS = 'vexriscv'

def parse_arguments():
    parser = argparse.ArgumentParser(description='pqriscv specific settings')
    parser.add_argument('-d', '--debug', help='Enable debug flags', default=False, action='store_true')
    parser.add_argument('-p', '--platform', help='The pqriscv platform', choices=['vexriscv'], default='vexriscv')
    parser.add_argument('-s', '--sub-platform', help='The platform subtype', default='pqvexriscvup5k')
    return parser.parse_known_args()

def get_platform(args):
    # NOTE: Add new platforms with an elif args.platform == 'XYZ':...
    if args.platform == 'vexriscv':
        settings = VexRiscvSettings(args.sub_platform, args.debug)
        platform = VexRiscv()
    else:
        raise ValueError('Unknown pqriscv platform')
    return platform, settings

class VexRiscvSettings(mupq.PlatformSettings):
    PQVEXRISCV_PLATFORMS = ['murax', 'pqvexriscvup5k', 'pqvexriscvicoboard']
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
        {'scheme': 'frodokem976aes', 'implementation': 'clean'},
        {'scheme': 'frodokem1344aes', 'implementation': 'clean'}
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

    def __enter__(self):
        # TODO: Implement something
        return super().__enter__()

    def __exit__(self,*args, **kwargs):
        # TODO: Implement something
        return super().__exit__(*args, **kwargs)

    def device(self):
        # TODO: Implement something
        return None

    def flash(self, binary_path):
        super().flash(binary_path)
        # TODO: Implement something
