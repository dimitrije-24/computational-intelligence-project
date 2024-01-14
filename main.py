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
    return [[random.random() < 0.25 for _ in range(int(len(array)))] for _ in range(int(len(array[0])))]

solution = initialize()

def stampaj(niz):
    n = len(niz)
    m = len(niz[0])
    for i in range(n):
        for j in range(m):
            print(niz[i][j],end=' ')
        print('\n')

stampaj(array)

def change_array(niz,solution):
    n = len(niz)
    m = len(niz[0])
    for i in range(n):
        for j in range(m):
            if niz[i][j] == '.' and solution[i][j]:
                niz[i][j] = 'X'
    return niz

def count_mines(matrix, i, j):
    rows = len(matrix)
    cols = len(matrix[0])
    count = 0

    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x, y) != (i, j) and matrix[x][y] == 'X':
                count += 1

    return count

def calc_penalty(matrix):
    n = len(matrix)
    m = len(matrix[0])
    penalty = 0

    for i in range(n):
        for j in range(m):
            if matrix[i][j] != '.' and matrix[i][j] != 'X':
                penalty += (int(matrix[i][j]) - count_mines(matrix,i,j))**2
    return penalty

print(array)

best_one = copy.deepcopy(array)
best_value = float('inf')
print('Best value',best_value)

num_iters = 1000000
values = [None for _ in range(num_iters)]

for i in range(num_iters):
    solution = initialize()
    array2 = copy.deepcopy(array)
    array2 = change_array(array2,solution)
    penalty = calc_penalty(array2)
    if penalty < best_value:
        best_one = copy.deepcopy(array2)
        best_value = penalty
    values[i] = best_value

print('Penalty',best_value)
stampaj(best_one)
plt.plot(range(num_iters),values)
plt.show()