#include <stdio.h>
#include <stdlib.h>
#include <uuid/uuid.h>
#include <unistd.h>

#define NB_PATCHES 3

// gcc -o sELF_control sELF_control.c -luuid

int main(){
	uuid_t binuuid;
	int ch;
	long int offset;
	unsigned int value;
	char* uuid;
	char execute[88], xxd[48];
	FILE *original, *copy;

	printf( "██╗  ██╗███████╗██████╗  ██████╗  ██████╗████████╗███████╗\n"
			"██║  ██║██╔════╝██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝\n"
			"███████║█████╗  ██████╔╝██║   ██║██║        ██║   █████╗  \n"
			"██╔══██║██╔══╝  ██╔══██╗██║   ██║██║        ██║   ██╔══╝  \n"
			"██║  ██║███████╗██║  ██║╚██████╔╝╚██████╗   ██║   ██║     \n"
			"╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝   ╚═╝     \n");
	printf("================ sELF control (by SoEasY) ================\n\n");
	fflush(stdout);

	uuid = (char*) malloc(37);
	uuid_generate_random(binuuid);
	uuid_unparse(binuuid, uuid);

	original = fopen("/self/EXECUTE_ME", "rb");
	copy = fopen(uuid, "wb");

	if(original == NULL){
		printf("[-] Impossible to open the original file.\n");
		return 1;
	}

	while((ch = fgetc(original)) != EOF)
		fputc(ch, copy);

	fclose(original);
	fclose(copy);

	for(int i=0; i < NB_PATCHES; i++){
		copy = fopen(uuid, "r+");
		offset = 0;

		if(copy == NULL){
			printf("[-] Impossible to open the temporary file.\n");
			return 1;
		}
	
		printf("\nPosition of the byte to patch in hex (example: %02X) : ", rand() % 32);
		fflush(stdout);
		scanf("%lx", &offset);
		printf("Value to put at this offset in hex (example: %02X) : ", rand() % 32);
		fflush(stdout);
		scanf("%x", &value);

		fseek(copy, offset, SEEK_SET);
		fputc(value, copy);
	
		fclose(copy);
	}

	// printf("\n[+] ELF header : \n");
	// sprintf(xxd, "xxd %s | head\0", uuid);
	// system(xxd);

	printf("\n[+] Execution : \n");
	fflush(stdout);
	sprintf(execute, "chmod +x %s && ./%s", uuid, uuid);
	system(execute);
	
	remove(uuid);
	return 0;
}