# pqriscv

## WIP

This is a work-in-progress for now.

## Introduction

This will be the RISC-V counterpart to the **pqm4** library,
benchmarking and testing framework.

## Setup/Installation
The **pqriscv** framework currently targets the
[VexRiscv](https://github.com/SpinalHDL/VexRiscv)
implementation of the RISC-V ISA. Dedicated implementations
for various FPGAs are provided by the
[pqriscv-vexriscv](https://github.com/mupq/pqriscv-vexriscv)
project. The framework is, however, setup to potentially
support multiple platforms in form of simple board support
packages (BSP).

### Toolchain
You'll need a suitable GNU toolchain for your RISC-V target,
so far the toolchain provided by [SiFive (see the "Prebuild
RISC-V GCC Toolchain"
section)](https://www.sifive.com/boards) can be used without
problems.

### Python3
The build-scripts require Python >= 3.6

### Building
Execute the `build_everything.py` script to build all
exeutables in ELF and binary format. All scripts support the
following flags:

* `-p` / `--platform`: Choose the target platform. Currently
  only `vexriscv` is supported.
* `-s` / `--sub-platform`: Choose the sub-platform. Some
  platforms may have multiple targets, implementations,
  boards, or similar.
* `-d` / `--debug`: Compile everything with debug flags.

### Testing
Testing akin to **pqm4** is currently a WIP. For now, the
speed, hashing and size benchmarks work to some degree, as
do the test vector tests. The tests require further command
line flags to those mentioned above:

* `-u UART`:
* `--openocd-script SCRIPT`: This script will be passed to
  OpenOCD to connect to the target (see
  [pqriscv-vexriscv](https://github.com/mupq/pqriscv-vexriscv)).
