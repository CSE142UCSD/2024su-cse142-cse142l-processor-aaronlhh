#ifndef FAST_URBG_INCLUDED
#define FAST_URBG_INCLUDED

#include<cstdint>

class fast_URBG {
	uint64_t seed;
public:
	fast_URBG(uint64_t seed=1): seed(seed){}
	
	typedef uint64_t result_type;
	static uint64_t min() { return 0;}
	static uint64_t max() { return (uint64_t)(-1);}
	uint64_t operator()() {
		return fast_rand(&seed);
	}
};


#endif
