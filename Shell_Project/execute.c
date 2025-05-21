#include "shell.h"

void execute_command(char *cmd) {
    char *args[MAX_INPUT / 2 + 1];
    int background = 0;
    
    char *token = strtok(cmd, " ");
    int i = 0;
    while (token != NULL) {
        if (strcmp(token, "&") == 0) {
            background = 1;
        } else {
            args[i++] = token;
        }
        token = strtok(NULL, " ");
    }
    args[i] = NULL;
    
    if (i == 0) return;
    
    pid_t pid = fork();
    if (pid == 0) {
        execvp(args[0], args);
        perror("execvp failed");
        exit(EXIT_FAILURE);
    } else if (pid > 0) {
        if (!background) {
            waitpid(pid, NULL, 0);
        }
    } else {
        perror("fork failed");
    }
}
