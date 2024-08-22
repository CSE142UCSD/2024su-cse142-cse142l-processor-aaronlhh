#include <cstdlib>
#include "archlab.h"
#include <unistd.h>
#include <algorithm>
#include <cstdint>
#include "function_map.hpp"
#include <dlfcn.h>
#include <vector>
#include <sstream>
#include <string>
#include "perfstats.h"
#include "table_struct.h"


#define ELEMENT_TYPE uint64_t

uint array_size;

typedef void(*select_case_impl)(order *orders, uint64_t o_records, output *result);

order *init_orders(uint32_t x_size, uint32_t y_size);
product *init_products(uint32_t x_size, uint32_t y_size);
output *init_results(uint32_t x_size);
void free_data(int64_t **M, uint32_t size);
bool compare_data(output *M, output *N, uint32_t x_size);
int main(int argc, char *argv[])
{
    int i, reps=1, iterations=1,mhz, c_size, p_size, b_size, verify =0;
    char *stat_file = NULL;
    char default_filename[] = "stats.csv";
    char preamble[1024];
    char epilogue[1024];
    char header[1024];
    std::stringstream clocks;
    std::vector<std::string> functions;
    std::vector<std::string> default_functions;
    std::vector<int> mhz_s;
    std::vector<int> default_mhz;
    std::vector<unsigned long int> c_sizes;
    std::vector<unsigned long int> default_c_sizes;
    std::vector<unsigned long int> p_sizes;
    std::vector<unsigned long int> default_p_sizes;
    std::vector<unsigned long int> b_sizes;
    std::vector<unsigned long int> default_b_sizes;
    default_c_sizes.push_back(65536);
    default_p_sizes.push_back(131072);
    default_b_sizes.push_back(1);
    order *orders; 
    product *products;
    output *results, *verification;

    float minv = -1.0;
    float maxv = 1.0;
    std::vector<uint64_t> seeds;
    std::vector<uint64_t> default_seeds;
    default_seeds.push_back(0xDEADBEEF);
    
    for(i = 1; i < argc; i++)
    {
            // This is an option.
        if(argv[i][0]=='-')
        {
            switch(argv[i][1])
            {
                case 'o':
                    if(i+1 < argc && argv[i+1][0]!='-')
                        stat_file = argv[i+1];
                    break;
                case 'r':
                    if(i+1 < argc && argv[i+1][0]!='-')
                        reps = atoi(argv[i+1]);
                    break;
                case 'c':
                    for(;i+1<argc;i++)
                    {
                        if(argv[i+1][0]!='-')
                        {
                            c_size = atoi(argv[i+1]);
                            c_sizes.push_back(c_size);
                        }
                        else
                            break;
                    }
                    break;
                case 'p':
                    for(;i+1<argc;i++)
                    {
                        if(argv[i+1][0]!='-')
                        {
                            p_size = atoi(argv[i+1]);
                            p_sizes.push_back(p_size);
                        }
                        else
                            break;
                    }
                    break;
/*                case 'b':
                    for(;i+1<argc;i++)
                    {
                        if(argv[i+1][0]!='-')
                        {
                            b_size = atoi(argv[i+1]);
                            b_sizes.push_back(b_size);
                        }
                        else
                            break;
                    }
                    break;*/
                case 'M':
                    for(;i+1<argc;i++)
                    {
                        if(argv[i+1][0]!='-')
                        {
                            mhz = atoi(argv[i+1]);
                            mhz_s.push_back(mhz);
                        }
                        else
                            break;
                    }
                    break;
                case 'f':
                    for(;i+1<argc;i++)
                    {
                        if(argv[i+1][0]!='-')
                        {
                            functions.push_back(std::string(argv[i+1]));
                        }
                    else
                        break;
                    }
                    break;
                case 'i':
                    if(i+1 < argc && argv[i+1][0]!='-')
                        iterations = atoi(argv[i+1]);
                    break;
                case 'h':
                    std::cout << "-s set the size of the source matrix.\n-k set the kernel matrix size.\n-f what functions to run.\n-d sets the random seed.\n-o sets where statistics should go.\n-i sets the number of iterations.\n-v compares the result with the reference solution.\n";
                    break;
                case 'v':
                    verify = 1;
                    break;
                }
            }
        }
    if(stat_file==NULL)
        stat_file = default_filename;

    if (std::find(functions.begin(), functions.end(), "ALL") != functions.end()) {
        functions.clear();
        for(auto & f : function_map::get()) {
            functions.push_back(f.first);
        }
    }
    
    for(auto & function : functions) {
        auto t= function_map::get().find(function);
        if (t == function_map::get().end()) {
            std::cerr << "Unknown function: " << function <<"\n";
            exit(1);
        }
        std::cerr << "Gonna run " << function << "\n";
    }
    if(c_sizes.size()==0)
        c_sizes = default_c_sizes;
    if(p_sizes.size()==0)
        p_sizes = default_p_sizes;
    if(b_sizes.size()==0)
        b_sizes = default_b_sizes;
    if(seeds.size()==0)
        seeds = default_seeds;
    if(functions.size()==0)
        functions = default_functions;

    if(verify == 1)
                sprintf(header,"customers,orders,function,iterations,IC,Cycles,CPI,CT,ET,L1_dcache_miss_rate,L1_dcache_misses,L1_dcache_accesses,branches,branch_misses,correctness");
    else
        sprintf(header,"customers,orders,function,iterations,IC,Cycles,CPI,CT,ET,L1_dcache_miss_rate,L1_dcache_misses,L1_dcache_accesses,branches,branch_misses");
    perfstats_print_header(stat_file, header);
     
    for(auto & seed: seeds ) {
        for(auto & c_size:c_sizes) {
            for(auto & p_size: p_sizes ) {
                for(auto & b_size: b_sizes ) {
                    orders = init_orders(c_size, p_size);
                    for(auto & function : functions) {
                        results = init_results(p_size);
                        std::cerr << "Running: " << function << "\n";
                        function_spec_t f_spec = function_map::get()[function];
                        auto fut = reinterpret_cast<select_case_impl>(f_spec.second);
                        sprintf(preamble, "%lu,%lu,%s,%d,",c_size,p_size,function.c_str(),iterations);
                        perfstats_init();
                        perfstats_enable(1);
                        for(int k=0;k<iterations;k++)
                        fut(orders, p_size, results);
                        perfstats_disable(1);
                        if(verify)
                        {
                            if(function.find("select_case_solution_c") != std::string::npos)
                            {
                                function_spec_t t = function_map::get()[std::string("select_case_reference_c")];
                                auto verify_fut = reinterpret_cast<select_case_impl>(t.second);                        
                                verification = init_results(p_size);
                                verify_fut(orders, p_size, verification);
                                if(compare_data(results,verification,b_size))
                                {
                                    std::cerr << "Passed!!\n";
                                    sprintf(epilogue,",1\n");
                                }
                                else
                                {
                                    std::cerr << "Reference solution does not agree with your optimization!\n";
                                    sprintf(epilogue,",-1\n");
                                }
                                free(verification);
                            }
                            else
                                sprintf(epilogue,",0\n");
                        }
                        else
                            sprintf(epilogue,"\n");
                        perfstats_print(preamble, stat_file, epilogue);
                        perfstats_deinit();
                        std::cerr << "Done execution: " << function << "\n";
                        free(results);
                    }
                    free(orders);
//                    free(products);
                }
            }
        }
    }
    return 0;
}

