# makefile

CC = gcc
CFLAGS = -Wall -Wextra -g
OBJ = main.o scheduler.o
TARGET = scheduler_simulator

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

main.o: main.c process.h scheduler.h
	$(CC) $(CFLAGS) -c main.c

scheduler.o: scheduler.c scheduler.h process.h
	$(CC) $(CFLAGS) -c scheduler.c

clean:
	rm -f $(OBJ) $(TARGET)