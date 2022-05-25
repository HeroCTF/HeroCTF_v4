.686
.model flat,stdcall
option casemap:none

include c:\masm32\include\masm32rt.inc
; again after the include because masm32rt.inc sets .486 (see http://masm32.com/board/index.php?topic=403.0)
.686 ; for CMOVcc instructions (conditionnal mov --> cmovl)

.CODE
  

; ---------------------------------------------------------------------------------------

get_function:
    push  ebp
	mov   ebp, esp
	sub   esp, 16
    ; edi = ptr to kernel32.dll

_get_kernel32:    
    ASSUME FS:NOTHING  ; without this : "error A2108: use of register assumed to ERROR"
    mov   eax, fs:30h
    mov   eax, DWORD PTR [eax + 0Ch]
    mov   eax, DWORD PTR [eax + 14h]
    mov   eax, DWORD PTR [eax]
    mov   eax, DWORD PTR [eax]
    mov   edi, DWORD PTR [eax + 10h]

_get_func_from_kernel32:
    mov   eax, DWORD PTR [edi + 3Ch]
    mov   eax, DWORD PTR [eax + edi + 78h]
    add   eax, edi
    mov   edx, DWORD PTR [eax + 20h]
    mov   ebx, DWORD PTR [eax + 1Ch]
    add   edx, edi
    mov   ecx, DWORD PTR [eax + 24h]
    add   ebx, edi
    mov   eax, DWORD PTR [eax + 18h]
    add   ecx, edi
    mov   DWORD PTR [ebp - 4], edx ; AddressOfNames
    mov   DWORD PTR [ebp - 8], ecx ; AddressOfNamesOrdinals
    mov   DWORD PTR [ebp - 12], eax ; NumberOfNames
    xor ecx, ecx
    test eax, eax
    jz _fail

_main_loop:
    mov   eax, DWORD PTR [edx + ecx*4]
    add   eax, edi

;====================================================
_function_name_checksum:
    push   ebx
    push   ecx
    mov    esi, eax
    xor    edx, edx
    jmp    short _test_end

_continue:
    movsx  ecx, bl
    rol    edx, 0eh
    cmp    bl, 61h
    lea    eax, [ecx - 20h]
    cmovl  eax, ecx
    add    edx, eax
    inc    esi
    
_test_end:
    mov   bl, BYTE PTR [esi]
    test  bl, bl
    jnz   short _continue

    mov   eax, edx
    pop   ecx
    pop   ebx 
;====================================================

    cmp   eax, [ebp + 8] ; function hash passed as parameter
    jz    _found

    mov   edx, DWORD PTR [ebp - 4] ; AddressOfNames
    inc   ecx
    cmp   ecx, DWORD PTR [ebp - 12] ; NumberOfNames
    jb    short _main_loop

_fail:
    xor eax, eax
    jmp _end

_found:
    mov   eax, DWORD PTR [ebp - 8] ; AddressOfNamesOrdinals
    movzx eax, WORD PTR  [eax + ecx*2]
    mov   eax, DWORD PTR [ebx + eax*4]
    add   eax, edi

_end:
    mov   esp, ebp
	pop   ebp
	ret

; ---------------------------------------------------------------------------------------

start:
    push  ebp
	mov   ebp, esp
    ; checksum("GetDateFormatWWorker") = 0xe3232703
    ; checksum("IsWow64GuestMachineSupported") = 0x89291c8b
    ; checksum("SetThreadPreferredUILanguages") = 0xac881638
    push   0e3232703h
    call   get_function

    push   89291c8bh
    call   get_function

    push   0ac881638h
    call   get_function

    mov   esp, ebp
    pop   ebp
    ret

end start