bool compareByCutomerID(const order &a, const order &b)
{
    if (a.customer_id < b.customer_id)
        return true;
    if (a.customer_id == b.customer_id)
        return a.product_id < b.product_id;
    return false;
}

bool compareByProductID(const product &a, const product &b)
{
    return a.product_id < b.product_id;
}


//START_INIT
order *init_orders(uint32_t x_size, uint32_t y_size)
{
    order *data;
    int64_t i,j;
    uint64_t seed;
    int64_t number_of_orders = y_size;
    data = (order *)malloc(number_of_orders*sizeof(order));
    j=0;
    for(i=0;i<number_of_orders;i++)
    {
        data[i].customer_id = fast_rand(&seed) % x_size;
        data[i].product_id =fast_rand(&seed) % y_size;
        data[i].quantity =fast_rand(&seed) & 0x7f;
    }
    std::sort(data, data+number_of_orders, compareByCutomerID);
//    for(i=0;i<number_of_orders;i++)
//        fprintf(stderr, "%lu: %lu %lu %lu\n", i, data[i].customer_id,data[i].product_id,data[i].quantity);
    return data;
}


product *init_products(uint32_t x_size, uint32_t y_size)
{
    product *data;
    int64_t i,j;
    uint64_t seed;
    data = (product *)malloc(x_size*sizeof(product));
    j=0;
    for(i=0;i<x_size;i++)
    {
        data[i].product_id = fast_rand(&seed) % x_size;
        data[i].brand =fast_rand(&seed) % y_size;
        data[i].price =fast_rand(&seed) & 0xff;
        while(data[i].price == 0) data[i].price =fast_rand(&seed) & 0xff;
        std::sort(data, data+x_size, compareByProductID);
    }
    for(i=0;i<x_size;i++)
    {
        if(i!=0 && data[i-1].product_id == data[i].product_id)
            data[i].product_id += 1;
//        fprintf(stderr, "%lu: %lu %lu %lu\n", i, data[i].product_id,data[i].brand,data[i].price);
        
    }
    return data;
}
//END_INIT


output *init_results(uint32_t x_size)
{
    output *data;
    data = (output *)calloc(x_size,sizeof(output));
    return data;
}

void free_data(int64_t **M, uint32_t size)
{
    uint32_t i;
//    for(i=0;i<size;i++)
//        free(M[i]);
    free(M[0]);
}

bool compare_data(output *M, output *N, uint32_t size)
{
    uint32_t i,j;
    for(i=0;i<size;i++)
    {
        memcmp(&M[i], &N[i], sizeof(output));
    }
    return true;
}