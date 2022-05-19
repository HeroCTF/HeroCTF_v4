BITS 32
        org     0x08040000
  
ehdr:                                           ; ***** Elf32_Ehdr *****
                db      0x7F, "E", "L", "F"     ;   e_ident[EI_MAG]
                db      1                       ;   e_ident[EI_CLASS]   (32 bits)
bin_sh          db      0x34 ; "/"                     ;   e_ident[EI_DATA]
                db      0xb7 ; "b"                     ;   e_ident[EI_VERSION]
                db      0x17 ; "i"                     ;   e_ident[EI_OSABI]
                db      0xb1 ; "n"                     ;   e_ident[EI_ABIVERSION]
                
                db      0x34
                db      0x80
                db      0x97
                db      0x39
                dw      0
                db      0
                ; db      "/sh", 0, 0, 0, 0       ;   e_ident[EI_PAD]        

                dw      2                       ;   e_type      (ET_EXEC)
                dw      3                       ;   e_machine   (x86)
                dd      1                       ;   e_version   (ELF version)
                dd      _part1                  ;   e_entry
                dd      phdr - $$               ;   e_phoff
_part1:
        mov     ebx, bin_sh-1                   ;   e_shoff
        inc     ebx                             ;   e_flags
        jmp     _part2

                dw      ehdrsize                ;   e_ehsize
                dw      phdrsize                ;   e_phentsize
                                                ;                 ***** Elf32_Phdr *****
phdr:           dd      1                       ;   e_phnum             p_type
                                                ;   e_shentsize
                dd      0                       ;   e_shnum             p_offset
                                                ;   e_shstrndx
ehdrsize        equ     $ - ehdr

                dd      $$                      ;   p_vaddr
_part2:
                mov     al, 0xb                 ;   p_paddr
                jmp     _part3                                     
                dd      filesize                ;   p_filesz
                dd      filesize                ;   p_memsz
                db      7                       ;   p_flags
_part3:         rol     DWORD [ebx], 17
                ror     DWORD [ebx+4], 15       ; p_align

phdrsize        equ     $ - phdr
                int     0x80
filesize        equ     $ - $$