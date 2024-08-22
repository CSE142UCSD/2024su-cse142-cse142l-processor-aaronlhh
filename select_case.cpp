#include"select_case_reference.hpp"
#include"select_case_solution.hpp"
#include <vector>

#define ELEMENT_TYPE uint64_t

typedef std::tuple<int, int> Bench;

std::vector<Bench> benches = {
    std::make_tuple(600, 2),
    std::make_tuple(350, 25),
    std::make_tuple(120, 100),
};

extern "C"
void select_case_reference_c(order *orders, uint64_t o_records, output *result)
{
    {
        select_case_reference(orders, o_records, result);
    }
}
FUNCTION(join, select_case_reference_c);


extern "C"
void select_case_solution_c(order *orders, uint64_t o_records, output *result)
{
    {
        select_case_solution(orders, o_records, result);
    }
}
FUNCTION(join, select_case_solution_c);
