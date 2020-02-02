CROSS_PREFIX ?= riscv64-unknown-elf
CC            = $(CROSS_PREFIX)-gcc
LD            = $(CROSS_PREFIX)-gcc
OBJCOPY       = $(CROSS_PREFIX)-objcopy
PLATFORM     ?= vexriscv
include common/$(PLATFORM).mk
DEFINES      ?=
OPT_SIZE     ?= 1
ifeq ($(OPT_SIZE),1)
CFLAGS       += -Os
else
CFLAGS       += -O3
endif
DEBUG        ?= 0
ifeq ($(DEBUG),1)
CFLAGS       += -g3
endif
CFLAGS       += \
              -Wall -Wextra -Wimplicit-function-declaration \
              -Wredundant-decls -Wmissing-prototypes -Wstrict-prototypes \
              -Wundef -Wshadow \
              -fno-common -MD $(DEFINES) \
							-DPQRISCV_PLATFORM=$(PLATFORM) \
              $(PLATFORM_CFLAGS)
LDFLAGS      += \
                $(PLATFORM_LDFLAGS)

CC_HOST      = gcc
LD_HOST      = gcc
CFLAGS_HOST  = -O3 -Wall -Wextra -Wpedantic
LDFLAGS_HOST =

# override as desired
TYPE ?= kem

COMMONSOURCES=mupq/common/fips202.c common/sha2.c mupq/common/keccakf1600.c mupq/pqclean/common/aes.c mupq/common/sp800-185.c
COMMONSOURCES_HOST=$(COMMONSOURCES)
COMMONSOURCES_RISCV=$(COMMONSOURCES)

COMMONINCLUDES=-I"mupq/common"
COMMONINCLUDES_RISCV=$(COMMONINCLUDES) -I"common"

RANDOMBYTES_RISCV=common/randombytes.c

DEST_HOST=bin-host
DEST=bin

TARGET_NAME = $(shell echo $(IMPLEMENTATION_PATH) | sed 's@/@_@g')
TYPE = $(shell echo $(IMPLEMENTATION_PATH) | sed -r 's@(.*/)?crypto_(kem|sign)(/.*)@\2@')
IMPLEMENTATION_SOURCES = $(wildcard $(IMPLEMENTATION_PATH)/*.c) $(wildcard $(IMPLEMENTATION_PATH)/*.s) $(wildcard $(IMPLEMENTATION_PATH)/*.S)
IMPLEMENTATION_HEADERS = $(IMPLEMENTATION_PATH)/*.h

info:
	@echo "TARGET_NAME: $(TARGET_NAME)"

.PHONY: all
all:
	@echo "Please use the scripts in this directory instead of using the Makefile"
	@echo
	@echo "If you really want to use it, please specify IMPLEMENTATION_PATH=path/to/impl"
	@echo "and a target binary, e.g.,"
	@echo "make IMPLEMENTATION_PATH=crypto_kem/kyber768/m4 bin/crypto_kem_kyber768_m4_test.bin"
	@echo "make clean also works"

$(DEST_HOST)/%_testvectors: $(COMMONSOURCES_HOST) $(IMPLEMENTATION_SOURCES) $(IMPLEMENTATION_HEADERS)
	mkdir -p $(DEST_HOST)
	$(CC_HOST) -o $@ \
		$(CFLAGS_HOST) -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE)\
		mupq/crypto_$(TYPE)/testvectors-host.c \
		$(COMMONSOURCES_HOST) \
		$(IMPLEMENTATION_SOURCES) \
		-I$(IMPLEMENTATION_PATH) \
		$(COMMONINCLUDES) \
		$(LDFLAGS_HOST)

$(DEST)/%.bin: elf/%.elf
	mkdir -p $(DEST)
	$(OBJCOPY) -Obinary $^ $@


# pattern rules, intended to match % to the type of test (i.e. test, speed, stack)
# note that this excludes testvectors, as that is a special case that provides its own randombytes
# TODO use notrandombytes more generically rather than included in testvectors.c
elf/$(TARGET_NAME)_%.elf: mupq/crypto_$(TYPE)/%.c $(COMMONSOURCES_RISCV) $(RANDOMBYTES_RISCV) $(IMPLEMENTATION_SOURCES) $(IMPLEMENTATION_HEADERS) $(PLATFORM_LINKDEP)
	mkdir -p elf
	$(CC) -o $@ $(CFLAGS) -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE) \
		$< $(COMMONSOURCES_RISCV) $(RANDOMBYTES_RISCV) $(IMPLEMENTATION_SOURCES) common/hal-$(PLATFORM).c \
		-I$(IMPLEMENTATION_PATH) $(COMMONINCLUDES_RISCV) $(LDFLAGS)

elf/$(TARGET_NAME)_testvectors.elf: mupq/crypto_$(TYPE)/testvectors.c $(COMMONSOURCES_RISCV) $(IMPLEMENTATION_SOURCES) $(IMPLEMENTATION_HEADERS) $(PLATFORM_LINKDEP)
	mkdir -p elf
	$(CC) -o $@ $(CFLAGS) -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE)\
		$< $(COMMONSOURCES_RISCV) $(IMPLEMENTATION_SOURCES) common/hal-$(PLATFORM).c \
		-I$(IMPLEMENTATION_PATH) $(COMMONINCLUDES_RISCV) $(LDFLAGS)

elf/$(TARGET_NAME)_hashing.elf: mupq/crypto_$(TYPE)/hashing.c $(COMMONSOURCES_RISCV) $(IMPLEMENTATION_SOURCES) $(IMPLEMENTATION_HEADERS) $(PLATFORM_LINKDEP) 
	mkdir -p elf
	$(CC) -o $@ $(CFLAGS) -DPROFILE_HASHING -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE) \
		$< $(COMMONSOURCES_RISCV) $(RANDOMBYTES_RISCV) $(IMPLEMENTATION_SOURCES) common/hal-$(PLATFORM).c \
		-I$(IMPLEMENTATION_PATH) $(COMMONINCLUDES_RISCV) $(LDFLAGS)

obj/$(TARGET_NAME)_%.o: $(IMPLEMENTATION_PATH)/%.c $(IMPLEMENTATION_HEADERS)
	mkdir -p obj
	$(CC) -o $@ -c $(CFLAGS) -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE) \
		-I$(IMPLEMENTATION_PATH) $(COMMONINCLUDES_RISCV) $<

obj/$(TARGET_NAME)_%.o: $(IMPLEMENTATION_PATH)/%.s $(IMPLEMENTATION_HEADERS)
	mkdir -p obj
	$(CC) -o $@ -c $(CFLAGS) -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE) \
		-I$(IMPLEMENTATION_PATH) $(COMMONINCLUDES_RISCV) $<

obj/$(TARGET_NAME)_%.o: $(IMPLEMENTATION_PATH)/%.S $(IMPLEMENTATION_HEADERS)
	mkdir -p obj
	$(CC) -o $@ -c $(CFLAGS) -DMUPQ_NAMESPACE=$(MUPQ_NAMESPACE) \
		-I$(IMPLEMENTATION_PATH) $(COMMONINCLUDES_RISCV) $<

.PHONY: clean

clean:
	rm -rf elf/
	rm -rf bin/
	rm -rf bin-host/
	rm -rf obj/
	rm -rf testvectors/
	rm -rf benchmarks/

.SECONDARY:
