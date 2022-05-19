#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// #define DEBUG 1

// original code : https://followtutorials.com/2017/11/rsa-algorithm-explained-with-c-code.html
 
typedef struct {
 int d;
 int x;
 int y;
} EE;

 
EE extended_euclid(int a, int b) {
 EE ee1, ee2, ee3;
 if (b == 0) {
  ee1.d = a;
  ee1.x = 1;
  ee1.y = 0;
  return ee1;
 } else {
  ee2 = extended_euclid(b, a % b);
  ee3.d = ee2.d;
  ee3.x = ee2.y;
  ee3.y = ee2.x - floor(a / b) * ee2.y;
  return ee3;
 }
}
 
 
int modulo(int x, int N){
    return (x % N + N) % N;
}

 
void decimal_to_binary(int op1, int aOp[]){
    int result, i = 0;
    do{
        result = op1 % 2;
        op1 /= 2;
        aOp[i] = result;
        i++;
    }while(op1 > 0);
}


int modular_exponentiation(int a, int b, int n){
 int *bb;
 int count = 0, c = 0, d = 1, i;
 
 // find out the size of binary b
 count = (int) (log(b)/log(2)) + 1;
 
 bb = (int *) malloc(sizeof(int*) * count);
 decimal_to_binary(b, bb);
 
 for (i = count - 1; i >= 0; i--) {
  c = 2 * c;
  d = (d*d) % n;
  if (bb[i] == 1) {
   c = c + 1;
   d = (d*a) % n;
  }
 }
 return d;
}


int p, q, phi, n;
char m[8];
int e;
 
int main(int argc, char* argv[]) {
    FILE* fd;
    char c;
    int check = 12345;
    int max = 46340;
    int min = 10000;

    printf("If you can find a value such that encrypt(value) == 12345, I'll give you my flag.\nBut don't try to much, it's impossible: I'm using a home made RSA algorithm with random values!\n");
    fflush(stdout);

    srand(time(NULL));
    p = rand() % (max + 1 - min) + min;
    // more seed = more secure (smart)
    srand(p);
    q = rand() % (max + 1 - min) + min;
    // always more (maximum security !!!)
    srand(q);
    e = rand() % (max + 1 - min) + min;
    // e = 1; // --> overflow to get this !

    n = p*q;
    phi = (p - 1) * (q - 1);

    #ifdef DEBUG
        printf("[+] Generated p : %d\n", p);
        printf("[+] Generated q : %d\n", q);
        printf("[+] Generated n : %d\n", n);
        printf("[+] Generated phi : %d\n", phi);
        printf("[+] Generated e : %d\n", e);
    #endif
        
    printf("Enter a value to encrypt: ");
    fflush(stdout);
    fgets(m, 16, stdin);

        
    #ifdef DEBUG
        printf("[+] e value : %d\n", e);
        printf("[+] Encrypted message is: %d\n", modular_exponentiation(atoi(m), e, n));
    #endif

    if(modular_exponentiation(atoi(m), e, n) == check){
        fd = fopen("flag.txt", "r");
        while((c = fgetc(fd)) != EOF)
            printf("%c", c);
    }else{
        printf("I told you, no one can solve this. You'll never get my flag!\n");
    }
    
    fflush(stdout);
    return 0;
}