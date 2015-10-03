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
//wrapper for atoh_inst
char * atoh(char * input){
	char * result = malloc(strlen(input)/2);

	for(int i = 0; i < strlen(input); i++){
		result[i/2] = (atoh_inst(input[i]) << 4) + atoh_inst(input[i+1]);
		i++;
	}
	return result;
}
//xor's two arrays of bytes
char * xor(char * input1, char * input2, int size) {

	char * result = malloc(size);
	for (int i = 0; i < size; i++){
		result[i] = input1[i] ^ input2[i];
	}
	return result;
}
//single byte xor an array
char * single_byte_xor(char byte, char * input, int size) {

	char * result = malloc(size);
	for (int i = 0; i < size; i++){
		result[i] = input[i] ^ byte;
	}
	return result;
}

int main(int argc, char * argv[]) {
	
	   FILE * fp;
       char * line = NULL;
       size_t len = 0;
       ssize_t read;

       for(int i = 0; i < 0xff; i++){

       fp = fopen("./chall4_encoded.txt", "r");


       if (fp == NULL)
           exit(EXIT_FAILURE);

       while ((read = getline(&line, &len, fp)) != -1) {

       		int size = strlen(line);

			char * hex1 = atoh(line);

			char * result;

			
			result = single_byte_xor(i,hex1,size);


				printf("%s\n",result);
			
				
		}
		 fclose(fp);
	}
		
      
       if (line)
           free(line);
       exit(EXIT_SUCCESS);
	return 0;
}