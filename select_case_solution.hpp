#ifndef select_case_SOLUTION_INCLUDED
#define select_case_SOLUTION_INCLUDED
#include <cstdlib>
#include "archlab.h"
#include <unistd.h>
#include<cstdint>
#include"function_map.hpp"
#include "table_struct.h"



#define TILE_SIZE 64
//template<typename T>
void __attribute__((noinline)) select_case_solution(order *orders, uint64_t o_records, output *result) {
    double discount = 0;
    for(int32_t i = 0; i < o_records; i++) {        
        if(result[i].quantity > 20 && result[i].quantity <= 35)
            discount = 0.95;
        else if(result[i].quantity > 35 && result[i].quantity <= 50)
            discount = 0.9;
        else if(result[i].quantity > 50 && result[i].quantity <= 65)
            discount = 0.85;
        else if(result[i].quantity > 65 && result[i].quantity <= 80)
            discount = 0.8;
        else if(result[i].quantity > 80 && result[i].quantity <= 100)
            discount = 0.75;
        else if(result[i].quantity > 100)
            discount = 0.7;
        else
            discount = 1;
        result[i].quantity = orders[i].quantity;
        result[i].customer_id = orders[i].customer_id;
        result[i].product_id = orders[i].product_id;
        result[i].discount = discount;
    }
    return;
}

#endif
