# Hello World

A simple project that demonstrates how to create a minimal ELF executable for x86-64 Linux that prints "Hello, World!".

## Overview

This project contains a Python script that generates a complete ELF binary from scratch without using any assembler or compiler. The generated binary:

- Is a valid 64-bit ELF executable
- Contains hand-crafted x86-64 shellcode
- Makes system calls directly (write and exit)
- Requires no external dependencies

## Usage

Run the Python script to compile the Hello World program:

```bash
python compile_hello_world.py
```

This will create an executable file named `helloworld`. You can run it with:

```bash
./helloworld
```

The program will print "Hello, World!" and exit with status code 0.

## Technical Details

The script creates a minimal ELF binary with:
- A 64-byte ELF header
- A 56-byte program header
- Custom x86-64 shellcode that:
  - Uses the write syscall to print the message
  - Uses the exit syscall to terminate cleanly
- No section headers or other optional ELF structures

## Requirements

- Python 3.x
- Linux environment (to run the generated binary)
