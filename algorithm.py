import random
import numpy as np
from enum import Enum


class CrossoverType(Enum):
    PartialMappedCrossover = 1
    OrderCrossover = 2
    PositionBasedCrossover = 3


class MutationType(Enum):
    Inversion = 1
    Insertion = 2
    Displacement = 3
    ReciprocalExchange = 4


class SelectionType(Enum):
    Deterministic = 1
    Stochastic = 2


class GeneticAlgorithm:
    def __init__(self, pop_size, number_of_genes, selection_type,
                 crossover_type, crossover_rate, mutation_type, mutation_rate,
                 compute_objective_value):

        self.pop_size = pop_size
        self.selection_type = selection_type
        self.crossover_size = int(pop_size * crossover_rate)
        if self.crossover_size % 2 == 1:
            self.crossover_size -= 1
        self.mutation_size = int(pop_size * mutation_rate)
        self.total_size = self.pop_size + self.mutation_size + self.crossover_size
        self.number_of_genes = number_of_genes
        self.crossover_type = crossover_type
        self.crossover_rate = crossover_rate
        self.mutation_type = mutation_type
        self.mutation_rate = mutation_rate
        self.compute_objective_value = compute_objective_value
        self.least_fitness_factor = 0.3
        self.mapping = [-1 for i in range(self.number_of_genes)]  # for crossover

    def initialize(self):
        self.selected_chromosomes = np.zeros((self.pop_size, self.number_of_genes))
        self.indexs = np.arange(self.total_size)
        self.chromosomes = np.zeros((self.total_size, self.number_of_genes), dtype=int)
        for i in range(self.pop_size):
            for j in range(self.number_of_genes):
                self.chromosomes[i][j] = j
            np.random.shuffle(self.chromosomes[i])

        for i in range(self.pop_size, self.total_size):
            for j in range(self.number_of_genes):
                self.chromosomes[i][j] = -1

        self.fitness = np.zeros(self.total_size)
        self.objective_values = np.zeros(self.total_size)
        self.best_chromosome = np.zeros(self.number_of_genes, dtype=int)
        self.best_fitness = 0

    def evaluate_fitness(self):
        for i, chromosome in enumerate(self.chromosomes[:self.pop_size]):
            self.objective_values[i] = self.compute_objective_value(chromosome)

        min_obj_val = np.min(self.objective_values)
        max_obj_val = np.max(self.objective_values)
        range_obj_val = max_obj_val - min_obj_val

        for i, obj in enumerate(self.objective_values):
            self.fitness[i] = max(self.least_fitness_factor * range_obj_val, pow(10, -5)) + \
                              (max_obj_val - obj)

    def update_best_solution(self):
        best_index = np.argmax(self.fitness)
        if self.best_fitness < self.fitness[best_index]:
            self.best_fitness = self.fitness[best_index]
            for i, gene in enumerate(self.chromosomes[best_index]):
                self.best_chromosome[i] = gene

    def _shuffle_index(self, length):
        for i in range(length):
            self.indexs[i] = i
        np.random.shuffle(self.indexs[:length])

    def perform_crossover_operation(self):
        self._shuffle_index(self.pop_size)

        child1_index = self.pop_size
        child2_index = self.pop_size + 1
        count_of_crossover = int(self.crossover_size / 2)
        for i in range(count_of_crossover):
            parent1_index = self.indexs[i]
            parent2_index = self.indexs[i + 1]

            if self.crossover_type == CrossoverType.PartialMappedCrossover:
                self._partial_mapped_crossover(parent1_index, parent2_index, child1_index, child2_index)
                self.objective_values[child1_index] = self.compute_objective_value(self.chromosomes[child1_index])
                self.objective_values[child2_index] = self.compute_objective_value(self.chromosomes[child2_index])

            child1_index += 2
            child2_index += 2

    def _partial_mapped_crossover(self, p1, p2, c1, c2):
        # reset
        for i in range(self.number_of_genes):
            self.mapping[i] = -1

        rand1 = random.randint(0, self.number_of_genes - 2)
        rand2 = random.randint(rand1 + 1, self.number_of_genes - 1)

        for i in range(rand1, rand2 + 1):
            c1_gene = self.chromosomes[p2][i]
            c2_gene = self.chromosomes[p1][i]

            if c1_gene == c2_gene:
                continue

            elif self.mapping[c1_gene] == -1 and self.mapping[c2_gene] == -1:
                self.mapping[c1_gene] = c2_gene
                self.mapping[c2_gene] = c1_gene

            elif self.mapping[c1_gene] == -1:
                self.mapping[c1_gene] = self.mapping[c2_gene]
                self.mapping[self.mapping[c2_gene]] = c1_gene
                self.mapping[c2_gene] = -2

            elif self.mapping[c2_gene] == -1:
                self.mapping[c2_gene] = self.mapping[c1_gene]
                self.mapping[self.mapping[c1_gene]] = c2_gene
                self.mapping[c1_gene] = -2

            else:
                self.mapping[self.mapping[c1_gene]] = self.mapping[c2_gene]
                self.mapping[self.mapping[c2_gene]] = self.mapping[c1_gene]
                self.mapping[c1_gene] = -3
                self.mapping[c2_gene] = -3

        for i in range(self.number_of_genes):
            if rand1 <= i <= rand2:
                self.chromosomes[c1][i] = self.chromosomes[p2][i]
                self.chromosomes[c2][i] = self.chromosomes[p1][i]
            else:
                if self.mapping[self.chromosomes[p1][i]] >= 0:
                    self.chromosomes[c1][i] = self.mapping[self.chromosomes[p1][i]]
                else:
                    self.chromosomes[c1][i] = self.chromosomes[p1][i]

                if self.mapping[self.chromosomes[p2][i]] >= 0:
                    self.chromosomes[c2][i] = self.mapping[self.chromosomes[p2][i]]
                else:
                    self.chromosomes[c2][i] = self.chromosomes[p2][i]

    def _do_roulette_wheel_selection(self, fitness_list):
        sum_fitness = sum(fitness_list)
        transition_probability = [fitness / sum_fitness for fitness in fitness_list]

        rand = random.random()
        sum_prob = 0
        for i, prob in enumerate(transition_probability):
            sum_prob += prob
            if sum_prob >= rand:
                return i

    def perform_selection(self):
        if self.selection_type == SelectionType.Deterministic:
            index = np.argsort(self.fitness)[::-1]
        elif self.selection_type == SelectionType.Stochastic:
            index = [self._do_roulette_wheel_selection(self.fitness) for i in range(self.pop_size)]
        else:
            index = self.indexs

        for i in range(self.pop_size):
            for j in range(self.number_of_genes):
                self.selected_chromosomes[i][j] = self.chromosomes[index[i]][j]

        for i in range(self.pop_size):
            for j in range(self.number_of_genes):
                self.chromosomes[i][j] = self.selected_chromosomes[i][j]

    def perform_mutation_operation(self):
        self._shuffle_index(self.pop_size + self.crossover_size)
        child1_index = self.pop_size + self.crossover_size
        for i in range(self.mutation_size):
            if self.mutation_type == MutationType.Inversion:
                parent1_index = self.indexs[i]
                self._inversion_mutation(parent1_index, child1_index)
                self.objective_values[child1_index] = self.compute_objective_value(self.chromosomes[child1_index])
                child1_index += 1

    def _inversion_mutation(self, p1, c1):
        rand1 = random.randint(0, self.number_of_genes - 2)
        rand2 = random.randint(rand1 + 1, self.number_of_genes - 1)
        for i in range(self.number_of_genes):
            if i < rand1 or i > rand2:
                self.chromosomes[c1][i] = self.chromosomes[p1][i]
            else:
                index = rand2 - (i - rand1)
                self.chromosomes[c1][i] = self.chromosomes[p1][index]
