RISCV_ARCH ?= rv32imc
RISCV_ABI ?= ilp32
RISCV_CMODEL ?= medany

ARCH_FLAGS += \
	-march=$(RISCV_ARCH) \
	-mabi=$(RISCV_ABI) \
	-mcmodel=$(RISCV_CMODEL)

CROSS_PREFIX ?= riscv64-unknown-elf
CC := $(CROSS_PREFIX)-gcc
CPP := $(CROSS_PREFIX)-cpp
AR := $(CROSS_PREFIX)-ar
LD := $(CC)
OBJCOPY := $(CROSS_PREFIX)-objcopy
SIZE := $(CROSS_PREFIX)-size

CFLAGS += \
	$(ARCH_FLAGS) \
	--specs=nano.specs \
	--specs=nosys.specs

LDFLAGS += \
	--specs=nano.specs \
	--specs=nosys.specs \
	-Wl,--wrap=_sbrk \
	-ffreestanding \
	-nostartfiles \
	-T$(LDSCRIPT) \
	$(ARCH_FLAGS)

LIBHAL_SRC := \
	common/vexriscv/start.S \
	common/vexriscv/init.c \
	common/hal-vexriscv.c \
	common/randombytes.c

obj/libpqvexriscvhal.a: $(call objs,$(LIBHAL_SRC))
obj/libpqvexriscvhal-nornd.a: $(call objs,$(filter-out common/randombytes.c,$(LIBHAL_SRC)))
obj/libpqvexriscvhal.a: CPPFLAGS += \
	-Icommon/vexriscv \
	$(if $(VEXRISCV_NONVOLATILE_ROM),,-DVEXRISCV_VOLATILE) \
	$(if $(VEXRISCV_RWMTVEC),-DVEXRISCV_RWMTVEC)

ifeq ($(AIO),1)
LDLIBS +=
LIBDEPS += $$(if $$(NO_RANDOMBYTES),$(filter-out common/randombytes.c,$(LIBHAL_SRC)),$(LIBHAL_SRC))
else
LDLIBS += -lpqm4hal$(if $(NO_RANDOMBYTES),-nornd)
LIBDEPS += obj/libpqm4hal$$(if $$(NO_RANDOMBYTES),-nornd).a
endif

LDSCRIPT = obj/ldscript.ld

LDLIBS += -lpqvexriscvhal$(if $(NO_RANDOMBYTES),-nornd)
LIBDEPS += obj/libpqvexriscvhal.a obj/libpqvexriscvhal-nornd.a

$(LDSCRIPT): common/vexriscv/vexriscv.ld $(CONFIG)
	@printf "  GENLNK  $@\n"; \
	[ -d $(@D) ] || $(Q)mkdir -p $(@D); \
	arm-none-eabi-gcc -x assembler-with-cpp -E -Wp,-P $(CPPFLAGS) $< -o $@

ifndef VEXRISCV_ROMSIZE
$(error Platform must define at least VEXRISCV_ROMSIZE)
endif

$(LDSCRIPT): CPPFLAGS += \
	$(if $(VEXRISCV_NONVOLATILE_ROM),-DNONVOLATILE_ROM) \
	$(if $(VEXRISCV_ROMORIGIN),-DROMORIGIN=$(VEXRISCV_ROMORIGIN)) \
	$(if $(VEXRISCV_RAMORIGIN),-DROMORIGIN=$(VEXRISCV_RAMORIGIN)) \
	-DROMSIZE=$(VEXRISCV_ROMSIZE) \
	$(if $(VEXRISCV_RAMSIZE),-DRAMSIZE=$(VEXRISCV_RAMSIZE))

LINKDEPS += $(LDSCRIPT) $(LIBDEPS)
