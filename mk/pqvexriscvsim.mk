VEXRISCV_ROMSIZE=256K
VEXRISCV_RAMSIZE=128K
VEXRISCV_RWMTVEC=1

excluded_schemes = \
	mupq/pqclean/crypto_kem/mceliece% \
	mupq/crypto_sign/falcon-1024-tree%

include mk/pqvexriscv.mk
