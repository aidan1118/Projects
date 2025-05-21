#include "shell.h"
#include <ctype.h> // for isdigit()

History history = { .count = 0 };

int main() {
    char input[MAX_INPUT];

    while (1) {
        printf(">> ");
        if (!fgets(input, MAX_INPUT, stdin)) {
            break;
        }

        input[strcspn(input, "\n")] = '\0';
        if (strlen(input) == 0) continue;

        // Handle quit
        if (strcmp(input, "quit") == 0) {
            break;
        }

        // Show command history
        if (strcmp(input, "hist") == 0) {
            show_history();
            continue; // do not add "hist" to history
        }

        // Handle r <number> to rerun a command from history
        if (input[0] == 'r' && isspace(input[1])) {
            int cmd_num = atoi(&input[2]); // expects format like r 3
            char *hist_cmd = get_command_by_number(cmd_num);
            if (hist_cmd) {
                printf(">> %s\n", hist_cmd);

                // ✅ Copy the command BEFORE history is modified
                char temp[COMMAND_LENGTH];
                strncpy(temp, hist_cmd, COMMAND_LENGTH - 1);
                temp[COMMAND_LENGTH - 1] = '\0';

                // Execute the copied command
                if (strchr(temp, '>')) {
                    execute_with_redirect(temp);
                } else {
                    execute_command(temp);
                }

                // ✅ Now safely add it to history
                add_to_history(temp);
            } else {
                printf("No such command in history.\n");
            }
            continue;
        }

        // Add the current command to history
        // Avoid double history update for 'r N'
        if (!(input[0] == 'r' && isspace(input[1]))) {
            add_to_history(input);
        }

        // Handle redirection
        if (strchr(input, '>')) {
            execute_with_redirect(input);
        } else {
            execute_command(input);
        }
    }

    return 0;
}