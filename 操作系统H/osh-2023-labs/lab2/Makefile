CC=g++
CFLAGS=-c -Wall
SOURCES=shell.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=shell

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f *o $(EXECUTABLE)