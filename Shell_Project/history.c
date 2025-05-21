#include "shell.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern History history;
extern void execute_command(char *command);
extern void execute_with_redirect(char *command);

void add_to_history(const char *cmd) {
    if (history.count < 5) {
        strcpy(history.commands[history.count], cmd);
        history.count++;
    } else {
        for (int i = 0; i < 4; i++) {
            strcpy(history.commands[i], history.commands[i + 1]);
        }
        strcpy(history.commands[4], cmd);
    }
}

// Show most recent command as 1, oldest as 5
void show_history() {
    int display_number = history.count;
    int start = (history.count > 5) ? history.count - 5 : 0;

    for (int i = start; i < history.count; i++, display_number--) {
        printf("%d %s\n", display_number, history.commands[i]);
    }
}

char* get_command_by_number(int num) {
    if (num < 1 || num > history.count || history.count == 0) {
        return NULL;
    }

    // 5 -> 0 (oldest), 4 -> 1, ..., 1 -> history.count - 1 (newest)
    return history.commands[history.count - num];
}
