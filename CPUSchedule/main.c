// main.c
#include <stdio.h>
#include <stdlib.h>
#include "process.h"
#include "scheduler.h"

void read_input(const char *filename, Process *processes, int *num_processes, int *rr_quantum, int *mlfq_quantum, int *mlfq_s_value) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    fscanf(file, "%d", num_processes);
    for (int i = 0; i < *num_processes; i++) {
        fscanf(file, "%d,%d", &processes[i].arrival_time, &processes[i].burst_time);
        processes[i].pid = i;
        processes[i].remaining_time = processes[i].burst_time;
        processes[i].start_time = -1;
        processes[i].finish_time = -1;
        processes[i].completed = 0;
        processes[i].last_queue = 1;
        processes[i].time_in_queue = 0;
    }

    fscanf(file, "%d", rr_quantum);
    fscanf(file, "%d", mlfq_quantum);
    fscanf(file, "%d", mlfq_s_value);

    fclose(file);
}

void reset_processes(Process *original, Process *copy, int num_processes) {
    for (int i = 0; i < num_processes; i++) {
        copy[i] = original[i];
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    Process original[MAX_PROCESSES];
    Process temp[MAX_PROCESSES];
    int num_processes;
    int rr_quantum;
    int mlfq_quantum;
    int mlfq_s_value;

    read_input(argv[1], original, &num_processes, &rr_quantum, &mlfq_quantum, &mlfq_s_value);

    printf("First-In-First-Out (FIFO) Scheduling:\n");
    reset_processes(original, temp, num_processes);
    fifo(temp, num_processes);
    printf("\n");

    printf("Shortest-Job-First (SJF) Scheduling:\n");
    reset_processes(original, temp, num_processes);
    sjf(temp, num_processes);
    printf("\n");

    printf("Round Robin Scheduling:\n");
    reset_processes(original, temp, num_processes);
    round_robin(temp, num_processes, rr_quantum);
    printf("\n");

    printf("Multi-Level Feedback Queue (MLFQ) Scheduling:\n");
    reset_processes(original, temp, num_processes);
    mlfq(temp, num_processes, mlfq_quantum, mlfq_s_value);
    printf("\n");

    return 0;
}
