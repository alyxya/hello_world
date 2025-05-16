#!/usr/bin/env python3

import struct
import os
import stat

# Hello World shellcode for x86-64
# This shellcode:
# - Makes a write syscall (1) to stdout (1) with the message "Hello, World!"
# - Makes an exit syscall (60) with exit code 0
SHELLCODE = bytes([
    # write(1, message, 14)
    0x48, 0xc7, 0xc0, 0x01, 0x00, 0x00, 0x00,  # mov rax, 1
    0x48, 0xc7, 0xc7, 0x01, 0x00, 0x00, 0x00,  # mov rdi, 1
    0x48, 0x8d, 0x35, 0x19, 0x00, 0x00, 0x00,  # lea rsi, [rip+25]
    0x48, 0xc7, 0xc2, 0x0e, 0x00, 0x00, 0x00,  # mov rdx, 14
    0x0f, 0x05,                                # syscall

    # exit(0)
    0x48, 0xc7, 0xc0, 0x3c, 0x00, 0x00, 0x00,  # mov rax, 60
    0x48, 0xc7, 0xc7, 0x00, 0x00, 0x00, 0x00,  # mov rdi, 0
    0x0f, 0x05,                                # syscall

    # "Hello, World!" string with newline
    0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x2c, 0x20, 0x57, 0x6f, 0x72, 0x6c, 0x64, 0x21, 0x0a
])

# Base address where the program will be loaded
LOAD_ADDR = 0x400000
ENTRY_POINT = LOAD_ADDR + 0x78  # Entry point (header size + program headers size)

def create_elf():
    # ELF Header (64 bytes for 64-bit ELF)
    elf_header = bytearray(64)

    # e_ident (16 bytes)
    elf_header[0:4] = b'\x7fELF'  # EI_MAG
    elf_header[4] = 2             # EI_CLASS (ELFCLASS64)
    elf_header[5] = 1             # EI_DATA (ELFDATA2LSB)
    elf_header[6] = 1             # EI_VERSION
    elf_header[7] = 0             # EI_OSABI
    elf_header[8] = 0             # EI_ABIVERSION
    # bytes 9-15 remain as zeros (EI_PAD)

    # Rest of the header (all values in little-endian)
    elf_header[16:18] = struct.pack('<H', 2)      # e_type (ET_EXEC)
    elf_header[18:20] = struct.pack('<H', 62)     # e_machine (EM_X86_64)
    elf_header[20:24] = struct.pack('<I', 1)      # e_version
    elf_header[24:32] = struct.pack('<Q', ENTRY_POINT)  # e_entry
    elf_header[32:40] = struct.pack('<Q', 64)     # e_phoff (program header offset)
    elf_header[40:48] = struct.pack('<Q', 0)      # e_shoff (no section headers)
    elf_header[48:52] = struct.pack('<I', 0)      # e_flags
    elf_header[52:54] = struct.pack('<H', 64)     # e_ehsize
    elf_header[54:56] = struct.pack('<H', 56)     # e_phentsize
    elf_header[56:58] = struct.pack('<H', 1)      # e_phnum (1 program header)
    elf_header[58:60] = struct.pack('<H', 0)      # e_shentsize
    elf_header[60:62] = struct.pack('<H', 0)      # e_shnum
    elf_header[62:64] = struct.pack('<H', 0)      # e_shstrndx

    # Program header (56 bytes for 64-bit ELF)
    program_header = bytearray(56)

    # Fill in program header fields
    program_header[0:4] = struct.pack('<I', 1)    # p_type (PT_LOAD)
    program_header[4:8] = struct.pack('<I', 5)    # p_flags (PF_R | PF_X)
    program_header[8:16] = struct.pack('<Q', 0)   # p_offset
    program_header[16:24] = struct.pack('<Q', LOAD_ADDR)  # p_vaddr
    program_header[24:32] = struct.pack('<Q', LOAD_ADDR)  # p_paddr
    program_header[32:40] = struct.pack('<Q', 64 + 56 + len(SHELLCODE))  # p_filesz
    program_header[40:48] = struct.pack('<Q', 64 + 56 + len(SHELLCODE))  # p_memsz
    program_header[48:56] = struct.pack('<Q', 0x1000)  # p_align

    # Calculate size of the resulting ELF file
    elf_size = 64 + 56 + len(SHELLCODE)

    # Create the binary data
    elf_data = bytearray(elf_size)

    # Write ELF header
    elf_data[0:64] = elf_header

    # Write program header
    elf_data[64:120] = program_header

    # Write shellcode
    elf_data[120:120+len(SHELLCODE)] = SHELLCODE

    return bytes(elf_data)

def main():
    elf_data = create_elf()

    # Write to file
    output_file = 'helloworld'
    with open(output_file, 'wb') as f:
        f.write(elf_data)

    # Make the file executable
    os.chmod(output_file, os.stat(output_file).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Created executable '{output_file}'")
    print("Run it with: ./helloworld")

if __name__ == '__main__':
    main()
