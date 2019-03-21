RISCV_ARCH ?= rv32im
RISCV_ABI ?= ilp32
RISCV_CMODEL ?= medany
RISCV_ARCHFLAGS += -march=$(RISCV_ARCH)
RISCV_ARCHFLAGS += -mabi=$(RISCV_ABI)
RISCV_ARCHFLAGS += -mcmodel=$(RISCV_CMODEL)

# C Flags that must be used for the Murax SoC
MURAX_CFLAGS += $(RISCV_ARCHFLAGS)
MURAX_CFLAGS += -fstrict-volatile-bitfields
MURAX_CFLAGS += --specs=nano.specs --specs=nosys.specs

# LD Flags that must be used to link executables for the Murax SoC
MURAX_LDFLAGS += $(RISCV_ARCHFLAGS)
MURAX_LDFLAGS += --specs=nano.specs --specs=nosys.specs
MURAX_LDFLAGS += -Wl,-Tmurax.ld
MURAX_LDFLAGS += -nostartfiles -ffreestanding -Wl,--gc-sections
# Something like this might be necessary, if _init / _fini can't be found
# MURAX_LDFLAGS += -Wl,--start-group init.o -lc -Wl,--end-group
