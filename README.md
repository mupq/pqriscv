# pqriscv
Post-quantum crypto library for the ARM Cortex-M4

## WIP

This is a work-in-progress for now.

## Introduction

This will be the RISC-V counterpart to the **pqm4** library,
benchmarking and testing framework.

## Setup/Installation
The **pqriscv** framework currently targets the
[VexRiscv](https://github.com/SpinalHDL/VexRiscv)
implementation of the RISC-V ISA. Dedicated implementations
for various FPGAs, as well as a simulator are planned. The
framework is, however, setup to potentially support multiple
platforms in form of simple board support packages (BSP).

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
Currently, no testing akin to **pqm4** is supported. You'll
have to load the ELF/binary manually onto your target.
