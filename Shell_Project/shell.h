#ifndef SHELL_H
#define SHELL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

#define MAX_INPUT 100
#define COMMAND_LENGTH 100

typedef struct {
    char commands[5][COMMAND_LENGTH];
    int count;
} History;

extern History history;

void add_to_history(const char *cmd);
void show_history();
void execute_command(char *cmd);
void execute_with_redirect(char *cmd);
char *get_command_by_number(int num);

#endif // SHELL_H
