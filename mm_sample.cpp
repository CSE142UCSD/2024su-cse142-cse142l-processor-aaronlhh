
#include"function_map.hpp"
#include"MissMachine.hpp"
#include<cassert>

extern "C"
uint64_t *sample(uint64_t * data, uint64_t size, uint64_t arg1) {
    MissMachine a(8, size);
#define MACHINES 9
    register MissingLink *al = a.links[0*(a.link_count/MACHINES)];
    register MissingLink *bl = a.links[1*(a.link_count/MACHINES)];

    for(unsigned int i = 0; i < 1000; i++) {
        al = al->next;
        bl = bl->next;
    }

    // add up all the pointers to keep the optimizer from optimizing them away.
    // It will totally do it if you give a chance.
    return reinterpret_cast<uint64_t*>(reinterpret_cast<uintptr_t>(al) +
                                       reinterpret_cast<uintptr_t>(bl)
                                       );
}

//-O1
