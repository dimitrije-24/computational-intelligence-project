import random
import copy
from typing import List
import matplotlib.pyplot as plt
import time

arrayp = [['1','.'],['.','.']]

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

arrayp = [['1','.','1','.','1','.'],
         ['1','.','.','.','.','.'],
         ['.','.','3','.','.','1'],
         ['.','.','.','.','1','.'],
         ['1','2','.','.','.','.'],
         ['.','.','.','.','0','.']]

arrayp = [['.','1','.','.','.'],
         ['1','.','2','.','.'],
         ['.','.','.','3','.'],
         ['.','.','1','.','.'],
         ['.','.','.','.','.']]

def initialize():
    map = {}
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == '.':
                map[(i,j)] = random.random() < 0.25
    return map

def print_board(solution):
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

def count_mines(solution, i, j):
    rows = len(array)
    cols = len(array[0])
    count = 0

    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x, y) != (i, j) and (x,y) in solution and solution[(x,y)]:
                count += 1

    return count

def board_value(solution):
    n = len(array)
    m = len(array[0])
    penalty = 0

    for i in range(n):
        for j in range(m):
            if (i,j) not in solution:
                penalty += abs(int(array[i][j]) - count_mines(solution,i,j))
    return penalty

def calc_mines(solution):
    return len([x for x in solution if solution[x]])

def init_brute():
    map = {}
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == '.':
                map[(i,j)] = False
    return map

brute_best_solution = None
brute_best_value = float('inf')
brute_best_mines = float('inf')

def brute_force(solution,m,n):

    current_value = board_value(solution)
    current_mines = calc_mines(solution)

    global brute_best_solution
    global brute_best_value
    global brute_best_mines
    if current_value < brute_best_value or (current_value == brute_best_value and current_mines < brute_best_mines):
        brute_best_solution = copy.deepcopy(solution)
        brute_best_value = current_value
        brute_best_mines = current_mines

    for i in range(m,len(array)):
        for j in range(n,len(array[0])):
            if (i,j) in solution:
                solution[(i,j)] = True
                if j + 1 < len(array[0]):
                    brute_force(solution,i,j+1)
                else:
                    brute_force(solution,i+1,0)
                solution[(i,j)] = False

def random_search():

    best_one = None
    best_value = float('inf')

    num_iters = 10
    values = [None for _ in range(num_iters)]

    for i in range(num_iters):
        solution = initialize()
        penalty = board_value(solution)
        if penalty < best_value:
            best_one = solution
            best_value = penalty
        values[i] = best_value

    print('Board value',best_value)
    print_board(best_one)
    plt.plot(range(num_iters),values)
    plt.show()
        

def local_search_invert_best_improvement(solution,value):
    improved = True
    while improved:
        improved = False
        best = None
        best_value = value
        best_mine_count = calc_mines(solution)

        for elem in solution.keys():
            solution[elem] = not solution[elem]
            new_value = board_value(solution)
            current_mines = calc_mines(solution)
            if new_value < best_value or (new_value == best_value and current_mines < best_mine_count):
                best_value = new_value
                improved = True
                best = elem
                best_mine_count = current_mines
            solution[elem] = not solution[elem]
        if improved:
            solution[best] = not solution[best]
            value = best_value
    return solution, value

def change_solution(solution):
    new_solution = copy.deepcopy(solution)
    index = random.choice(list(solution.keys()))
    new_solution[index] = not new_solution[index]
    return new_solution

def simulated_annealing(num_iters):
    solution = initialize()
    value = board_value(solution)
    best = copy.deepcopy(solution)
    best_value = float('inf')
    best_mine_count = calc_mines(solution)

    for i in range(num_iters):
        new_solution = change_solution(solution)
        new_value = board_value(new_solution)
        current_mines = calc_mines(new_solution)
        if new_value < value:
            value = new_value
            solution = copy.deepcopy(new_solution)
            if new_value < best_value or (new_value == best_value and current_mines < best_mine_count):
                best_value = new_value
                best = copy.deepcopy(new_solution)
                best_mine_count = current_mines
        else:
            if random.random() < 1/(i+1):
                value = new_value
                solution = copy.deepcopy(new_solution)

    return best, best_value

def shake(solution,k):
    new_solution = copy.deepcopy(solution)
    chosen_elements = random.sample(list(solution.keys()),k)
    for elem in chosen_elements:
        new_solution[elem] = not new_solution[elem]
    return new_solution

def vns(k0,kn,num_iters):
    solution = initialize()
    value = board_value(solution)
    best_mine_count = calc_mines(solution)

    for i in range(num_iters):
        for k in range(k0,kn):
            new_solution = shake(solution,k)
            new_value = board_value(new_solution)
            new_solution, new_value = local_search_invert_best_improvement(new_solution,new_value)
            current_mines = calc_mines(new_solution)
            if new_value < value or (new_value == value and random.random() < 0.5 or
                                     new_value == value and current_mines < best_mine_count):
                value = new_value
                solution = copy.deepcopy(new_solution)
                best_mine_count = current_mines
                break
    return solution, value

def iterate():
    niz = []
    for i in range(100):
        print('Iteration #',(i+1))
        solution, value = vns(5,10,100)
        #solution_for_local_search = initialize()
        #value_for_local_search = board_value(solution_for_local_search)
        #solution, value = local_search_invert_best_improvement(solution_for_local_search,value_for_local_search)
        #solution, value = simulated_annealing(100000)
        niz.append(value)
    plt.plot(range(100),niz)
    plt.show()


#iterate()
start_time = time.time()
#solution, value = vns(5,10,100)
#solution, value = simulated_annealing(1000000)
solution_for_local_search = initialize()
value_for_local_search = board_value(solution_for_local_search)
#brute_solution = init_brute()
#brute_force(brute_solution,0,0)
solution, value = local_search_invert_best_improvement(solution_for_local_search,value_for_local_search)
    
#random_search()

#print_board(brute_best_solution)
#print(brute_best_value)

print_board(solution)
print(value)
print('Time elapsed: ', time.time() - start_time)