import csv
import pandas as pd
import config
from args import parse_args
from algorithm import GeneticAlgorithm, SelectionType, CrossoverType, MutationType


class Problem:
    def __init__(self, data):
        self._data = data.values
        self._n_items = len(data.values)
        self._n_tasks = len(data.columns)

    def compute_obj_value(self, X):
        count, val = 0, 0
        for item in X:
            val += self._data[item][count]
            count += 1
            if count == self._n_tasks:
                count = 0
        return val

    @property
    def n_items(self):
        return self._n_items

    @property
    def n_tasks(self):
        return self._n_tasks


def main():
    args = parse_args()

    data = pd.read_csv(config.IN_DIR / args.input)
    task_names = data.columns
    problem = Problem(data)

    pop_size = args.p_size
    selection_type = SelectionType.Deterministic
    crossover_type = CrossoverType.PartialMappedCrossover
    crossover_rate = args.c_rate
    mutation_type = MutationType.Inversion
    mutation_rate = args.m_rate
    solver = GeneticAlgorithm(pop_size, problem.n_items, selection_type,
                              crossover_type, crossover_rate,
                              mutation_type, mutation_rate,
                              problem.compute_obj_value)
    result = []
    solver.initialize()
    for i in range(args.n_iter):
        solver.perform_crossover_operation()
        solver.perform_mutation_operation()
        solver.evaluate_fitness()
        solver.update_best_solution()
        solver.perform_selection()

        if not i % 10:
            opt_val = solver.best_chromosome
            print(f'iteration {i} :')
            print(f'{opt_val}: {problem.compute_obj_value(opt_val)}')

            temp = [0] * problem.n_items
            for j, v in enumerate(opt_val):
                temp[v] = task_names[j % problem.n_tasks]
            result.append(temp)

    with open(config.OUT_DIR / args.output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([f'n{i + 1}' for i in range(problem.n_items)])
        writer.writerows(result)


if __name__ == '__main__':
    main()
