# Task Assignment Tool
This tool is implemented by Genetic Algorithm. You can use it for Job Scheduling Problem or Assignment Problem.

## Usage

Input format: Columns and rows represent people and jobs, respectively. every cell is the prioritisation score for this
job (score is 0 to n-1). If a number is closer to "n" indicates they more want the task.

```
task1, task2, task3 ...
0, 1, 2 ...
2, 0, 1 ...
1, 0, 2 ...
...
```

#### Assigning jobs

```
python main.py
```

Optional arguments:

| Parameter   |   Default    | Description                               |
|:------------|:------------:|:------------------------------------------|
| -i --input  |   data.csv   | data to use, please include the extension |
| -o --output |  result.csv  | output file name                          |
| -p --p-size |      50      | population size                           |
| -c --c-rate |     0.2      | crossover rate                            |
| -m --m-rate |     0.1      | mutation rate                             |
| -n --n-iter |     1000     | number of iterations                      |

Output example (csv format)

```
n1,n2,n3,n4,n5,n6,n7,n8,n9,n10
t2,t1,t1,t4,t3,t5,t4,t2,t5,t3
t2,t4,t1,t3,t3,t5,t1,t4,t5,t2
... (skip many iteration)
t3,t1,t4,t4,t3,t5,t2,t1,t5,t2
t3,t1,t4,t4,t3,t5,t2,t1,t5,t2
t3,t1,t4,t4,t3,t5,t2,t1,t5,t2
... (skip many iteration)
t2,t4,t4,t3,t3,t5,t1,t1,t5,t2
t2,t4,t4,t3,t3,t5,t1,t1,t5,t2
t2,t4,t4,t3,t3,t5,t1,t1,t5,t2
t2,t4,t4,t3,t3,t5,t1,t1,t5,t2
t2,t4,t4,t3,t3,t5,t1,t1,t5,t2 <- the last iteration is optimal solution
```

#### Generating Simulation data

```
python gen.py
```

Optional arguments:

| Parameter     |      Default       | Description                               |
|:--------------|:------------------:|:------------------------------------------|
| -o --output   | simulated-data.csv | output file name                          |
| -nt --n-tasks |         5          | number of tasks (jobs)                    |
| -ni --n-items |         10         | number of items (persons, machines, etc.) |

Output example (csv format)

```
t1,t2,t3,t4,t5
0,3,2,4,1
3,2,1,4,0
4,1,2,3,0
4,3,1,0,2
3,4,2,0,1
1,3,4,2,0
2,1,3,0,4
1,4,0,2,3
0,1,3,4,2
4,3,1,0,2
```

## Dependencies
* numpy >= 1.20.3
* pandas >= 1.3.4