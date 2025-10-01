// process.h
#ifndef PROCESS_H
#define PROCESS_H

#define MAX_PROCESSES 100

typedef struct Process {
    int pid;            // Process ID
    int arrival_time;   // Time process arrives
    int burst_time;     // Original burst time
    int remaining_time; // Remaining time for preemptive scheduling
    int start_time;     // When the process first starts execution
    int finish_time;    // When the process finishes
    int last_queue;     // For MLFQ: current queue level (1-4)
    int time_in_queue;  // For MLFQ: time used in current queue quantum
    int completed;      // 0 = not completed, 1 = completed
} Process;

#endif