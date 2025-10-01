# CPU Scheduling Simulator

This project is a CPU scheduling algorithms simulator that implements and compares four different process scheduling policies: FIFO (First-In-First-Out), SJF (Shortest-Job-First), Round Robin, and MLFQ (Multi-Level Feedback Queue). The program reads process arrival times and burst times from an input file, then runs each scheduling algorithm to calculate execution timelines, turnaround times, and latency metrics. It demonstrates key operating systems concepts like preemption, time-slicing, priority queues, and starvation prevention mechanisms used in modern CPU schedulers.

## Files Structure

- `main.c` - Main program entry point and input file parsing
- `scheduler.c` - Implementation of all four scheduling algorithms
- `scheduler.h` - Header file for scheduler functions
- `process.h` - Process structure definition and constants
- `makefile` - Build configuration
- `test1_basic.txt` - Basic test case input file
- `test2_preemption.txt` - Test case for preemption scenarios
- `test3_starvation.txt` - Test case for starvation prevention

## Building the Project

To compile the simulator, use the provided makefile:

```bash
make
```

This will create an executable named `scheduler_simulator`.

To clean build artifacts:

```bash
make clean
```

## Running the Simulator

Run the simulator with an input file:

```bash
./scheduler_simulator <input_file>
```

Example:

```bash
./scheduler_simulator test1_basic.txt
```

## Input File Format

The input file should contain:
1. Number of processes
2. Each process on a separate line: `arrival_time,burst_time`
3. Round Robin time quantum
4. MLFQ time quantum
5. MLFQ S value (time threshold for queue demotion)

Example input file:
```
3
0,5
1,3
2,8
2
1
10
```

## Test Cases

- `test1_basic.txt` - Basic scheduling scenario
- `test2_preemption.txt` - Tests preemptive scheduling behavior
- `test3_starvation.txt` - Tests starvation prevention mechanisms

## Scheduling Algorithms

1. **FIFO (First-In-First-Out)** - Non-preemptive, processes run in arrival order
2. **SJF (Shortest-Job-First)** - Non-preemptive, shortest burst time first
3. **Round Robin** - Preemptive with configurable time quantum
4. **MLFQ (Multi-Level Feedback Queue)** - Multi-level queues with aging mechanism

The simulator outputs execution timelines, turnaround times, and average latency for each algorithm.