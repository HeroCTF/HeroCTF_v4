#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// compile from C to LLVM IR : clang -S -emit-llvm -no-pie -o MVBN.s source.c
// compile LLVM IR to ELF x64 (without linking) : llc -o MVBN.o MVBN.s -filetype=obj
// link libc : gcc -no-pie -o MVBN MVBN.o

unsigned char key[33] = {0x37,0x20,0x3e,0x29,0x04,0x09,0x00,0x10,0x32,0x1a,0x7d,0x35,0x20,0x71,0x13,0x30,0x4c,0x37,0x35,0x19,0x1c,0x75,0x7c,0x2a,0x20,0x35,0x3e,0x76,0x15,0x76,0x2f,0x32,0x02};

// ELF header : 0x7f, 0x45, 0x4c, 0x46
int check_password(char* passwd){
	if(strlen(passwd) != 33){
		return -1;
	}

	for(int i=0; i < 33; i++){
		if((*(unsigned char*)(0x400000 + (i % 4)) ^ passwd[i]) != key[i]){
			return 1;
		}
	}

	return 0;
}

int main(int argc, char** argv){
	if(argc != 2){
		printf("Usage: %s <flag>\n", argv[0]);
		return EXIT_FAILURE;
	}

	if(check_password(argv[1])){
		puts("[-] Bad password... Try again.");
	
	}else{
		puts("[+] Well done ! You can validate with flag :)");
	}

	return EXIT_SUCCESS;
}
