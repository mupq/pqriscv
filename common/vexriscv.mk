RISCV_ARCH ?= rv32im
RISCV_ABI ?= ilp32
RISCV_CMODEL ?= medany
RISCV_ARCHFLAGS += -march=$(RISCV_ARCH)
RISCV_ARCHFLAGS += -mabi=$(RISCV_ABI)
RISCV_ARCHFLAGS += -mcmodel=$(RISCV_CMODEL)

# C Flags that must be used for the Murax SoC
VEXRISCV_CFLAGS += $(RISCV_ARCHFLAGS)
VEXRISCV_CFLAGS += -fstrict-volatile-bitfields
# VEXRISCV_CFLAGS += --specs=nano.specs --specs=nosys.specs

VEXRISCV_PLATFORM ?= pqvexriscvup5k

VEXRISCV_LINKERSCRIPT = common/bsp/vexriscv/$(VEXRISCV_PLATFORM).ld
# LD Flags that must be used to link executables for the Murax SoC
VEXRISCV_LDFLAGS += $(RISCV_ARCHFLAGS)
VEXRISCV_LDFLAGS += --specs=nano.specs --specs=nosys.specs
VEXRISCV_LDFLAGS += -Wl,-T$(VEXRISCV_LINKERSCRIPT)
VEXRISCV_LDFLAGS += -nostartfiles -ffreestanding -Wl,--gc-sections
VEXRISCV_LDFLAGS += -Lcommon/bsp/vexriscv
VEXRISCV_LDFLAGS += -Wl,--start-group -l$(VEXRISCV_PLATFORM)bsp -lc -Wl,--end-group

PLATFORM_CFLAGS = $(VEXRISCV_CFLAGS) -DVEXRISCV_PLATFORM=$(VEXRISCV_PLATFORM)
PLATFORM_LDFLAGS = $(VEXRISCV_LDFLAGS)
PLATFORM_LINKDEP = common/bsp/vexriscv/lib$(VEXRISCV_PLATFORM)bsp.a

$(PLATFORM_LINKDEP):
	make -C common/bsp/vexriscv PLATFORM=$(VEXRISCV_PLATFORM)
