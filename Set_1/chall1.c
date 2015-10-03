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

int main(int argc, char * argv[]) {
	
	char * input = argv[1];

	int size = strlen(input);
	char * hex = atoh(input);

	printf("%s\n%s\n",input,hex);

	return 0;
}