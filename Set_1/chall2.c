//Aaron Sedlacek
//10/02/2015
// I got kinda lazy, this sample just takes a hex string and makes bytes
#include "stdio.h"
#include "ctype.h"
#include "string.h"
#include "stdlib.h"

//converts ascii char to hex equiv
int atoh_inst(char input){

	if('0' <= input && input <= '9' ) {
		int foo = input;

		foo = foo - '0';
		return foo;
	}

	else {
		int foo = input;
		foo = toupper(input); 
		foo = foo - 'A' + 10;
		return foo;
	}
}

char * atoh(char * input){
	char * result = malloc(strlen(input)/2);

	for(int i = 0; i < strlen(input); i++){
		result[i/2] = (atoh_inst(input[i]) << 4) + atoh_inst(input[i+1]);
		i++;
	}

	return result;
}

char * xor(char * input1, char * input2, int size) {

	char * result = malloc(size);
	for (int i = 0; i < size; i++){
		result[i] = input1[i] ^ input2[i];

	}
	return result;
}

int main(int argc, char * argv[]) {
	
	char * input1 = argv[1];
	char * input2 = argv[2];

	int size = strlen(input1);

	char * hex1 = atoh(input1);
	char * hex2 = atoh(input2);

	char * result = xor(hex1,hex2,size);

	printf("input 1: ");
	for(int i = 0; i < size/2; i++){
		printf("%x ",hex1[i]);	
	}
	printf("\n");

	printf("input 2: ");
	for(int i = 0; i < size/2; i++){
		printf("%x ",hex2[i]);	
	}
	printf("\n");

	printf("result: ");
	for(int i = 0; i < size/2; i++){
		printf("%x ",result[i]);	
	}
	printf("\n");


	return 0;
}