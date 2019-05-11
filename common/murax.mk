RISCV_ARCH ?= rv32im
RISCV_ABI ?= ilp32
RISCV_CMODEL ?= medany
RISCV_ARCHFLAGS += -march=$(RISCV_ARCH)
RISCV_ARCHFLAGS += -mabi=$(RISCV_ABI)
RISCV_ARCHFLAGS += -mcmodel=$(RISCV_CMODEL)

# C Flags that must be used for the Murax SoC
MURAX_CFLAGS += $(RISCV_ARCHFLAGS)
MURAX_CFLAGS += -fstrict-volatile-bitfields
# MURAX_CFLAGS += --specs=nano.specs --specs=nosys.specs

MURAX_LINKERSCRIPT = common/bsp/murax/murax.ld
# LD Flags that must be used to link executables for the Murax SoC
MURAX_LDFLAGS += $(RISCV_ARCHFLAGS)
MURAX_LDFLAGS += --specs=nano.specs --specs=nosys.specs
MURAX_LDFLAGS += -Wl,-T$(MURAX_LINKERSCRIPT)
MURAX_LDFLAGS += -nostartfiles -ffreestanding -Wl,--gc-sections
MURAX_LDFLAGS += -Lcommon/bsp/murax
MURAX_LDFLAGS += -Wl,--start-group -lmuraxbsp -lc -Wl,--end-group

PLATFORM_CFLAGS = $(MURAX_CFLAGS)
PLATFORM_LDFLAGS = $(MURAX_LDFLAGS)
PLATFORM_LINKDEP = common/bsp/murax/libmuraxbsp.a

$(PLATFORM_LINKDEP):
	make -C common/bsp/murax
