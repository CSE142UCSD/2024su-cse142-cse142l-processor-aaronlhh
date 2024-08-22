#include <algorithm>
#include <ctime>
#include <iostream>
#include <climits>

#ifdef __cplusplus
extern "C" {
#endif
#include "perfstats.h"
#ifdef __cplusplus
}
#endif
long long calculate_sum(int *data, unsigned int size, int threshold);


int main(int argc, char **argv)
{
    // generate data
//    const unsigned arraySize = 262144;
    int arraySize = atoi(argv[1]);
    int data[arraySize];
    long long sum = 0;

    int iterations = atoi(argv[2]);
    int option = atoi(argv[3]);
    char preamble[1024];
    char epilogue[1024];
    char header[1024];
//    char stat_file[1024];
    char default_filename[] = "stats.csv";
    char *stat_file = default_filename;
    
    for (unsigned c = 0; c < arraySize; ++c)
        data[c] = std::rand();
    //START
    if(option)
        std::sort(data, data + arraySize);
    
    sprintf(header,"size,iterations,sort_or_not,IC,Cycles,CPI,CT,ET,L1_dcache_miss_rate,L1_dcache_misses,L1_dcache_accesses,branches,branch_misses");
    perfstats_print_header(stat_file, header);
    sprintf(preamble, "%d,%d,%d,",arraySize,iterations,option);
    perfstats_init();
    perfstats_enable();

    for (unsigned i = 0; i < iterations; ++i) {
        sum += calculate_sum(data, arraySize, std::rand());
    }
    //END
    perfstats_disable();
    sprintf(epilogue,"\n");
    perfstats_print(preamble, stat_file, epilogue);
    perfstats_deinit();
    std::cout << "sum = " << sum << std::endl;
}

