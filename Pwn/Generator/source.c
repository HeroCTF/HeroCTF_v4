#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// gcc -no-pie -fno-stack-protector -Wno-stringop-overflow -masm=intel -o Generator source.c

// XOR it to have "/bin/sh\x00"
char random_str[8];
const char* playstore_link = "https://bit.ly/384qugO";


void interesting(){
	__asm__ __volatile__ (
	"xor [rdi], rsi\n"
	"ret\n"	

	"pop rdi\n"
	"pop rsi\n"
	"pop rdx\n"
	"ret\n"

	"xchg rax, rdx\n"
	"ret\n"

	"syscall\n"
	);
}


int main(void){
	char answer[5];
	srand(time(NULL));
	
	// Creating random string
	for(int i=0; i < 7; i++){
		random_str[i] = (rand() % (126 - 33 + 1)) + 33;
	}
	random_str[7] = '\x00';

	printf("Random string generated: %s\n", random_str);
	printf("Are you satisfied by this application ? (yes/no) ");
	fflush(stdout);
	fgets(answer, 100, stdin);

	if(!strncmp(answer, "yes", 3)){
		printf("Nice ! Rate us on the playstore: %s\n", playstore_link);
		fflush(stdout);
	
	}else{
		// didn't find the GCC flag to disable optimisation that will replace printf("...\n") with puts(...) ¯\_(ツ)_/¯
		printf("Sorry to read this, we will do our best to give you a better user experience...%c", '\n');
		fflush(stdout);
		exit(1);
	}
	
	return EXIT_SUCCESS;
}
