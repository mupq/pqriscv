OUTPUT_FORMAT("elf32-littleriscv", "elf32-littleriscv", "elf32-littleriscv")
OUTPUT_ARCH(riscv)

ENTRY( _start )

__ram_size = 16M;

MEMORY
{
rom (wxa!ri) : ORIGIN = 0x80000000, LENGTH = 8M
ram (wxa!ri) : ORIGIN = 0x80800000, LENGTH = 8M
}

INCLUDE nonvolatile.ld
