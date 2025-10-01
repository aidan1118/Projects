// scheduler.h
#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "process.h"

void fifo(Process *processes, int num_processes);
void sjf(Process *processes, int num_processes);
void round_robin(Process *processes, int num_processes, int quantum);
void mlfq(Process *processes, int num_processes, int base_quantum, int s_value);

#endif