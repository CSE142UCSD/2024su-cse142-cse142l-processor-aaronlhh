SHELL=/bin/bash
.SUFFIXES:
default:

.PHONY: create-labs

STUDENT_EDITABLE_FILES=select_case_solution.hpp config.make
PRIVATE_FILES=Assignment.key.ipynb admin .git solution bad-solution

COMPILER=$(CXX) 
MICROBENCH_OPTIMIZE= -DHAVE_LINUX_PERF_EVENT_H -I$(PWD) -g $(C_OPTS)
LIBS= -lm -pthread -lboost_program_options -L/usr/lib/ -lboost_system -ldl
BUILD=build/

OPTIMIZE+=-march=x86-64
COMPILER=g++-9
include config.make

.PHONY: autograde
autograde: select_case.exe 
	./select_case.exe -M 3300 -o bench.csv -i 10 -c 65536 -p 134217728 -f select_case_solution_c
	./select_case.exe -M 3300 -o correctness.csv -v -c 1024 2048 -p 32768 131072 262144 -f select_case_solution_c

.PRECIOUS: $(BUILD)%.cpp
.PRECIOUS: $(BUILD)%.s
.PRECIOUS: $(BUILD)%.hpp

$(BUILD)perfstats.o: perfstats.c perfstats.h
	mkdir -p $(BUILD) 
	cp  $< $(BUILD)$<
	$(COMPILER) -DHAVE_LINUX_PERF_EVENT_H -O3 -I$(PWD) $(LIBS) -o $(BUILD)perfstats.o -c $(BUILD)perfstats.c


$(BUILD)%.s: $(BUILD)%.cpp
	mkdir -p $(BUILD) 
#	cp  $< $(BUILD)$<
	$(COMPILER) $(MICROBENCH_OPTIMIZE) $(LIBS) -S $(BUILD)$*.cpp

$(BUILD)%.so: $(BUILD)%.cpp
	mkdir -p $(BUILD) 
	cp *.hpp $(BUILD)
	cp *.h   $(BUILD)
	$(COMPILER)  -DHAVE_LINUX_PERF_EVENT_H $(MICROBENCH_OPTIMIZE) $(LIBS) -rdynamic -fPIC -shared -o $(BUILD)$*.so $(BUILD)$*.cpp
#	$(COMPILER) $(MICROBENCH_OPTIMIZE) $(LIBS) -c -fPIC -o $(BUILD)$*.o $(BUILD)$*.cpp

$(BUILD)%.cpp: %.cpp
	cp $< $(BUILD)
	cp *.hpp $(BUILD)

        
$(BUILD)select_case.o : OPTIMIZE=$(select_case_OPTIMIZE)
$(BUILD)select_case.s : OPTIMIZE=$(select_case_OPTIMIZE)
$(BUILD)select_case_main.o : OPTIMIZE=$(select_case_OPTIMIZE)

select_case.exe:  $(BUILD)select_case_main.o  $(BUILD)select_case.o $(BUILD)perfstats.o
	$(COMPILER) $(select_case_OPTIMIZE) $(BUILD)select_case_main.o  $(BUILD)perfstats.o $(BUILD)select_case.o -o select_case.exe

$(BUILD)run_tests.o : OPTIMIZE=-O3

$(BUILD)%.o: %.cpp
	mkdir -p $(BUILD)
	cp *.hpp $(BUILD) 
	cp  $< $(BUILD)$<
	$(COMPILER)  -DHAVE_LINUX_PERF_EVENT_H $(select_case_OPTIMIZE) $(MICROBENCH_OPTIMIZE) $(LIBS) -o $(BUILD)$*.o -c $(BUILD)$*.cpp


fiddle.exe:  $(BUILD)fiddle.o $(FIDDLE_OBJS) $(BUILD)perfstats.o
	$(COMPILER) $(MICROBENCH_OPTIMIZE)  -DHAVE_LINUX_PERF_EVENT_H $(BUILD)fiddle.o $(BUILD)perfstats.o $(FIDDLE_OBJS) $(LIBS) -o fiddle.exe

array_sort.exe:  $(BUILD)array_sort.o $(BUILD)calculate_sum.o $(BUILD)perfstats.o
	$(COMPILER) -O0  -DHAVE_LINUX_PERF_EVENT_H $(BUILD)array_sort.o $(BUILD)perfstats.o $(BUILD)calculate_sum.o $(LIBS) -o array_sort.exe


#-include $(DJR_JOB_ROOT)/$(LAB_SUBMISSION_DIR)/config.make
clean: 
	rm -f *.exe $(BUILD)*
