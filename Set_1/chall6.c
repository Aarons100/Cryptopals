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


char * repeating_key_xor(char * key, char * input, int size) {
	char * result = malloc(size);
	for (int i = 0; i < size; i++) {
		result[i] = input[i] ^ key[i % strlen(key)];
	}
	return result;
}
//computes hamming distance between two integers
int countHammDist(unsigned int n, unsigned int m)
{
	int i=0;
	unsigned int count = 0 ;
	for(i=0; i<8; i++){
		if( (n&1) != (m&1) ) {
   			count++;
		}
		n >>= 1;
		m >>= 1;
	}
	return count;
}
//compute hamming distance between two strings
int hamming_distance(char * input1, char * input2, int size) {

	int result = 0;
	for(int i = 0; i < size; i++) {
		result = result + countHammDist(input1[i],input2[i]);
	}
	return result;
}

int main(int argc, char * argv[]) {
	
	FILE *f = fopen("chall6-b64-decoded.bin", "rb");
	fseek(f, 0, SEEK_END);
	long fsize = ftell(f);
	fseek(f, 0, SEEK_SET);

	char *string = malloc(fsize + 1);
	fread(string, fsize, 1, f);
	fclose(f);

	for(int i = 2; i <= 40; i++) {

		int dist = hamming_distance(&string[0],&string[i],i);

		dist = dist / i;
		printf("key size: %d, hamming distance: %d\n",i, dist);
	}
	//yeah i'm skipping the rest of this challenge, its just repeating key xor...
	return 0;
}