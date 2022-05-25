#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void secret(long pass1, long pass2, long pass3){
	char* flag = "Hero{ret2csu_1s_th3_w4y_f0r_th1s_f4ncy_aarch64_ROP!!!}";
	if(pass1 == 0xDEADBEEF){
		if(pass2 == 0xCAFEBABE900DF00D){
			if(pass3 == 0xFEEDBABEBAADF00D){
				printf("Well, I guess you can have my secret: %s\n", flag);
				fflush(stdout);
			}
		}
	}
}


void vuln(){
	char buffer[0x100];
	
	printf("Do you think you are worthy of knowing my secret? ");
	fflush(stdout);
	// fflush(stdin);

	read(0, buffer, 1500);
	// w0 manipulation !
}


void main(void){
	vuln();
	// no "return 0" !!! \o/
}
