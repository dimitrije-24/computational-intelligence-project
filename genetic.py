import random
import copy
from typing import List
import matplotlib.pyplot as plt
import time

arrayp = [['1','.','.','.'],['.','.','.','.'],['.','.','4','.'],['.','.','.','.']]

array = [['1','.','1','.','1','.','2','.','1','1'],
         ['1','.','.','.','.','.','.','.','.','1'],
         ['.','.','3','.','.','2','.','.','.','.'],
         ['.','.','.','.','1','.','.','3','3','.'],
         ['1','1','1','.','.','.','.','2','.','3'],
         ['.','.','.','.','0','.','1','.','3','.'],
         ['.','.','.','1','.','.','2','.','4','.'],
         ['0','.','.','3','.','.','4','.','.','.'],
         ['.','3','.','2','.','.','4','.','.','2'],
         ['.','.','.','.','.','.','.','2','.','0']]

class Individual:
    def __init__(self):
        self.code = self.initialize()
        self.fitness = self.board_value()
        self.mines_total = self.count_total_mines()

    def initialize(self):
        map = {}
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] == '.':
                    map[(i,j)] = random.random() < 0.25
        return map
    
    def board_value(self):
        n = len(array)
        m = len(array[0])
        penalty = 0

        for i in range(n):
            for j in range(m):
                if (i,j) not in self.code:
                    penalty += abs(int(array[i][j]) - Individual.count_mines(self.code,i,j))
        return penalty
    
    def count_total_mines(self):
        return len([x for x in self.code if self.code[x]])

    
    @staticmethod
    def count_mines(matrix, i, j):
        rows = len(array)
        cols = len(array[0])
        count = 0

        for x in range(max(0, i - 1), min(rows, i + 2)):
            for y in range(max(0, j - 1), min(cols, j + 2)):
                if (x, y) != (i, j) and (x,y) in matrix and matrix[(x,y)]:
                    count += 1

        return count

def selection(population,tournament_size):
    choice = random.sample(population,tournament_size)
    return min(choice,key=lambda x:(x.fitness,x.mines_total))

def crossover(parent1,parent2,child1,child2):
    
    random_elem = random.choice(list(parent1.code))

    for elem in parent1.code.keys():
        if elem[0] < random_elem[0] or elem[1] < random_elem[1]:
            child1.code[elem] = parent1.code[elem]
        else:
            child1.code[elem] = parent2.code[elem]
    
    for elem in parent1.code.keys():
        if elem[0] < random_elem[0] or elem[1] < random_elem[1]:
            child2.code[elem] = parent2.code[elem]
        else:
            child2.code[elem] = parent1.code[elem]

def mutation(individual,mutation_prob):
    for elem in individual.code.keys():
        if random.random() < mutation_prob:
            individual.code[elem] = not individual.code[elem]

def ga(population_size,num_generations,elitism_size,tournament_size,mutation_prob):
    population = [Individual() for _ in range(population_size)]
    new_population = population.copy()

    values = [None for _ in range(num_generations)]

    for i in range(num_generations):
        print('Generation number',i)
        population.sort(key=lambda x: x.fitness)
        new_population[:elitism_size] = population[:elitism_size]
        for j in range(elitism_size,population_size,2):
            parent1 = selection(population,tournament_size)
            parent2 = selection(population,tournament_size)

            crossover(parent1,parent2,child1=new_population[j],child2=new_population[j+1])
            
            mutation(new_population[j],mutation_prob)
            mutation(new_population[j+1],mutation_prob)

            new_population[j].fitness = new_population[j].board_value()
            new_population[j+1].fitness = new_population[j+1].board_value()

            new_population[j].fitness = new_population[j].count_total_mines()
            new_population[j].fitness = new_population[j+1].count_total_mines()

        population = new_population.copy()

        value = min(population,key=lambda x : (x.fitness,x.mines_total))
        values[i] = value.fitness
    
    print('Time needed: ', time.time() - start_time)
    plt.plot(range(num_generations),values)
    plt.show()
    return min(population,key=lambda x: (x.fitness,x.mines_total))

def stampaj(solution):
    n = len(array)
    m = len(array[0])
    for i in range(n):
        for j in range(m):
            if (i,j) in solution:
                if solution[(i,j)]:
                    print('X',end=' ')
                else:
                    print('.',end=' ')
            else:
                print(array[i][j],end=' ')
        print('\n')

start_time = time.time()
best_individual = ga(population_size=100,num_generations=100,elitism_size=30,tournament_size=70,mutation_prob=0.05)
stampaj(best_individual.code)
print(best_individual.fitness)