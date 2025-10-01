// scheduler.c
#include <stdio.h>
#include <stdlib.h>
#include "scheduler.h"

int all_processes_completed(Process *processes, int num_processes) {
    for (int i = 0; i < num_processes; i++) {
        if (!processes[i].completed)
            return 0;
    }
    return 1;
}

void calculate_and_display(Process *processes, int num_processes) {
    double total_turnaround = 0;
    double total_latency = 0;

    printf("PID\tArrival\tBurst\tStart\tFinish\tTurnaround\tLatency\n");

    for (int i = 0; i < num_processes; i++) {
        int turnaround = processes[i].finish_time - processes[i].arrival_time;
        int latency = processes[i].start_time - processes[i].arrival_time;
        printf("%d\t%d\t%d\t%d\t%d\t%d\t\t%d\n",
               processes[i].pid,
               processes[i].arrival_time,
               processes[i].burst_time,
               processes[i].start_time,
               processes[i].finish_time,
               turnaround,
               latency);

        total_turnaround += turnaround;
        total_latency += latency;
    }

    printf("Average Turnaround Time: %.2f\n", total_turnaround / num_processes);
    printf("Average Latency: %.2f\n", total_latency / num_processes);
}

// -------------------- FIFO Implementation -------------------- //
void fifo(Process *processes, int num_processes) {
    int clock = 0;

    for (int i = 0; i < num_processes; i++) {
        // Wait for the process to arrive if needed
        if (clock < processes[i].arrival_time) {
            clock = processes[i].arrival_time;
        }

        processes[i].start_time = clock;
        clock += processes[i].burst_time;
        processes[i].finish_time = clock;
        processes[i].completed = 1;
    }

    calculate_and_display(processes, num_processes);
}

// -------------------- SJF Implementation -------------------- //
void sjf(Process *processes, int num_processes) {
    int clock = 0;
    int completed = 0;

    while (completed < num_processes) {
        int idx = -1;
        int min_remaining = 1000000; // a very large number

        // Find the process with minimum remaining time that has arrived
        for (int i = 0; i < num_processes; i++) {
            if (!processes[i].completed &&
                processes[i].arrival_time <= clock &&
                processes[i].remaining_time < min_remaining) {
                min_remaining = processes[i].remaining_time;
                idx = i;
            }
        }

        if (idx == -1) {
            // No process has arrived yet, move clock forward
            clock++;
            continue;
        }

        // First time the process is running
        if (processes[idx].start_time == -1) {
            processes[idx].start_time = clock;
        }

        // Execute for 1 unit (since SJF is preemptive)
        processes[idx].remaining_time--;
        clock++;

        if (processes[idx].remaining_time == 0) {
            processes[idx].finish_time = clock;
            processes[idx].completed = 1;
            completed++;
        }
    }

    calculate_and_display(processes, num_processes);
}

// -------------------- Round Robin Implementation -------------------- //

// Define a simple queue structure for RR
typedef struct QueueNode {
    int pid;
    struct QueueNode *next;
} QueueNode;

typedef struct Queue {
    QueueNode *front;
    QueueNode *rear;
} Queue;

void enqueue(Queue *q, int pid) {
    QueueNode *new_node = (QueueNode *)malloc(sizeof(QueueNode));
    new_node->pid = pid;
    new_node->next = NULL;

    if (q->rear == NULL) {
        q->front = q->rear = new_node;
    } else {
        q->rear->next = new_node;
        q->rear = new_node;
    }
}

int dequeue(Queue *q) {
    if (q->front == NULL)
        return -1;

    QueueNode *temp = q->front;
    int pid = temp->pid;
    q->front = q->front->next;

    if (q->front == NULL)
        q->rear = NULL;

    free(temp);
    return pid;
}

int is_empty(Queue *q) {
    return (q->front == NULL);
}

void round_robin(Process *processes, int num_processes, int quantum) {
    Queue q = {NULL, NULL};
    int clock = 0;
    int completed = 0;
    int process_in_queue[MAX_PROCESSES] = {0}; // track who is already enqueued

    while (completed < num_processes) {
        // Add new arrivals to the queue
        for (int i = 0; i < num_processes; i++) {
            if (!process_in_queue[i] && processes[i].arrival_time <= clock && !processes[i].completed) {
                enqueue(&q, i);
                process_in_queue[i] = 1;
            }
        }

        if (is_empty(&q)) {
            // No ready process, move clock forward
            clock++;
            continue;
        }

        int idx = dequeue(&q);

        // First time running?
        if (processes[idx].start_time == -1) {
            processes[idx].start_time = clock;
        }

        int exec_time = (processes[idx].remaining_time < quantum) ? processes[idx].remaining_time : quantum;
        for (int t = 0; t < exec_time; t++) {
            clock++;
            // New arrivals during execution
            for (int i = 0; i < num_processes; i++) {
                if (!process_in_queue[i] && processes[i].arrival_time <= clock && !processes[i].completed) {
                    enqueue(&q, i);
                    process_in_queue[i] = 1;
                }
            }
        }

        processes[idx].remaining_time -= exec_time;

        if (processes[idx].remaining_time == 0) {
            processes[idx].finish_time = clock;
            processes[idx].completed = 1;
            completed++;
        } else {
            // Not finished, requeue
            enqueue(&q, idx);
        }
    }

    calculate_and_display(processes, num_processes);
}

