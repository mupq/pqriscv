RISCV_ARCH ?= rv32im
RISCV_ABI ?= ilp32
RISCV_CMODEL ?= medany
RISCV_ARCHFLAGS += -march=$(RISCV_ARCH)
RISCV_ARCHFLAGS += -mabi=$(RISCV_ABI)
RISCV_ARCHFLAGS += -mcmodel=$(RISCV_CMODEL)

CFLAGS += -Os -Wall -Wextra
CFLAGS += $(RISCV_ARCHFLAGS)
CFLAGS += -fstrict-volatile-bitfields
CFLAGS += --specs=nano.specs --specs=nosys.specs

CROSS_PREFIX ?= riscv64-unknown-elf
CC = $(CROSS_PREFIX)-gcc
AR = $(CROSS_PREFIX)-ar

SRCS = init.c murax_start.s
OBJS = init.o murax_start.o
TARGET = libmuraxbsp.a

all: $(TARGET)

$(TARGET): $(OBJS)
	$(AR) rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.S
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -rf $(OBJS) $(TARGET)
