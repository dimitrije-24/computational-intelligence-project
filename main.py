import random
import copy
from typing import List
import matplotlib.pyplot as plt

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

def initialize():
    map = {}
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == '.':
                map[(i,j)] = random.random() < 0.25
    return map

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

def count_mines(matrix, i, j):
    rows = len(array)
    cols = len(array[0])
    count = 0

    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x, y) != (i, j) and (x,y) in matrix and matrix[(x,y)]:
                count += 1

    return count

def calc_penalty(solution):
    n = len(array)
    m = len(array[0])
    penalty = 0

    for i in range(n):
        for j in range(m):
            if (i,j) not in solution:
                penalty += (int(array[i][j]) - count_mines(solution,i,j))**2
    return penalty

def random_search():

    best_one = None
    best_value = float('inf')
    #print('Best value',best_value)

    num_iters = 1000000
    values = [None for _ in range(num_iters)]

    for i in range(num_iters):
        solution = initialize()
        penalty = calc_penalty(solution)
        if penalty < best_value:
            best_one = solution
            best_value = penalty
        values[i] = best_value

    stampaj(best_one)
    print('Penalty',best_value)
    plt.plot(range(num_iters),values)
    plt.show()

random_search()