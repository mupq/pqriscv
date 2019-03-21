import subprocess

from mupq import mupq


class RISCVSettings(mupq.PlatformSettings):
    #: Specify folders to include
    scheme_folders = [  # mupq.PlatformSettings.scheme_folders + [
        ('pqm4', 'crypto_kem'),
        ('pqm4', 'crypto_sign'),
    ]

    #: List of dicts, in each dict specify (Scheme class) attributes of the
    #: scheme with values, if all attributes match the scheme is skipped.
    skip_list = (
        {'scheme': 'frodo640-aes', 'implementation': 'ref'},
        {'scheme': 'frodo640-cshake', 'implementation': 'ref'},
    )


class RISCV(mupq.Platform):

    # return device for serial communication
    def device(self):
        raise NotImplementedError

    # flash binary to device
    def flash(self, binary_path):
        raise NotImplementedError

