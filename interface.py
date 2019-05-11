from mupq import mupq

class MuraxSettings(mupq.PlatformSettings):
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


class Murax(mupq.Platform):

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
