
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

#undef MACHINES

//START
extern "C"
uint64_t* miss_machines(uint64_t thread_count, uint64_t * data, uint64_t size, uint64_t arg1, uint64_t arg2, uint64_t arg3) {
    MissMachine a(arg1, size);

#define MACHINES  13
//    a.shuffle();
    a.make_links();
    register MissingLink *al = a.links[0* (a.link_count/MACHINES)];
    register MissingLink *bl = a.links[1* (a.link_count/MACHINES)];
    register MissingLink *cl = a.links[2* (a.link_count/MACHINES)];
    register MissingLink *dl = a.links[3* (a.link_count/MACHINES)];
    register MissingLink *el = a.links[4* (a.link_count/MACHINES)];
    register MissingLink *fl = a.links[5* (a.link_count/MACHINES)];
    register MissingLink *gl = a.links[6* (a.link_count/MACHINES)];
    register MissingLink *hl = a.links[7* (a.link_count/MACHINES)];
    register MissingLink *il = a.links[8* (a.link_count/MACHINES)];
    register MissingLink *jl = a.links[9* (a.link_count/MACHINES)];
    register MissingLink *kl = a.links[10*(a.link_count/MACHINES)];
    register MissingLink *ll = a.links[11*(a.link_count/MACHINES)];
    register MissingLink *ml = a.links[12*(a.link_count/MACHINES)];
#define ITERATIONS arg3
    switch(arg2) {
        case 1: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
            }
        }
        break;
        case 2: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
            }
        }
        break;
        case 3: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
            }
        }
        break;
//END
        case 4: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
            }
        }
        break;
        case 5: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
            }
        }
        break;
        case 6: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
            }
        }
        break;
        case 7: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
            }
        }
        break;
        case 8: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
                hl = hl->next;
            }
        }
        break;
        case 9: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
                hl = hl->next;
                il = il->next;
            }
        }
        break;
        case 10: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
                hl = hl->next;
                il = il->next;
                jl = jl->next;
            }
        }
        break;
        case 11: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
                hl = hl->next;
                il = il->next;
                jl = jl->next;
                kl = kl->next;
            }
        }
        break;
        case 12: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
                hl = hl->next;
                il = il->next;
                jl = jl->next;
                kl = kl->next;
                ll = ll->next;
            }
        }
        break;
        case 13: {
            for(unsigned int i = 0; i < ITERATIONS; i++) {
                al = al->next;
                bl = bl->next;
                cl = cl->next;
                dl = dl->next;
                el = el->next;
                fl = fl->next;
                gl = gl->next;
                hl = hl->next;
                il = il->next;
                jl = jl->next;
                kl = kl->next;
                ll = ll->next;
                ml = ml->next;
            }
        }
        break;
        default:
            assert(0);
    }
    return reinterpret_cast<uint64_t*>(reinterpret_cast<uintptr_t>(al) +
                                       reinterpret_cast<uintptr_t>(bl) +
                                       reinterpret_cast<uintptr_t>(cl) +
                                       reinterpret_cast<uintptr_t>(dl) +
                                       reinterpret_cast<uintptr_t>(el) + 
                                       reinterpret_cast<uintptr_t>(fl) + 
                                       reinterpret_cast<uintptr_t>(gl) + 
                                       reinterpret_cast<uintptr_t>(hl) + 
                                       reinterpret_cast<uintptr_t>(il) +
                                       reinterpret_cast<uintptr_t>(jl) +
                                       reinterpret_cast<uintptr_t>(kl) +
                                       reinterpret_cast<uintptr_t>(ll) +
                                       reinterpret_cast<uintptr_t>(ml)
                                       );
} 
FUNCTION(one_array_2arg, miss_machines);


//-O3 
