#-*- Makefile -*-
ARCHLAB=$(ARCHLAB_ROOT)
PCM_ROOT=$(ARCHLAB)/pcm
PAPI_ROOT=/usr/local
PIN_ROOT=$(ARCHLAB)/pin
export PIN_ROOT

GPROF?=no
ifeq ($(GPROF),no)
else
PROFILE_FLAGS+=-pg
DEBUG?=no
endif

GCOV?=no
ifeq ($(GCOV),no)
else
PROFILE_FLAGS+= -fprofile-arcs -ftest-coverage
DEBUG?=yes
endif

DEBUG?=yes
ifeq ($(DEBUG),yes)
DEBUG_FLAGS=-DDEBUG
else
C_OPTS ?= -O3 
endif

AUTO_VEC?=no
ifeq ($(AUTO_VEC),yes)
AUTO_VEC_FLAGS=-fopt-info-vec-all
else
AUTO_VEC_FLAGS?=
endif

OPENMP?=no
ifeq ($(OPENMP),yes)
OPENMP_OPTS=-fopenmp
OPENMP_LIBS=-lgomp
else
OPENMP_OPTS=
OPENMP_LIBS=
endif

CFLAGS ?=  -Wall -Werror -g $(EXTRA) $(C_OPTS) $(PROFILE_FLAGS) $(DEBUG_FLAGS) $(AUTO_VEC_FLAGS) -I$(PCM_ROOT) -pthread $(OPENMP_OPTS) -I$(ARCHLAB)/libarchlab -I$(ARCHLAB) -I$(PAPI_ROOT)/include $(USER_CFLAGS) $(LAB_CFLAGS) #-fopenmp
CXXFLAGS ?=$(CFLAGS) -std=gnu++11
ARCHLAB_LDFLAGS= -L$(PAPI_ROOT)/lib -L$(ARCHLAB)/libarchlab -L$(PCM_ROOT) -larchlab -lpcm -lpapi -lboost_program_options $(OPENMP_LIBS) 
GENERIC_LDFLAGS= $(USER_LDFLAGS) $(LD_OPTS) $(PROFILE_FLAGS) -pthread #-fopenmp
LDFLAGS ?= $(GENERIC_LDFLAGS) $(ARCHLAB_LDFLAGS)

ASM_FLAGS=
CPP_FLAGS=
.PRECIOUS: %.o %.exe %.s %.i
.PHONY: default

default:

ifeq ($(shell uname -s),Darwin)
ifeq ($(FORCE),) 
$(error You cannot compile code with archlab on an Mac.  Instead, develop inside the course docker container (FORCE=yes to override))
endif
endif

#%.o : %.cpp
#	$(CC) -c $(CFLAGS) $(ASM_FLAGS) $< -o $@

%.o : %.cpp
	$(CXX) -c $(CXXFLAGS)  $< -o $@

%.o : %.c
	$(CC) -c $(CFLAGS)  $< -o $@

%.i : %.cpp
	$(CXX) -E -c $(CXXFLAGS) $(CPP_FLAGS) $< -o $@
%.i : %.c
	$(CC) -E -c $(CFLAGS) $(CPP_FLAGS) $< -o $@
%.s : %.asm
	cp $< $@

%.s : %.cpp
	$(CXX) -S -c $(CXXFLAGS) $(ASM_FLAGS) -g0 $< -o $@

%.s : %.c
	$(CC) -S -c $(CFLAGS) $(ASM_FLAGS) -g0 $< -o $@

%.pin-trace: %.exe
	pin -t $(ARCHLAB)/pin-tools/obj-intel64/trace_archlab.so -o $@ -- $(abspath $<) $(TRACE_ARGS) --engine pin

%.trace.s: %.trace
	cp $< $@

%.d: %.c
	 @set -e; rm -f $@; \
         $(CC) -MM $(CXXFLAGS) $< > $@.$$$$; \
         sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
         rm -f $@.$$$$

%.d: %.cpp
	@set -e; rm -f $@; \
         $(CXX) -MM $(CXXFLAGS) $< > $@.$$$$; \
         sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
         rm -f $@.$$$$

### Rules for the rename-x86

RENAME_FLAGS?= 

.PRECIOUS: %.gv %.pin-trace 

#%.gv %.csv: %.s
#	rename-x86.py --dot $*.gv --csv $*.csv $(RENAME_FLAGS) < $<  || rm -rf $*.gv $*.csv 

%.gv %.csv: %.pin-trace
	rename-x86.py --dot $*.gv --pin-trace --csv $*.csv $(RENAME_FLAGS) < $< 


%-gv.pdf: %.gv
	dot -Tpdf $< > $@ || rm -rf $@

%-gv.svg: %.gv
	dot -Tsvg $< > $@ || rm -rf $@

rename-clean:
	rm -rf *.gv *-gv.pdf *.pin-trace #*.csv 

clean: rename-clean

.PHONY: %.out
%.out : %.exe %.i %.s 
	(./$< --stats-file $*-stats.csv $(CMD_LINE_ARGS) > $@ 2>&1)
	pretty-csv $*-stats.csv >> $@
	cat $@

ifeq ($(GPROF),yes)
	gprof ./$< > $*.gprof
endif

.PHONY: archlab-clean
archlab-clean:
	rm -rf *.exe *.o *.i *.s *.out *.d *.gcda *.gcno *.gprof *.gcov *.csv.raw core	

clean: archlab-clean

.PHONY: help

help:
	@echo 'make clean     : cleanup'
	@echo 'make DEBUG=no  : Disable debugging mode (currently=$(DEBUG))'
	@echo 'make GPROF=yes : Enable gprof.  Implies DEBUG=no. (currently=$(GPROF))'
	@echo 'make GCOV=yes  : Enable gcov. (currently=$(GCOV))'


