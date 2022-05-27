#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// #define DEBUG

typedef struct {
	char* name;
	char* type;
} user_t;

int nb_users;
user_t users[8];


void add_user(){
	if(nb_users == 8){
		puts("[-] Maximum users number reached!");
		return;
	}

	char* name = (char*) malloc(50);
	char* type = (char*) malloc(50);

	printf("\n[+] Username: ");
	fflush(stdout);
	fgets(name, 45, stdin);
	name[strcspn(name, "\n")] = '\x00';

	strcpy(type, "user");
	user_t* user = (user_t*) &users[nb_users];
	user->name = name;
	user->type = type;

	printf("[+] Created with user ID n°%d\n", nb_users);
	nb_users++;
}


void remove_user(){
	int id;
	
	printf("\n[+] User ID to delete: ");
	fflush(stdout);
	scanf("%d", &id);
	getchar();

	if(id < 0 || id >= nb_users){
		puts("[-] Invalid user ID.");
		return;
	}

	user_t* user = (user_t*) &users[id];
	free(user->name);
	free(user->type);
	printf("[+] User with ID n°%d was deleted!\n", id);
}


void admin_login(){
	FILE* fd;
	char c;
	int id;

	printf("\n[+] User ID to login with: ");
	fflush(stdout);
	scanf("%d", &id);
	getchar();

	if(id < 0 || id >= nb_users){
		puts("[-] Invalid user ID.");
		return;
	}

	user_t* user = (user_t*) &users[id];

	if(strcmp("admin", user->type)){
		puts("[-] You are not admin.");
		return;
	}

	puts("[+] Welcome back, admin!");

	fd = fopen("flag.txt", "r");
	while((c = fgetc(fd)) != EOF){
		printf("%c", c);
	}
}


void view_users(){
	printf("nb_users: %d\n", nb_users);
	for(int i=0; i < nb_users; i++){
		user_t* user = (user_t*) &users[i];
		printf("- User ID n°%d:\n", i);
		printf("\t- Name: %s\n", user->name);
		printf("\t- Type: %s\n", user->type);
	}
}


int main(void){
	int choice;
	nb_users = 0;

	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stderr, 0, 2, 0);
	
	while(0x1337){
		printf(	"################\n"
			   	"#     Menu     #\n"
			   	"################\n\n"
			#ifdef DEBUG
			 	"0) View users\n"
			#endif
				"1) Create user\n"
			 	"2) Delete user\n"
			 	"3) Admin login\n"
			 	"4) EXIT\n\n"

			 	"--> Your choice: ");
		
		scanf("%d", &choice);
		getchar();

		switch(choice){
			#ifdef DEBUG
				case 0:
					view_users();
					break;
			#endif
			case 1:
				add_user();
				break;
			case 2:
				remove_user();
				break;
			case 3:
				admin_login();
				break;
			case 4:
				return EXIT_SUCCESS;
			default:
				puts("[-] Invalid choice.");
				break;
		}
		puts("\n");
		fflush(stdout);
	}
}
