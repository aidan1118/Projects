# Shell Project

A simple Unix shell implementation in C that provides basic command execution, history management, and I/O redirection.

## Features

- **Command Execution**: Execute system commands with arguments
- **Background Processes**: Run commands in the background using `&`
- **Command History**: Maintain a history of the last 5 commands
- **History Navigation**: Re-execute previous commands using `r <number>`
- **I/O Redirection**: Redirect output to files using `>`
- **Built-in Commands**:
  - `quit`: Exit the shell
  - `hist`: Display command history

## Building

Compile the shell using the provided Makefile:

```bash
make
```

This creates the `task_shell` executable.

## Usage

Run the shell:

```bash
./task_shell
```

The shell prompt is `>>`. Enter commands as you would in a regular shell.

### Examples

```bash
>> ls -l
>> cat file.txt > output.txt
>> hist
>> r 2
>> sleep 10 &
>> quit
```

## File Structure

- `main.c`: Main shell loop and command parsing
- `execute.c`: Command execution functionality
- `history.c`: Command history management
- `redirect.c`: I/O redirection implementation
- `shell.h`: Header file with function declarations and constants
- `makefile`: Build configuration

## Cleaning

Remove compiled files:

```bash
make clean
```