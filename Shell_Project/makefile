CC = gcc
CFLAGS = -Wall -Wextra -std=c99

OBJS = main.o execute.o history.o redirect.o

task_shell: $(OBJS)
	$(CC) $(CFLAGS) -o task_shell $(OBJS)

main.o: main.c shell.h
	$(CC) $(CFLAGS) -c main.c

execute.o: execute.c shell.h
	$(CC) $(CFLAGS) -c execute.c

history.o: history.c shell.h
	$(CC) $(CFLAGS) -c history.c

redirect.o: redirect.c shell.h
	$(CC) $(CFLAGS) -c redirect.c

clean:
	rm -f *.o task_shell

