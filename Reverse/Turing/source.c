#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv){
	if(argc != 2){
		printf("usage: %s <flag>\n", argv[0]);
		return EXIT_FAILURE;
	}

	if(argv[1][0] != 'I' || argv[1][1] != '_' || argv[1][2] != 'l' || argv[1][3] != '1' || argv[1][4] != 'k' || argv[1][5] != '3' || argv[1][6] != '_' ||
	   argv[1][7] != 't' || argv[1][8] != '0' || argv[1][9] != '_' || argv[1][10] != 'm' || argv[1][11] != '0' || argv[1][12] != 'v' || argv[1][13] != '3' || 
	   argv[1][14] != '_' || argv[1][15] != '1' || argv[1][16] != 't' || argv[1][17] != '!')
	
	{
		puts("[-] Nope.");
		return EXIT_FAILURE;
	}	

	printf("[+] Well done ! The flag is Hero{%s}\n", argv[1]);
	return EXIT_SUCCESS;
}