// -------------------- Multi-Level Feedback Queue Implementation -------------------- //

#define NUM_QUEUES 4

void move_all_to_top_queue(Queue queues[], int num_queues) {
    QueueNode *new_front = NULL, *new_rear = NULL;

    // Combine all queues into one list maintaining order
    for (int q = 0; q < num_queues; q++) {
        while (!is_empty(&queues[q])) {
            QueueNode *node = queues[q].front;
            if (new_rear == NULL) {
                new_front = new_rear = node;
            } else {
                new_rear->next = node;
                new_rear = node;
            }
            queues[q].front = node->next;
            if (queues[q].front == NULL)
                queues[q].rear = NULL;
        }
    }

    // Set the combined list to the top queue (queue 0)
    queues[0].front = new_front;
    queues[0].rear = new_rear;
}

void mlfq(Process *processes, int num_processes, int base_quantum, int s_value) {
    Queue queues[NUM_QUEUES];
    for (int i = 0; i < NUM_QUEUES; i++) {
        queues[i].front = queues[i].rear = NULL;
    }

    int clock = 0;
    int completed = 0;
    int process_in_queue[MAX_PROCESSES] = {0}; // track who is enqueued
    int s_timer = 0; // time passed since last S reset

    int current_pid = -1; // currently running process
    int current_queue = -1;
    int time_used_in_quantum = 0;

    while (completed < num_processes) {
        // Add newly arrived processes to Queue 1
        for (int i = 0; i < num_processes; i++) {
            if (!process_in_queue[i] && processes[i].arrival_time <= clock && !processes[i].completed) {
                enqueue(&queues[0], i);
                process_in_queue[i] = 1;
                processes[i].last_queue = 1;
            }
        }

        // Check if S time has passed
        if (s_timer == s_value) {
            move_all_to_top_queue(queues, NUM_QUEUES);
            s_timer = 0;
            // After moving all processes, reset their queue levels
            for (int i = 0; i < num_processes; i++) {
                if (!processes[i].completed) {
                    processes[i].last_queue = 1;
                }
            }
        }

        // Check if a new higher priority process arrived -> preempt
        int higher_priority_found = 0;
        for (int q = 0; q < NUM_QUEUES; q++) {
            if (!is_empty(&queues[q])) {
                if (current_queue == -1 || q < current_queue) {
                    higher_priority_found = 1;
                    break;
                }
            }
        }
        if (higher_priority_found && current_pid != -1) {
            // Preempt current process and put it back to its queue
            enqueue(&queues[current_queue], current_pid);
            current_pid = -1;
            current_queue = -1;
            time_used_in_quantum = 0;
        }

        // Select next process if none running
        if (current_pid == -1) {
            for (int q = 0; q < NUM_QUEUES; q++) {
                if (!is_empty(&queues[q])) {
                    current_pid = dequeue(&queues[q]);
                    current_queue = q;
                    time_used_in_quantum = 0;
                    break;
                }
            }
        }

        if (current_pid == -1) {
            // No ready process, advance clock
            clock++;
            s_timer++;
            continue;
        }

        // First time running?
        if (processes[current_pid].start_time == -1) {
            processes[current_pid].start_time = clock;
        }

        // Execute for 1 unit
        processes[current_pid].remaining_time--;
        clock++;
        s_timer++;
        time_used_in_quantum++;

        // Process finished
        if (processes[current_pid].remaining_time == 0) {
            processes[current_pid].finish_time = clock;
            processes[current_pid].completed = 1;
            completed++;
            current_pid = -1;
            current_queue = -1;
            time_used_in_quantum = 0;
        }
        // Time quantum used up, drop to lower queue
        else {
            int current_quantum = base_quantum * (1 << current_queue);
            if (time_used_in_quantum == current_quantum) {
                if (current_queue < NUM_QUEUES - 1) {
                    // Drop to lower queue
                    enqueue(&queues[current_queue + 1], current_pid);
                    processes[current_pid].last_queue = current_queue + 2; // (queue index + 1)
                } else {
                    // Already in lowest queue, stay there
                    enqueue(&queues[current_queue], current_pid);
                }
                current_pid = -1;
                current_queue = -1;
                time_used_in_quantum = 0;
            }
        }
    }

    calculate_and_display(processes, num_processes);
}