#include"function_map.hpp"
#include<cstdint>

extern "C"
uint64_t* wide_1(uint64_t threads, uint64_t * data, uint64_t size, uint64_t arg1, uint64_t arg2, uint64_t arg3) {
    register uint64_t i =0;
    register uint64_t a = arg1;
	for(i = 0; i < size; i++) {
		a = a+i;
		a = a+i;       
		a = a+i;       
		a = a+i;       
		a = a+i;
	}
	data[0] = a;
	return data;
}
FUNCTION(one_array_2arg, wide_1);

extern "C"
uint64_t* wide_2(uint64_t threads, uint64_t * data, uint64_t size, uint64_t arg1, uint64_t arg2, uint64_t arg3) {
	register uint64_t a = arg1;
	register uint64_t b = arg1 << 1;
	register uint64_t c = arg1 << 2;
	register uint64_t d=  arg1 << 3;
	register uint64_t e = arg1 << 4;
	register uint64_t f= size;

	for(register uint64_t i = 0; i < size; i++) {
		a = a+i;  b = b+i;
		a = a+i;  b = b+i;       
		a = a+i;  b = b+i;       
		a = a+i;  b = b+i;       
		a = a+i;  b = b+i;
	}
	data[0] = a + b + c +d + e + f;
	return data;
}
FUNCTION(one_array_2arg, wide_2);

extern "C"
uint64_t* wide_3(uint64_t threads, uint64_t * data, uint64_t size, uint64_t arg1, uint64_t arg2, uint64_t arg3) {
	register uint64_t a = arg1;
	register uint64_t b = arg1 << 1;
	register uint64_t c = arg1 << 2;
	register uint64_t d=  arg1 << 3;
	register uint64_t e = arg1 << 4;
	register uint64_t f= size;

	for(register uint64_t i = 0; i < size; i++) {
		a = a+i;  b = b+i;  c = c+i;
		a = a+i;  b = b+i;  c = c+i;       
		a = a+i;  b = b+i;  c = c+i;       
		a = a+i;  b = b+i;  c = c+i;       
		a = a+i;  b = b+i;  c = c+i;
	}
	data[0] = a + b + c +d + e + f;
	return data;
}
FUNCTION(one_array_2arg, wide_3);

extern "C"
uint64_t* wide_4(uint64_t threads, uint64_t * data, uint64_t size, uint64_t arg1, uint64_t arg2, uint64_t arg3) {
	register uint64_t a = arg1;
	register uint64_t b = arg1 << 1;
	register uint64_t c = arg1 << 2;
	register uint64_t d=  arg1 << 3;
	register uint64_t e = arg1 << 4;
	register uint64_t f= size;

	for(register uint64_t i = 0; i < size; i++) {
		a = a+i;  b = b+i;  c = c+i;  d = d+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i; 
	}
	data[0] = a + b + c +d + e + f;
	return data;
}
FUNCTION(one_array_2arg, wide_4);
extern "C"
uint64_t* wide_5(uint64_t threads, uint64_t * data, uint64_t size, uint64_t arg1, uint64_t arg2, uint64_t arg3) {
	register uint64_t a = arg1;
	register uint64_t b = arg1 << 1;
	register uint64_t c = arg1 << 2;
	register uint64_t d=  arg1 << 3;
	register uint64_t e = arg1 << 4;
	register uint64_t f= size;

	for(register uint64_t i = 0; i < size; i++) {
		a = a+i;  b = b+i;  c = c+i;  d = d+i;  e = e+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i;  e = e+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i;  e = e+i;
		a = a+i;  b = b+i;  c = c+i;  d = d+i;  e = e+i; 
		a = a+i;  b = b+i;  c = c+i;  d = d+i;  e = e+i; 
	}
	data[0] = a + b + c +d + e + f;
	return data;
}

FUNCTION(one_array_2arg, wide_5);
