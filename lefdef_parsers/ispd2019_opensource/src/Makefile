WFLAG  = -Wall -Werror
CFLAG  = 
TARGET = bin/ispd19eval
# OPT  = -O3 -static -DNDEBUG  
OPT  = -O3 -DNDEBUG 
LIBS = -pthread
RM    = rm
BISON = bison
FLEX  = flex
AR    = ar rcs
TAG   = ctags
CC    = g++ -std=c++11 $(OPT) $(WFLAG) $(CFLAG) -I.

CC_OBJS = main.o
IO_OBJS = io/io.o io/lef.o io/def.o io/rpt.o io/guide.o io/weight.o
DB_OBJS = db/db.o db/net.cpp #db/guide.o

DEF_OBJS = lefdef/def/lib/libdef.a
LEF_OBJS = lefdef/lef/lib/liblef.a
LIB_OBJS = $(DEF_OBJS) $(LEF_OBJS)

OBJS = $(CC_OBJS) $(IO_OBJS) $(DB_OBJS) $(LIB_OBJS)

SRCS = ${OBJS:%.o=%.cpp}
BFILE = ispd19eval
AFILE = ispa19eval.a

define copy_build
	mkdir -p ../$(TARGET)
	mv -u $(BFILE) ../$(TARGET)/
	cp -u data/* ../$(TARGET)/
endef

.PHONY: all
all: $(BFILE)

.PHONY: install
install: $(BFILE)
	$(call copy_build)

#$(BFILE): $(DEF_OBJS) $(LEF_OBJS) $(OBJS)
$(BFILE): $(OBJS)
	$(CC) -o $(BFILE) $(OBJS) $(LIB_OBJS) $(LIBS)
	$(call copy_build)

#$(LEF_OBJS):
.PHONY: lef
lef:
	make -C lefdef/lef release

#$(DEF_OBJS):
.PHONY: def
def:
	make -C lefdef/def release

%.o : %.cpp
	$(CC) -o $*.o -c $*.cpp

.PHONY: clean
clean:
	$(RM) -f */*.o *.o
	$(RM) -f $(BFILE) $(AFILE) core.*

.PHONY: cleanall
cleanall:
	$(RM) -f */*.o *.o
	$(RM) -f $(BFILE) $(AFILE) core.*
	make -C lefdef/lef clean
	make -C lefdef/def clean
